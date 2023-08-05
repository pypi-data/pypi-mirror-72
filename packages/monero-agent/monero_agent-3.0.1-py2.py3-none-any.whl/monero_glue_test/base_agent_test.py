#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import os
import binascii
import collections
import aiounittest
import pkg_resources
from monero_serialize.xmrtypes import RctType

from monero_glue.messages import MoneroRctKeyPublic
from monero_glue.xmr import crypto, monero, ring_ct, common, mlsag2
from monero_glue.hwtoken import misc
from monero_serialize import xmrserialize, xmrtypes

from monero_glue.xmr.enc import chacha_poly
from monero_glue.xmr.sub.addr import get_change_addr_idx
from monero_glue.xmr.sub.seed import SeedDerivation


class BaseAgentTest(aiounittest.AsyncTestCase):

    def get_trezor_mnemonics(self):
        return [
            'permit universe parent weapon amused modify essay borrow tobacco budget '
            'walnut lunch consider gallery ride amazing frog forget treat market '
            'chapter velvet useless topple',

            'permit permit parent weapon amused modify essay borrow tobacco budget '
            'walnut lunch consider gallery ride amazing frog forget treat market '
            'chapter velvet useless topple',

            'permit permit permit weapon amused modify essay borrow tobacco budget '
            'walnut lunch consider gallery ride amazing frog forget treat market '
            'chapter velvet useless topple',
        ]

    def get_trezor_creds(self, idx, slip0010=True):
        sd = SeedDerivation.from_mnemonics(self.get_trezor_mnemonics()[idx], slip0010=slip0010)
        return sd.creds(monero.NetworkTypes.TESTNET)

    def get_all_trezor_creds(self):
        return [
            self.get_trezor_creds(0),
            self.get_trezor_creds(0, False),
            self.get_trezor_creds(1),
            self.get_trezor_creds(1, False),
            self.get_trezor_creds(2),
            self.get_trezor_creds(2, False)
        ]

    def get_all_creds(self):
        return [
            self.get_creds_old(),
            self.get_creds_old2(),
            self.get_creds(),
            self.get_creds_01(),
            self.get_creds_02()
        ]

    def get_creds_old(self):
        """
        Wallet credentials
        :return:
        """
        return monero.AccountCreds.new_wallet(
            priv_view_key=crypto.b16_to_scalar(
                b"4ce88c168e0f5f8d6524f712d5f8d7d83233b1e7a2a60b5aba5206cc0ea2bc08"
            ),
            priv_spend_key=crypto.b16_to_scalar(
                b"f2644a3dd97d43e87887e74d1691d52baa0614206ad1b0c239ff4aa3b501750a"
            ),
            network_type=monero.NetworkTypes.TESTNET,
        )

    def get_creds_old2(self):
        """
        Wallet credentials
        :return:
        """
        return monero.AccountCreds.new_wallet(
            priv_view_key=crypto.b16_to_scalar(
                b"6b8a47bdc2bd9923b1684abdbbed56a4e834b101011e4c28585ae1d01281030d"
            ),
            priv_spend_key=crypto.b16_to_scalar(
                b"85148a19717a505fe4fc84219a79c4b4fdc35772ecb03b71385dc6572845d809"
            ),
            network_type=monero.NetworkTypes.TESTNET,
        )

    def get_creds(self):
        """
        Wallet credentials
        :return:
        """
        return monero.AccountCreds.new_wallet(  # slip0010
            priv_view_key=crypto.b16_to_scalar(
                b"a6ccd4ac344a295d1387f8d18c81bdd394f1845de84188e204514ef9370fd403"
            ),
            priv_spend_key=crypto.b16_to_scalar(
                b"14821d0bc5659b24cafbc889dc4fc60785ee08b65d71c525f81eeaba4f3a570f"
            ),
            network_type=monero.NetworkTypes.TESTNET,
        )

    def get_creds_01(self):
        """
        Wallet 02 credentials
        :return:
        """
        return monero.AccountCreds.new_wallet(
            priv_view_key=crypto.b16_to_scalar(
                b"42ba20adb337e5eca797565be11c9adb0a8bef8c830bccc2df712535d3b8f608"
            ),
            priv_spend_key=crypto.b16_to_scalar(
                b"b0ef6bd527b9b23b9ceef70dc8b4cd1ee83ca14541964e764ad23f5151204f0f"
            ),
            network_type=monero.NetworkTypes.TESTNET,
        )

    def get_creds_02(self):
        """
        Wallet 01 credentials
        :return:
        """
        return monero.AccountCreds.new_wallet(
            priv_view_key=crypto.b16_to_scalar(
                b"9e7aba8ae9ee134e5d5464d9145a4db26793d7411af7d06f20e755cb2a5ad50f"
            ),
            priv_spend_key=crypto.b16_to_scalar(
                b"283d8bab1aeaee8f8b5aed982fc894c67d3e03db9006e488321c053f5183310d"
            ),
            network_type=monero.NetworkTypes.TESTNET,
        )

    def get_trezor_tsx_tests(self):
        # return [('tsx_t_uns_%02d.txt' % i) for i in [1,4,8,14,16,17]]
        return [('tsx_t_uns_%02d.txt' % i) for i in range(1, 19)] \
               + [('tsx_t_uns_%02d_sub.txt' % i) for i in [8, 12]] \
               + [('tsx_t_uns_%02d_sub_add.txt' % i) for i in [8, 12]]

    def get_trezor_tsx_tests_heavy(self):
        return [
            'tsx_t_uns_08_sub_mix11_inp32_out16.txt',
            'tsx_t_uns_08_sub_mix11_inp64_out16.txt',
            'tsx_t_uns_08_sub_mix11_inp128_out16.txt',
            'tsx_t_uns_08_sub_mix11_inp256_out16.txt',

            'tsx_t_uns_08_sub_mix19_inp32_out16.txt',
            'tsx_t_uns_08_sub_mix19_inp64_out16.txt',

            'tsx_t_uns_08_sub_mix49_inp32_out16.txt',
            'tsx_t_uns_08_sub_mix49_inp64_out16.txt',

            'tsx_t_uns_08_sub_mix99_inp32_out16.txt',
            'tsx_t_uns_08_sub_mix99_inp64_out16.txt',

            'tsx_t_uns_08_sub_mix19_inp128_out16.txt',
            'tsx_t_uns_08_sub_mix19_inp256_out16.txt',

            'tsx_t_uns_08_sub_mix49_inp128_out16.txt',
            'tsx_t_uns_08_sub_mix49_inp256_out16.txt',

            'tsx_t_uns_08_sub_mix99_inp128_out16.txt',
            'tsx_t_uns_08_sub_mix99_inp256_out16.txt',
        ]

    def get_data_file(self, fl):
        return pkg_resources.resource_string(
            __name__, os.path.join("data", fl)
        )

    async def verify_ki_export(self, res, exp):
        """
        Verifies key image export
        :param res:
        :param exp:
        :return:
        """
        self.assertTrue(len(res) > 0)
        for idx, kie in enumerate(res):
            td = exp.tds[idx]
            ki = crypto.decodepoint(kie[0])
            pkey = crypto.decodepoint(td.m_tx.vout[td.m_internal_output_index].target.key)
            sig = [[crypto.decodeint(kie[1][0]), crypto.decodeint(kie[1][1])]]
            self.assertTrue(ring_ct.check_ring_singature(kie[0], ki, [pkey], sig))

    def get_expected_payment_id(self, fl):
        """
        Expected payment id type, data for file name
        :param fl:
        :return:
        """
        if fl is None:
            return None

        bname = os.path.basename(fl)
        if bname in ['tsx_t_uns_12.txt', 'tsx_t_uns_13.txt', 'tsx_t_uns_14.txt', 'tsx_t_uns_15.txt']:
            return 1, binascii.unhexlify('deadc0dedeadc0de')
        elif bname in ['tsx_t_uns_16.txt', ]:
            return 0, binascii.unhexlify('e8ce72659fbde7cc7c44871ca7784bba24b57323e66f7384ab06f2b8eea40649')
        elif bname in ['tsx_uns01.txt', 'tsx_uns02.txt', 'tsx_uns03.txt']:
            return 1, binascii.unhexlify('deadc0dedeadc0d1')
        elif bname in ['tsx_pending01.txt', ]:
            return 1, binascii.unhexlify('2f3413399032aeea')
        else:
            return None

    async def tx_sign_test(self, agent, con_data, creds, all_creds, fl, sign_tx=False):
        """
        General transaction signer / tester
        :param agent:
        :param con_data:
        :param creds:
        :param all_creds:
        :param fl:
        :param sign_tx ca:
        :return:
        """
        if not sign_tx:
            txes = await agent.sign_unsigned_tx(con_data)
        else:
            txes = await agent.sign_tx(con_data)

        await self.verify(txes[0], agent.last_transaction_data(), creds=creds)
        await self.receive(txes[0], all_creds, agent.last_transaction_data(), self.get_expected_payment_id(fl))

        if os.getenv('TREZOR_TEST_GET_TX'):
            await self.get_tx_key_test(agent, agent.last_transaction_data(), creds, all_creds)

    async def verify(self, tx, con_data=None, creds=None):
        """
        Transaction verification
        :param tx:
        :param con_data:
        :param creds:
        :return:
        """

        # Unserialize the transaction
        tx_obj = xmrtypes.Transaction()
        reader = xmrserialize.MemoryReaderWriter(bytearray(tx))
        ar1 = xmrserialize.Archive(reader, False)

        await ar1.message(tx_obj, msg_type=xmrtypes.Transaction)
        extras = await monero.parse_extra_fields(tx_obj.extra)
        monero.expand_transaction(tx_obj)

        tx_pub = crypto.decodepoint(monero.find_tx_extra_field_by_type(
            extras, xmrtypes.TxExtraPubKey
        ).pub_key)

        additional_pub_keys = monero.find_tx_extra_field_by_type(
            extras, xmrtypes.TxExtraAdditionalPubKeys
        )
        additional_pub_keys = [crypto.decodepoint(x) for x in additional_pub_keys.data] if additional_pub_keys is not None else None

        # Verify range proofs
        out_idx = 0
        is_bp = tx_obj.rct_signatures.type in [RctType.Bulletproof, RctType.Bulletproof2]
        if not is_bp:
            for idx, rsig in enumerate(tx_obj.rct_signatures.p.rangeSigs):
                out_pk = tx_obj.rct_signatures.outPk[idx]
                C = crypto.decodepoint(out_pk.mask)
                rsig = tx_obj.rct_signatures.p.rangeSigs[idx]
                res = ring_ct.ver_range(C, rsig, use_bulletproof=is_bp)
                self.assertTrue(res, "Invalid Range proof")

        else:
            for idx, rsig in enumerate(tx_obj.rct_signatures.p.bulletproofs):
                rsig_num_outs = min(len(tx_obj.rct_signatures.outPk), 1 << (len(rsig.L) - 6))
                outs = tx_obj.rct_signatures.outPk[out_idx : out_idx + rsig_num_outs]
                rsig.V = [crypto.encodepoint(ring_ct.bp_comm_to_v(crypto.decodepoint(xx.mask))) for xx in outs]
                res = ring_ct.ver_range(None, rsig, use_bulletproof=is_bp)
                self.assertTrue(res, "Invalid Range proof")

        # Prefix hash
        prefix_hash = await monero.get_transaction_prefix_hash(tx_obj)
        is_simple = len(tx_obj.vin) > 1 or is_bp

        self.assertEqual(prefix_hash, con_data.tx_prefix_hash)
        tx_obj.rct_signatures.message = prefix_hash

        # MLSAG hash
        mlsag_hash = await monero.get_pre_mlsag_hash(tx_obj.rct_signatures)

        # Decrypt transaction key
        tx_key = misc.compute_tx_key(creds.spend_key_private, prefix_hash, salt=con_data.enc_salt1, rand_mult=con_data.enc_salt2)[0]
        key_buff = chacha_poly.decrypt_pack(tx_key, con_data.enc_keys)

        tx_priv_keys = [crypto.decodeint(x) for x in common.chunk(key_buff, 32) if x]
        tx_priv = tx_priv_keys[0]
        tx_additional_priv = tx_priv_keys[1:]

        # Verify mlsag signature
        monero.recode_msg(tx_obj.rct_signatures.p.MGs, encode=False)
        for idx in range(len(tx_obj.vin)):
            if is_simple:
                mix_ring = [MoneroRctKeyPublic(dest=x[1].dest, commitment=x[1].mask) for x in con_data.tx_data.sources[idx].outputs]
                if is_bp:
                    pseudo_out = crypto.decodepoint(bytes(tx_obj.rct_signatures.p.pseudoOuts[idx]))
                else:
                    pseudo_out = crypto.decodepoint(bytes(tx_obj.rct_signatures.pseudoOuts[idx]))
                self.assertTrue(mlsag2.ver_rct_mg_simple(
                    mlsag_hash, tx_obj.rct_signatures.p.MGs[idx], mix_ring, pseudo_out
                ), "MG invalid")

            else:
                txn_fee_key = crypto.scalarmult_h(tx_obj.rct_signatures.txnFee)
                mix_ring = [[MoneroRctKeyPublic(dest=x[1].dest, commitment=x[1].mask)] for x in con_data.tx_data.sources[idx].outputs]
                self.assertTrue(mlsag2.ver_rct_mg(
                    tx_obj.rct_signatures.p.MGs[idx], mix_ring, tx_obj.rct_signatures.outPk, txn_fee_key, mlsag_hash
                ), "MG invalid")

    async def receive(self, tx, all_creds, con_data=None, exp_payment_id=None):
        """
        Test transaction receive with known view/spend keys of destinations.
        :param tx:
        :param all_creds:
        :param con_data:
        :param exp_payment_id:
        :return:
        """
        # Unserialize the transaction
        tx_obj = xmrtypes.Transaction()
        reader = xmrserialize.MemoryReaderWriter(bytearray(tx))
        ar1 = xmrserialize.Archive(reader, False)

        await ar1.message(tx_obj, msg_type=xmrtypes.Transaction)
        extras = await monero.parse_extra_fields(tx_obj.extra)
        tx_pub = monero.find_tx_extra_field_by_type(
            extras, xmrtypes.TxExtraPubKey
        ).pub_key
        additional_pub_keys = monero.find_tx_extra_field_by_type(
            extras, xmrtypes.TxExtraAdditionalPubKeys
        )
        num_outs = len(tx_obj.vout)
        num_received = 0

        # Try to receive tsx outputs with each account.
        tx_money_got_in_outs = collections.defaultdict(lambda: 0)
        outs = []

        change_idx = get_change_addr_idx(con_data.tsx_data.outputs, con_data.tsx_data.change_dts)
        received_idxs = []

        for idx, creds in enumerate(all_creds):
            wallet_subs = {}
            for account in range(0, 5):
                monero.compute_subaddresses(creds, account, range(25), wallet_subs)

            derivation = crypto.generate_key_derivation(
                crypto.decodepoint(tx_pub), creds.view_key_private
            )
            additional_derivations = []
            if additional_pub_keys and additional_pub_keys.data:
                for x in additional_pub_keys.data:
                    additional_derivations.append(
                        crypto.generate_key_derivation(
                            crypto.decodepoint(x), creds.view_key_private
                        )
                    )

            for ti, to in enumerate(tx_obj.vout):
                tx_scan_info = monero.check_acc_out_precomp(
                    to, wallet_subs, derivation, additional_derivations, ti
                )
                if not tx_scan_info.received:
                    continue

                received_idxs.append(ti)
                num_received += 1
                tx_scan_info = monero.scan_output(
                    creds, tx_obj, ti, tx_scan_info, tx_money_got_in_outs, outs, False
                )

                # Check spending private key correctness
                self.assertTrue(
                    crypto.point_eq(
                        crypto.decodepoint(tx_obj.rct_signatures.outPk[ti].mask),
                        crypto.gen_c(tx_scan_info.mask, tx_scan_info.amount),
                    ), "Invalid masks"
                )

                self.assertTrue(
                    crypto.point_eq(
                        crypto.decodepoint(tx_obj.vout[ti].target.key),
                        crypto.scalarmult_base(tx_scan_info.in_ephemeral),
                    ), "Invalid txin"
                )

                # payment ID
                payment_id = None
                payment_id_type = None
                extra_nonce = monero.find_tx_extra_field_by_type(extras, xmrtypes.TxExtraNonce)
                if extra_nonce and monero.has_encrypted_payment_id(extra_nonce.nonce):
                    payment_id_type = 1
                    payment_id = monero.get_encrypted_payment_id_from_tx_extra_nonce(extra_nonce.nonce)
                    payment_id = monero.encrypt_payment_id(payment_id, crypto.decodepoint(tx_pub), creds.view_key_private)

                elif extra_nonce and monero.has_payment_id(extra_nonce.nonce):
                    payment_id_type = 0
                    payment_id = monero.get_payment_id_from_tx_extra_nonce(extra_nonce.nonce)

                if exp_payment_id is not None:
                    # Not checking payment id for change transaction
                    if exp_payment_id[0] == 1 and change_idx is not None and ti == change_idx:
                        continue

                    self.assertEqual(payment_id_type, exp_payment_id[0])
                    self.assertEqual(payment_id, exp_payment_id[1])

        # All outputs have to be successfully received
        self.assertEqual(num_outs, num_received, 'Received only: %s' % received_idxs)

    def verify_tx_key(self, tx_priv, tx_pub, all_creds_subs):
        if crypto.point_eq(tx_pub, crypto.scalarmult_base(tx_priv)):
            return True
        for cred_idx, subs in enumerate(all_creds_subs):
            for ckey in subs:
                if crypto.point_eq(tx_pub, crypto.scalarmult(ckey, tx_priv)):
                    return True
        return False

    async def get_tx_key_test(self, agent, con_data, creds, all_creds):
        salt1 = con_data.enc_salt1
        salt2 = con_data.enc_salt2
        res = await agent.get_tx_key(salt1, salt2, con_data.enc_keys, con_data.tx_prefix_hash, creds.view_key_private)

        extras = await monero.parse_extra_fields(list(con_data.tx.extra))
        tx_pub = monero.find_tx_extra_field_by_type(extras, xmrtypes.TxExtraPubKey, 0)
        additional_pub_keys = monero.find_tx_extra_field_by_type(
            extras, xmrtypes.TxExtraAdditionalPubKeys
        )

        # For verification need to build database creds -> pubkeys
        all_creds_subs = []
        for idx, ccred in enumerate(all_creds):
            subs = {}
            for accnt in range(10):
                subs = monero.compute_subaddresses(ccred, accnt, range(20), subs)
            all_creds_subs.append([crypto.decodepoint(xx) for xx in subs.keys()])

        if not self.verify_tx_key(res[0], crypto.decodepoint(tx_pub.pub_key), all_creds_subs):
            raise ValueError("Tx pub mismatch")

        if additional_pub_keys and len(additional_pub_keys.data) != len(res) - 1:
            raise ValueError("Invalid additional keys count")

        if additional_pub_keys:
            for i, ad in enumerate(additional_pub_keys.data):
                if not self.verify_tx_key(res[i+1], crypto.decodepoint(ad), all_creds_subs):
                    raise ValueError("Tx additional %s pub mismatch" % i)

        my_pub = crypto.scalarmult_base(creds.view_key_private)
        res_der = await agent.get_tx_deriv(salt1, salt2, con_data.enc_keys, con_data.tx_prefix_hash, creds.view_key_private, crypto.encodepoint(my_pub))
        if len(res) != len(res_der):
            raise ValueError("Derivation array mismatch")
        tmp = crypto.scalarmult(my_pub, res[0])
        if not crypto.point_eq(tmp, res_der[0]):
            raise ValueError("Derivation 0 mismatch")

        if additional_pub_keys:
            for i in range(len(additional_pub_keys.data)):
                tmp = crypto.scalarmult(my_pub, res[i + 1])
                if not crypto.point_eq(tmp, res_der[i + 1]):
                    raise ValueError("Tx derivation additional %s mismatch" % i)
