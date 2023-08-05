#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import logging
import traceback

from monero_glue.agent import agent_misc
from monero_glue.hwtoken import misc as tmisc
from monero_glue.messages import (
    Failure,
    MoneroGetAddress,
    MoneroGetWatchKey,
    MoneroGetTxKeyRequest,
    MoneroGetTxKeyAck,
    MoneroKeyImageSyncFinalRequest,
    MoneroKeyImageSyncStepRequest,
    MoneroLiveRefreshStartRequest,
    MoneroLiveRefreshStartAck,
    MoneroLiveRefreshStepRequest,
    MoneroLiveRefreshStepAck,
    MoneroLiveRefreshFinalRequest,
    MoneroLiveRefreshFinalAck,
    MoneroTransactionAllInputsSetAck,
    MoneroTransactionAllInputsSetRequest,
    MoneroTransactionAllOutSetAck,
    MoneroTransactionAllOutSetRequest,
    MoneroTransactionData,
    MoneroTransactionFinalAck,
    MoneroTransactionFinalRequest,
    MoneroTransactionInitAck,
    MoneroTransactionInitRequest,
    MoneroTransactionInputsPermutationRequest,
    MoneroTransactionInputViniRequest,
    MoneroTransactionRsigData,
    MoneroTransactionSetInputAck,
    MoneroTransactionSetInputRequest,
    MoneroTransactionSetOutputAck,
    MoneroTransactionSetOutputRequest,
    MoneroTransactionSignInputAck,
    MoneroTransactionSignInputRequest,
    MoneroOutputEntry,
)
from monero_glue.protocol_base.base import TError
from monero_glue.xmr import common, crypto, key_image, monero, ring_ct
from monero_glue.xmr.enc import chacha_poly
from monero_glue.xmr.sub import addr as xmr_addr
from monero_serialize import xmrserialize, xmrtypes

logger = logging.getLogger(__name__)


DEFAULT_MONERO_BIP44 = [
    0x8000002C,
    0x80000080,
    0x80000000,
]  # parse_path(monero.DEFAULT_BIP32_PATH)


def get_rsig_type(us_bulletproof, num_outputs):
    if not us_bulletproof:
        return 0  # Borromean
    elif num_outputs > 16:
        return 2  # Multioutputs
    else:
        return 3  # Padded


def generate_rsig_batch_sizes(rsig_type, num_outputs):
    amount_batched = 0
    batches = []

    while amount_batched < num_outputs:
        if rsig_type == 0 or rsig_type == 1:  # Borromean, BP per output
            batches.append(1)
            amount_batched += 1

        elif rsig_type == 3:  # BP padded
            if num_outputs > 16:
                raise ValueError(
                    "BP padded can support only BULLETPROOF_MAX_OUTPUTS statements"
                )

            batches.append(num_outputs)
            amount_batched += num_outputs

        elif rsig_type == 2:  # multioutput
            batch_size = 1
            while (
                batch_size * 2 + amount_batched <= num_outputs and batch_size * 2 <= 16
            ):
                batch_size *= 2
            batch_size = min(batch_size, num_outputs - amount_batched)
            batches.append(batch_size)
            amount_batched += batch_size

        else:
            raise ValueError("Unknown rsig type")
    return batches


class TData(object):
    """
    Agent transaction-scoped data
    """

    def __init__(self):
        self.tsx_data = None  # type: MoneroTransactionData
        self.tx_data = None  # construction data
        self.rsig_type = 0
        self.rsig_batches = []
        self.rsig_param = None
        self.cur_input_idx = 0
        self.cur_output_idx = 0
        self.cur_batch_idx = 0
        self.cur_output_in_batch_idx = 0
        self.tx = xmrtypes.Transaction(version=2, vin=[], vout=[], extra=[])
        self.tx_in_hmacs = []
        self.tx_out_entr_hmacs = []
        self.tx_out_hmacs = []
        self.tx_out_rsigs = []
        self.tx_out_pk = []
        self.tx_out_ecdh = []
        self.source_permutation = []
        self.alphas = []
        self.spend_encs = []
        self.pseudo_outs = []
        self.couts = []
        self.rsig_gamma = []
        self.tx_prefix_hash = None
        self.enc_salt1 = None
        self.enc_salt2 = None
        self.enc_keys = None  # encrypted tx keys
        self.rv = None


class SignAuxData(object):
    def __init__(self):
        self.destinations = None  # type: list[tuple[xmr_addr.AddrInfo, int]]


class Agent(object):
    """
    Glue agent, running on host
    """

    def __init__(
        self, trezor, address_n=None, network_type=None, slip0010=True, **kwargs
    ):
        self.trezor = trezor
        self.ct = None  # type: TData
        self.address_n = address_n if address_n else DEFAULT_MONERO_BIP44
        self.network_type = network_type
        if not slip0010:
            raise ValueError("Non-SLIP0010 not supported anymore")
        if address_n and 0 in address_n:
            raise ValueError("SLIP0010 cannto contain public derivation")
        if address_n is None:
            self.address_n = DEFAULT_MONERO_BIP44

        self.hf = 10
        self.client_version = 1
        self.subaddresses = {}

    def is_simple(self, rv):
        """
        True if simpe
        :param rv:
        :return:
        """
        return rv.type in [
            xmrtypes.RctType.Simple,
            xmrtypes.RctType.Bulletproof,
            xmrtypes.RctType.Bulletproof2,
        ]

    def is_bulletproof(self, rv):
        """
        True if bulletproof
        :param rv:
        :return:
        """
        return rv.type in [xmrtypes.RctType.Bulletproof, xmrtypes.RctType.Bulletproof2]

    def is_error(self, response):
        """
        True if trezor returned an error
        :param response:
        :return:
        """
        return isinstance(response, TError) or isinstance(response, Failure)

    def handle_error(self, response):
        """
        Raises an error if Trezor returned an error.
        :param response:
        :return:
        """
        if not self.is_error(response):
            return
        raise agent_misc.TrezorReturnedError(resp=response)

    async def sign_unsigned_tx(self, unsig):
        """
        Processes unsigned transaction set, returns serialized signed transactions.
        :param unsig:
        :return:
        """
        txes = []
        for tx in unsig.txes:
            await self.sign_transaction_data(tx)
            txes.append(await self.serialized_tx())

        return txes

    async def sign_tx(self, construction_data):
        """
        Transfers transaction, serializes response

        :param construction_data:
        :return:
        """
        if not isinstance(construction_data, list):
            construction_data = [construction_data]

        txes = []
        for tdata in construction_data:
            await self.sign_transaction_data(tdata)
            txes.append(await self.serialized_tx())

        return txes

    async def serialized_tx(self):
        """
        Returns the last signed transaction as blob
        :return:
        """
        return await self.serialize_tx(self.ct.tx)

    async def serialize_tx(self, tx):
        """
        Serializes transaction
        :param tx:
        :return:
        """
        writer = xmrserialize.MemoryReaderWriter()
        ar1 = xmrserialize.Archive(writer, True, xmrtypes.hf_versions(self.hf))
        await ar1.message(tx, msg_type=xmrtypes.Transaction)
        return bytes(writer.get_buffer())

    def _is_req_bulletproof(self):
        return self.ct.rsig_type != 0

    def _is_bulletproof(self):
        if self.ct.rv is None:
            raise ValueError("RV is None")
        return self.ct.rv.type in (3, 4)

    def _is_simple(self):
        if self.ct.rv is None:
            raise ValueError("RV is None")
        return self.ct.rv.type == 2

    def _is_offloading(self):
        return self.ct and self.ct.rsig_param and self.ct.rsig_param.offload_type != 0

    def _num_outputs(self):
        return len(self.ct.tx_data.splitted_dsts)

    def _num_inputs(self):
        return len(self.ct.tx_data.sources)

    def _get_integrated_idx(self, outputs, aux_data=None):
        if aux_data is None or aux_data.destinations is None:
            return []

        integrated_indices = []
        integrated_pairs = []
        for idx, cur in enumerate(aux_data.destinations):
            ainfo = cur[0]
            if ainfo.is_integrated:
                caddr = xmr_addr.build_address(ainfo.spend_key, ainfo.view_key)
                integrated_pairs.append((caddr, cur[1]))

        for idx, dst in enumerate(outputs):
            for ipair in integrated_pairs:
                if xmr_addr.addr_eq(ipair[0], dst.addr) and dst.amount == ipair[1]:
                    integrated_indices.append(idx)

        logger.debug("Integrated indices: %s" % len(integrated_indices))
        return integrated_indices

    def _strip_sources(self, sources, keep_idx=True):
        """
        Stripping unnecessary information from a transfer. Speeds up the input processing stages as
        mixin keys are needed only in the last step of the protocol - signatures.

        Unfortunately, not applicable yet because HMAC over src_entr would differ.
        Further analysis of this is required to determine how to HMAC src_entr.
        Proposal:
            - Hash whole outputs subpart to a single hash file. src_entry.output_hash.
            - Exclude src_entry.outputs from the HMAC. output_hash is included in HMAC
            - Signature step fails if output_hash is not matching.

        :param sources:
        :param keep_idx:
        :return:
        """
        for idx in range(len(sources.outputs)):
            if idx == sources.real_output:
                continue
            sources.outputs[idx] = (
                MoneroOutputEntry(idx=sources.outputs[idx].idx)
                if keep_idx
                else MoneroOutputEntry()
            )
        return sources

    async def sign_transaction_data(
        self,
        tx,
        multisig=False,
        exp_tx_prefix_hash=None,
        use_tx_keys=None,
        aux_data=None,
    ):
        """
        Uses Trezor to sign the transaction
        :param tx:
        :type tx: xmrtypes.TxConstructionData
        :param multisig:
        :param exp_tx_prefix_hash:
        :param use_tx_keys:
        :param aux_data:
        :return:
        """
        self.ct = TData()
        self.ct.tx_data = tx

        payment_id = []
        extras = await monero.parse_extra_fields(tx.extra)
        extra_nonce = monero.find_tx_extra_field_by_type(extras, xmrtypes.TxExtraNonce)
        if extra_nonce and monero.has_encrypted_payment_id(extra_nonce.nonce):
            payment_id = monero.get_encrypted_payment_id_from_tx_extra_nonce(
                extra_nonce.nonce
            )
        elif extra_nonce and monero.has_payment_id(extra_nonce.nonce):
            payment_id = monero.get_payment_id_from_tx_extra_nonce(extra_nonce.nonce)

        # Init transaction
        tsx_data = MoneroTransactionData()
        tsx_data.version = 1
        tsx_data.client_version = self.client_version
        tsx_data.payment_id = payment_id
        tsx_data.unlock_time = tx.unlock_time
        tsx_data.outputs = [
            tmisc.translate_monero_dest_entry_pb(x) for x in tx.splitted_dsts
        ]
        tsx_data.change_dts = tmisc.translate_monero_dest_entry_pb(tx.change_dts)
        tsx_data.num_inputs = len(tx.sources)
        tsx_data.mixin = len(tx.sources[0].outputs)
        tsx_data.fee = sum([x.amount for x in tx.sources]) - sum(
            [x.amount for x in tx.splitted_dsts]
        )
        tsx_data.account = tx.subaddr_account
        tsx_data.minor_indices = tx.subaddr_indices
        tsx_data.integrated_indices = self._get_integrated_idx(
            tsx_data.outputs, aux_data
        )
        self.ct.tx.unlock_time = tx.unlock_time

        # Rsig
        num_outputs = len(tsx_data.outputs)
        use_bp = common.defattr(tx, "use_bulletproofs", False)
        self.ct.rsig_type = get_rsig_type(use_bp, num_outputs)
        self.ct.rsig_batches = generate_rsig_batch_sizes(self.ct.rsig_type, num_outputs)
        rsig_data = MoneroTransactionRsigData(
            rsig_type=self.ct.rsig_type, grouping=self.ct.rsig_batches
        )
        tsx_data.rsig_data = rsig_data

        if self.hf >= 10:
            tsx_data.rsig_data.bp_version = 2

        self.ct.tsx_data = tsx_data
        init_msg = MoneroTransactionInitRequest(
            version=0,
            address_n=self.address_n,
            network_type=self.network_type,
            tsx_data=tsx_data,
        )

        t_res = await self.trezor.tsx_sign(init_msg)  # type: MoneroTransactionInitAck
        self.handle_error(t_res)

        self.ct.tx_out_entr_hmacs = t_res.hmacs
        self.ct.rsig_param = t_res.rsig_data

        # Set transaction inputs
        for idx, src in enumerate(tx.sources):
            src_pb = tmisc.translate_monero_src_entry_pb(src)
            msg = MoneroTransactionSetInputRequest(src_entr=src_pb)

            t_res = await self.trezor.tsx_sign(
                msg
            )  # type: MoneroTransactionSetInputAck
            self.handle_error(t_res)

            vini_p = await tmisc.parse_msg(t_res.vini, xmrtypes.TxInV())
            vini = vini_p.txin_to_key
            self.ct.tx.vin.append(vini)
            self.ct.tx_in_hmacs.append(t_res.vini_hmac)
            self.ct.pseudo_outs.append((t_res.pseudo_out, t_res.pseudo_out_hmac))
            self.ct.alphas.append(t_res.pseudo_out_alpha)
            self.ct.spend_encs.append(t_res.spend_key)

        # Sort key image
        self.ct.source_permutation = list(range(len(tx.sources)))
        self.ct.source_permutation.sort(
            key=lambda x: self.ct.tx.vin[x].k_image, reverse=True
        )

        def swapper(x, y):
            self.ct.tx.vin[x], self.ct.tx.vin[y] = self.ct.tx.vin[y], self.ct.tx.vin[x]
            self.ct.tx_in_hmacs[x], self.ct.tx_in_hmacs[y] = (
                self.ct.tx_in_hmacs[y],
                self.ct.tx_in_hmacs[x],
            )
            self.ct.pseudo_outs[x], self.ct.pseudo_outs[y] = (
                self.ct.pseudo_outs[y],
                self.ct.pseudo_outs[x],
            )
            self.ct.alphas[x], self.ct.alphas[y] = self.ct.alphas[y], self.ct.alphas[x]
            self.ct.spend_encs[x], self.ct.spend_encs[y] = (
                self.ct.spend_encs[y],
                self.ct.spend_encs[x],
            )
            tx.sources[x], tx.sources[y] = tx.sources[y], tx.sources[x]

        common.apply_permutation(self.ct.source_permutation, swapper)

        msg = MoneroTransactionInputsPermutationRequest(perm=self.ct.source_permutation)
        t_res = await self.trezor.tsx_sign(msg)
        self.handle_error(t_res)

        # Set vin_i back - tx prefix hashing
        for idx in range(len(self.ct.tx.vin)):
            src_pb = tmisc.translate_monero_src_entry_pb(tx.sources[idx])
            msg = MoneroTransactionInputViniRequest(
                src_entr=src_pb,
                vini=await tmisc.dump_msg(self.ct.tx.vin[idx], prefix=b"\x02"),
                vini_hmac=self.ct.tx_in_hmacs[idx],
                orig_idx=self.ct.source_permutation[idx],
            )
            t_res = await self.trezor.tsx_sign(msg)
            self.handle_error(t_res)

        # All inputs set
        t_res = await self.trezor.tsx_sign(
            MoneroTransactionAllInputsSetRequest()
        )  # type: MoneroTransactionAllInputsSetAck
        self.handle_error(t_res)
        await self._on_all_input_set(t_res)

        # Set transaction outputs
        for idx, dst in enumerate(tx.splitted_dsts):
            msg = await self._step_set_outputs(idx, dst)

            t_res = await self.trezor.tsx_sign(
                msg
            )  # type: MoneroTransactionSetOutputAck
            self.handle_error(t_res)

            await self._on_set_outputs_ack(idx, dst, t_res)

        t_res = await self.trezor.tsx_sign(
            MoneroTransactionAllOutSetRequest()
        )  # type: MoneroTransactionAllOutSetAck
        self.handle_error(t_res)

        rv = xmrtypes.RctSig()
        rv.p = xmrtypes.RctSigPrunable()
        rv.txnFee = t_res.rv.txn_fee
        rv.message = t_res.rv.message
        rv.type = t_res.rv.rv_type
        self.ct.tx.extra = list(bytearray(t_res.extra))

        # Verify transaction prefix hash correctness, tx hash in one pass
        self.ct.tx_prefix_hash = await monero.get_transaction_prefix_hash(self.ct.tx)
        if not common.ct_equal(t_res.tx_prefix_hash, self.ct.tx_prefix_hash):
            raise ValueError("Transaction prefix has does not match")

        # RctSig
        if self.is_simple(rv):
            if self.is_bulletproof(rv):
                rv.p.pseudoOuts = [x[0] for x in self.ct.pseudo_outs]
            else:
                rv.pseudoOuts = [x[0] for x in self.ct.pseudo_outs]

        # Range proof
        rv.p.rangeSigs = []
        rv.p.bulletproofs = []
        rv.outPk = []
        rv.ecdhInfo = []
        for idx in range(len(self.ct.tx_out_pk)):
            rv.outPk.append(self.ct.tx_out_pk[idx])
            rv.ecdhInfo.append(self.ct.tx_out_ecdh[idx])

        for idx in range(len(self.ct.tx_out_rsigs)):
            if self.is_bulletproof(rv):
                rv.p.bulletproofs.append(self.ct.tx_out_rsigs[idx])
            else:
                rv.p.rangeSigs.append(self.ct.tx_out_rsigs[idx])

        mlsag_hash = t_res.full_message_hash
        mlsag_hash_computed = await monero.get_pre_mlsag_hash(rv)
        if not common.ct_equal(mlsag_hash, mlsag_hash_computed):
            raise ValueError("Pre MLSAG hash has does not match")

        # Sign each input
        couts = []
        rv.p.MGs = []
        for idx, src in enumerate(tx.sources):
            msg = MoneroTransactionSignInputRequest(
                src_entr=tmisc.translate_monero_src_entry_pb(src),
                vini=await tmisc.dump_msg(self.ct.tx.vin[idx], prefix=b"\x02"),
                vini_hmac=self.ct.tx_in_hmacs[idx],
                pseudo_out=self.ct.pseudo_outs[idx][0],
                pseudo_out_hmac=self.ct.pseudo_outs[idx][1],
                pseudo_out_alpha=self.ct.alphas[idx],
                spend_key=self.ct.spend_encs[idx],
                orig_idx=self.ct.source_permutation[idx],
            )
            t_res = await self.trezor.tsx_sign(
                msg
            )  # type: MoneroTransactionSignInputAck
            self.handle_error(t_res)

            if self.client_version > 0 and t_res.pseudo_out:
                self.ct.pseudo_outs[idx] = t_res.pseudo_out, self.ct.pseudo_outs[idx][1]
                if self.is_bulletproof(rv):
                    rv.p.pseudoOuts[idx] = t_res.pseudo_out
                else:
                    rv.pseudoOuts[idx] = t_res.pseudo_out

            mg = await tmisc.parse_msg(t_res.signature, xmrtypes.MgSig())
            rv.p.MGs.append(mg)
            couts.append(None)

        self.ct.tx.signatures = []
        self.ct.tx.rct_signatures = rv

        t_res = await self.trezor.tsx_sign(
            MoneroTransactionFinalRequest()
        )  # type: MoneroTransactionFinalAck
        self.handle_error(t_res)

        if multisig:
            cout_key = t_res.cout_key
            for ccout in couts:
                self.ct.couts.append(chacha_poly.decrypt_pack(cout_key, ccout))

        self.ct.enc_salt1, self.ct.enc_salt2 = t_res.salt, t_res.rand_mult
        self.ct.enc_keys = t_res.tx_enc_keys
        return self.ct.tx

    async def _on_all_input_set(self, ack):
        if not self._is_offloading() or self.client_version > 0:
            return

        if ack.rsig_data is None:
            raise ValueError("Rsig offloading requires rsig param")

        rsig_data = ack.rsig_data
        if rsig_data.mask is None:
            raise ValueError("Gamma masks not present in offloaded version")

        mask = rsig_data.mask
        if len(mask) != self._num_outputs() * 32:
            raise ValueError("Invalid number of masks: %s" % len(mask))

        for i in range(len(mask) // 32):
            self.ct.rsig_gamma.append(mask[i * 32 : (i + 1) * 32])

    async def _step_set_outputs(self, idx, dst):
        self.ct.cur_output_idx = idx
        self.ct.cur_output_in_batch_idx += 1

        msg = MoneroTransactionSetOutputRequest(
            dst_entr=tmisc.translate_monero_dest_entry_pb(dst),
            dst_entr_hmac=self.ct.tx_out_entr_hmacs[idx],
        )

        # Range sig offloading to the host
        if self.client_version == 0 and self._is_offloading():
            return await self._v0_offloading(idx, dst, msg)

        return msg

    async def _v0_offloading(self, idx, dst, msg):
        offload_res = await self._rct_offload(idx, dst)
        if offload_res:
            msg.rsig_data = offload_res

        return msg

    async def _rct_offload(self, idx, dst):
        if (
            self.ct.rsig_batches[self.ct.cur_batch_idx]
            > self.ct.cur_output_in_batch_idx
        ):
            return None

        rsig_data = MoneroTransactionRsigData()
        batch_size = self.ct.rsig_batches[self.ct.cur_batch_idx]

        if not self._is_req_bulletproof():
            if batch_size > 1:
                raise ValueError("Borromean cannot batch outputs")

            mask = crypto.decodeint(self.ct.rsig_gamma[idx])
            C, a, R = ring_ct.prove_range_mem(dst.amount, mask)
            rsig_data.rsig = tmisc.dump_msg(R)
            self.ct.tx_out_rsigs.append(R)

        else:
            amounts = []
            masks = []
            for i in range(batch_size):
                amounts.append(
                    self.ct.tx_data.splitted_dsts[1 + idx - batch_size + i].amount
                )
                masks.append(
                    crypto.decodeint(self.ct.rsig_gamma[1 + idx - batch_size + i])
                )

            bp = await ring_ct.prove_range_bp_batch(amounts, masks)
            self.ct.tx_out_rsigs.append(bp)

            rsig_data.rsig = await tmisc.dump_msg(bp)
        return rsig_data

    async def _on_set_outputs_ack(self, idx, dst, t_res):
        self.ct.tx.vout.append(await tmisc.parse_msg(t_res.tx_out, xmrtypes.TxOut()))
        self.ct.tx_out_hmacs.append(t_res.vouti_hmac)
        self.ct.tx_out_pk.append(await tmisc.parse_msg(t_res.out_pk, xmrtypes.CtKey()))

        # hf10 encodes only 8B amount
        if self.hf == 9:
            self.ct.tx_out_ecdh.append(
                await tmisc.parse_msg(t_res.ecdh_info, xmrtypes.EcdhTuple())
            )

        else:
            cur_ecdh = xmrtypes.EcdhTuple(
                mask=crypto.NULL_KEY_ENC, amount=bytearray(crypto.NULL_KEY_ENC)
            )
            cur_ecdh.amount[0:8] = bytearray(t_res.ecdh_info)
            self.ct.tx_out_ecdh.append(cur_ecdh)

        rsig_buff = None
        if t_res.rsig_data:
            tsig_data = t_res.rsig_data

            if tsig_data.rsig and len(tsig_data.rsig) > 0:
                rsig_buff = tsig_data.rsig
            elif tsig_data.rsig_parts and len(tsig_data.rsig_parts) > 0:
                rsig_buff = b"".join(tsig_data.rsig_parts)

            if self.client_version >= 1 and tsig_data.mask:
                logger.debug("MASK received")
                self.ct.rsig_gamma.append(tsig_data.mask)

        # Client1: send generated BP if offloading
        if self.client_version >= 1 and self._is_offloading():
            proc = await self._v1_offloading(idx, dst, t_res)
            if not proc:
                return  # no state advance

        else:
            rsig = None
            if rsig_buff and not self._is_req_bulletproof():
                rsig = await tmisc.parse_msg(rsig_buff, xmrtypes.RangeSig())
            elif rsig_buff:
                rsig = await tmisc.parse_msg(rsig_buff, xmrtypes.Bulletproof())
            else:
                return  # no state change

            await self._out_proc_range_proof(rsig)

        # batch state advance
        self.ct.cur_batch_idx += 1
        self.ct.cur_output_in_batch_idx = 0

    async def _out_proc_range_proof(self, rsig):
        if self._is_req_bulletproof():
            rsig.V = []
            batch_size = self.ct.rsig_batches[self.ct.cur_batch_idx]
            for i in range(batch_size):
                commitment = self.ct.tx_out_pk[
                    1 + self.ct.cur_output_idx - batch_size + i
                ].mask
                commitment = crypto.scalarmult(
                    crypto.decodepoint(commitment), crypto.sc_inv_eight()
                )
                rsig.V.append(crypto.encodepoint(commitment))

        self.ct.tx_out_rsigs.append(rsig)

        # Rsig verification
        try:
            if not ring_ct.ver_range(
                C=crypto.decodepoint(self.ct.tx_out_pk[-1].mask),
                rsig=rsig,
                use_bulletproof=self._is_req_bulletproof(),
            ):
                logger.warning("Rsing not valid")

        except Exception as e:
            logger.error("Exception rsig: %s" % e)
            traceback.print_exc()

    async def _v1_offloading(self, idx, dst, t_res):
        """
        Client V2 range proof offloading.
        Performs additional round trip
        """
        rsig_data = await self._rct_offload(idx, dst)
        if not rsig_data:
            return False

        msg = MoneroTransactionSetOutputRequest(
            rsig_data=rsig_data, is_offloaded_bp=True
        )

        t_res = await self.trezor.tsx_sign(msg)  # type: MoneroTransactionSetOutputAck
        self.handle_error(t_res)
        return True

    def last_transaction_data(self):
        """
        Returns last transaction data
        :return:
        """
        return self.ct

    async def get_address(
        self, account=0, minor=0, payment_id=None, show_display=False
    ):
        """
        Get address from the device
        :return:
        """
        msg = MoneroGetAddress(
            address_n=self.address_n,
            network_type=self.network_type,
            account=account,
            minor=minor,
            show_display=show_display,
        )

        msg.payment_id = payment_id
        res = await self.trezor.call(msg)
        return res

    async def get_watch_only(self):
        """
        Watch only key load
        :return:
        """
        msg = MoneroGetWatchKey(
            address_n=self.address_n, network_type=self.network_type
        )
        res = await self.trezor.get_view_key(msg)
        return res

    async def import_outputs(self, outputs):
        """
        Key images sync. Required for hot wallet be able to construct transactions.
        If the signed transaction is not relayed with the hot wallet it gets out of sync with
        key images. Thus importing is needed.

        Wallet2::import_outputs()

        :param outputs:
        :return:
        """
        ki_export_init = await key_image.generate_commitment(outputs)
        ki_export_init.address_n = self.address_n
        ki_export_init.network_type = self.network_type
        t_res = await self.trezor.key_image_sync(ki_export_init)
        self.handle_error(t_res)

        sub_res = []
        iter = await key_image.yield_key_image_data(outputs)
        batches = common.chunk(iter, 10)
        for rr in batches:  # type: list[key_image.MoneroTransferDetails]
            t_res = await self.trezor.key_image_sync(
                MoneroKeyImageSyncStepRequest(tdis=rr)
            )
            self.handle_error(t_res)

            sub_res += t_res.kis

        t_res = await self.trezor.key_image_sync(MoneroKeyImageSyncFinalRequest())
        self.handle_error(t_res)

        # Decrypting phase
        enc_key = bytes(t_res.enc_key)
        final_res = []
        for sub in sub_res:  # type: key_image.MoneroExportedKeyImage
            plain = chacha_poly.decrypt(enc_key, bytes(sub.iv), bytes(sub.blob))
            ki_bin = plain[:32]

            # ki = crypto.decodepoint(ki_bin)
            # sig = [crypto.decodeint(plain[32:64]), crypto.decodeint(plain[64:])]

            final_res.append((ki_bin, (plain[32:64], plain[64:])))

        return final_res

    async def _get_tx_key_intern(
        self,
        salt1,
        salt2,
        tx_enc_keys,
        tx_prefix_hash,
        view_key_priv,
        view_public_key=None,
        reason=0,
    ):
        msg = MoneroGetTxKeyRequest(
            address_n=self.address_n, network_type=self.network_type
        )
        msg.salt1 = salt1
        msg.salt2 = salt2
        msg.tx_enc_keys = tx_enc_keys
        msg.tx_prefix_hash = tx_prefix_hash
        msg.reason = reason
        msg.view_public_key = view_public_key
        t_res = await self.trezor.get_tx_key(msg)  # type: MoneroGetTxKeyAck
        self.handle_error(t_res)

        enc_key = self._compute_tx_key_host(view_key_priv, tx_prefix_hash, t_res.salt)
        decr = chacha_poly.decrypt_pack(
            enc_key, t_res.tx_keys if reason == 0 else t_res.tx_derivations
        )
        if len(decr) % 32 != 0:
            raise ValueError("Invalid length")
        return bytearray(decr)

    async def get_tx_key(
        self, salt1, salt2, tx_enc_keys, tx_prefix_hash, view_key_priv
    ):
        decr = await self._get_tx_key_intern(
            salt1, salt2, tx_enc_keys, tx_prefix_hash, view_key_priv
        )
        n_keys = len(decr) // 32
        res = []
        for i in range(n_keys):
            res.append(crypto.decodeint(decr[i * 32 : (i + 1) * 32]))
        return res

    async def get_tx_deriv(
        self, salt1, salt2, tx_enc_keys, tx_prefix_hash, view_key_priv, view_key_pub
    ):
        decr = await self._get_tx_key_intern(
            salt1, salt2, tx_enc_keys, tx_prefix_hash, view_key_priv, view_key_pub, 1
        )
        n_keys = len(decr) // 32
        res = []
        for i in range(n_keys):
            res.append(crypto.decodepoint(decr[i * 32 : (i + 1) * 32]))
        return res

    @staticmethod
    def _compute_tx_key_host(view_key_private, tx_prefix_hash, salt):
        passwd = crypto.keccak_2hash(
            crypto.encodeint(view_key_private) + tx_prefix_hash
        )
        tx_key = crypto.compute_hmac(salt, passwd)
        return tx_key

    async def live_refresh_start(self):
        msg = MoneroLiveRefreshStartRequest(
            address_n=self.address_n, network_type=self.network_type
        )
        t_res = await self.trezor.live_refresh(msg)
        self.handle_error(t_res)

    async def live_refresh_final(self):
        t_res = await self.trezor.live_refresh(MoneroLiveRefreshFinalRequest())
        self.handle_error(t_res)

    async def live_refresh(
        self, view_key_private, out_key, recv_deriv, real_out_idx, major, minor
    ):
        msg = MoneroLiveRefreshStepRequest(
            out_key=out_key,
            recv_deriv=recv_deriv,
            real_out_idx=real_out_idx,
            sub_addr_major=major,
            sub_addr_minor=minor,
        )
        t_res = await self.trezor.live_refresh(msg)  # type: MoneroLiveRefreshStepAck
        self.handle_error(t_res)

        enc_key = self._compute_ki_enc_key_host(view_key_private, out_key, t_res.salt)
        decr = chacha_poly.decrypt_pack(enc_key, t_res.key_image)

        ki_bin = decr[:32]
        ki = crypto.decodepoint(ki_bin)
        sig = [[crypto.decodeint(decr[32:64]), crypto.decodeint(decr[64:])]]

        if not ring_ct.check_ring_singature(
            ki_bin, ki, [crypto.decodepoint(out_key)], sig
        ):
            raise ValueError("Invalid ring sig on KI")

        return ki

    @staticmethod
    def _compute_ki_enc_key_host(view_key_private, prefix, salt):
        passwd = crypto.keccak_2hash(crypto.encodeint(view_key_private) + prefix)
        enc_key = crypto.compute_hmac(salt, passwd)
        return enc_key
