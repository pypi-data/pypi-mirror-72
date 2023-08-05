#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import binascii
import struct

from monero_glue.misc import b58_mnr
from monero_glue.xmr import common, crypto, mlsag2, ring_ct
from monero_serialize import protobuf as xproto
from monero_serialize import xmrserialize, xmrtypes

from .sub.addr import *
from .sub.creds import *
from .sub.keccak_hasher import *
from .sub.mlsag_hasher import *
from .sub.recode import *
from .sub.recode_ext import *
from .sub.tsx_helper import *
from .sub.xmr_net import *
from typing import Tuple, List, Dict, Optional
from .crypto import Ge25519, Sc25519


Subaddresses = Dict[bytes, Tuple[int, int]]
DISPLAY_DECIMAL_POINT = 12


class XmrNoSuchAddressException(common.XmrException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TxScanInfo(object):
    """
    struct tx_scan_info_t
    """

    __slots__ = [
        "in_ephemeral",
        "ki",
        "mask",
        "amount",
        "money_transfered",
        "error",
        "received",
    ]


def get_subaddress_secret_key(secret_key: Sc25519, index=None, major=None, minor=None) -> Sc25519:
    """
    Builds subaddress secret key from the subaddress index
    Hs(SubAddr || a || index_major || index_minor)
    """
    if index:
        major = index.major
        minor = index.minor

    if major == 0 and minor == 0:
        return secret_key

    return crypto.get_subaddress_secret_key(secret_key, major, minor)


def get_subaddress_spend_public_key(view_private: Sc25519, spend_public: Ge25519, major, minor) -> Ge25519:
    """
    Generates subaddress spend public key D_{major, minor}
    """
    if major == 0 and minor == 0:
        return spend_public

    m = get_subaddress_secret_key(view_private, major=major, minor=minor)
    M = crypto.scalarmult_base(m)
    D = crypto.point_add(spend_public, M)
    return D


def derive_subaddress_public_key(out_key, derivation: Ge25519, output_index) -> Ge25519:
    """
    out_key - H_s(derivation || varint(output_index))G
    """
    crypto.check_ed25519point(out_key)
    scalar = crypto.derivation_to_scalar(derivation, output_index)
    point2 = crypto.scalarmult_base(scalar)
    point4 = crypto.point_sub(out_key, point2)
    return point4


def generate_key_image(public_key: Ge25519, secret_key: Sc25519) -> Ge25519:
    """
    Key image: secret_key * H_p(pub_key)
    """
    point = crypto.hash_to_point(public_key)
    point2 = crypto.scalarmult(point, secret_key)
    return point2


def is_out_to_acc_precomp(
    subaddresses: Subaddresses, out_key: Ge25519, derivation: Ge25519, additional_derivations: Optional[List[Ge25519]], output_index
) -> Optional[Tuple[Tuple[int, int], Ge25519]]:
    """
    Searches subaddresses for the computed subaddress_spendkey.
    If found, returns (major, minor), derivation.
    """
    subaddress_spendkey = crypto.encodepoint(
        derive_subaddress_public_key(out_key, derivation, output_index)
    )
    if subaddress_spendkey in subaddresses:
        return subaddresses[subaddress_spendkey], derivation

    if additional_derivations and len(additional_derivations) > 0:
        if output_index >= len(additional_derivations):
            raise ValueError("Wrong number of additional derivations")

        subaddress_spendkey = derive_subaddress_public_key(
            out_key, additional_derivations[output_index], output_index
        )
        subaddress_spendkey = crypto.encodepoint(subaddress_spendkey)
        if subaddress_spendkey in subaddresses:
            return (
                subaddresses[subaddress_spendkey],
                additional_derivations[output_index],
            )

    return None


def generate_key_image_helper_precomp(
    ack, out_key, recv_derivation, real_output_index, received_index
) -> Tuple[Sc25519, Ge25519]:
    """
    Generates UTXO spending key and key image.

    :param ack: sender credentials
    :type ack: AccountCreds
    :param out_key: real output (from input RCT) destination key
    :param recv_derivation:
    :param real_output_index:
    :param received_index: subaddress index this payment was received to
    :return: (spending private key, KI)
    """
    if not crypto.sc_isnonzero(ack.spend_key_private):
        raise ValueError("Watch-only wallet not supported")

    # derive secret key with subaddress - step 1: original CN derivation
    scalar_step1 = crypto.derive_secret_key(
        recv_derivation, real_output_index, ack.spend_key_private
    )

    # step 2: add Hs(SubAddr || a || index_major || index_minor)
    subaddr_sk = None
    scalar_step2 = None
    if received_index == (0, 0):
        scalar_step2 = scalar_step1
    else:
        subaddr_sk = get_subaddress_secret_key(
            ack.view_key_private, major=received_index[0], minor=received_index[1]
        )
        scalar_step2 = crypto.sc_add(scalar_step1, subaddr_sk)

    # when not in multisig, we know the full spend secret key, so the output pubkey can be obtained by scalarmultBase
    if len(ack.multisig_keys) == 0:
        pub_ver = crypto.scalarmult_base(scalar_step2)

    else:
        # When in multisig, we only know the partial spend secret key. But we do know the full spend public key,
        # so the output pubkey can be obtained by using the standard CN key derivation.
        pub_ver = crypto.derive_public_key(
            recv_derivation, real_output_index, ack.spend_key_public
        )

        # Add the contribution from the subaddress part
        if received_index != (0, 0):
            subaddr_pk = crypto.scalarmult_base(subaddr_sk)
            pub_ver = crypto.point_add(pub_ver, subaddr_pk)

    if not crypto.point_eq(pub_ver, out_key):
        raise ValueError(
            "key image helper precomp: given output pubkey doesn't match the derived one"
        )

    ki = generate_key_image(crypto.encodepoint(pub_ver), scalar_step2)
    return scalar_step2, ki


def generate_key_image_helper(
    creds,
    subaddresses,
    out_key: Ge25519,
    tx_public_key: Ge25519,
    additional_tx_public_keys,
    real_output_index,
) -> Tuple[Sc25519, Ge25519, Ge25519]:
    """
    Generates UTXO spending key and key image.
    Supports subaddresses.

    :param creds:
    :param subaddresses:
    :param out_key: real output (from input RCT) destination key
    :param tx_public_key: R, transaction public key
    :param additional_tx_public_keys: Additional Rs, for subaddress destinations
    :param real_output_index: index of the real output in the RCT
    :return: (private spending key, KI, recv_derivation)
    """
    recv_derivation = crypto.generate_key_derivation(
        tx_public_key, creds.view_key_private
    )

    additional_recv_derivations = []
    for add_pub_key in additional_tx_public_keys:
        additional_recv_derivations.append(
            crypto.generate_key_derivation(add_pub_key, creds.view_key_private)
        )

    subaddr_recv_info = is_out_to_acc_precomp(
        subaddresses,
        out_key,
        recv_derivation,
        additional_recv_derivations,
        real_output_index,
    )
    if subaddr_recv_info is None:
        raise XmrNoSuchAddressException()

    xi, ki = generate_key_image_helper_precomp(
        creds, out_key, subaddr_recv_info[1], real_output_index, subaddr_recv_info[0]
    )
    return xi, ki, recv_derivation


def check_acc_out_precomp(tx_out: Ge25519, subaddresses: Subaddresses, derivation: Ge25519, additional_derivations: Optional[List[Ge25519]], i) -> TxScanInfo:
    """
    wallet2::check_acc_out_precomp
    Detects whether the tx output belongs to the subaddresses. If yes, computes the derivation.
    Returns TxScanInfo

    :param tx_out:
    :param derivation:
    :param additional_derivations:
    :param i:
    :return:
    """
    tx_scan_info = TxScanInfo()
    tx_scan_info.error = True

    if not isinstance(tx_out.target, xmrtypes.TxoutToKey):
        return tx_scan_info

    tx_scan_info.received = is_out_to_acc_precomp(
        subaddresses,
        crypto.decodepoint(tx_out.target.key),
        derivation,
        additional_derivations,
        i,
    )
    if tx_scan_info.received:
        tx_scan_info.money_transfered = tx_out.amount
    else:
        tx_scan_info.money_transfered = 0
    tx_scan_info.error = False
    return tx_scan_info


def scan_output(creds, tx, i, tx_scan_info, tx_money_got_in_outs, outs, multisig):
    """
    Wallet2::scan_output()
    Computes spending key, key image, decodes ECDH info, amount, checks masks.
    """
    if multisig:
        tx_scan_info.in_ephemeral = 0
        tx_scan_info.ki = crypto.identity()

    else:
        out_dec = crypto.decodepoint(tx.vout[i].target.key)
        res = generate_key_image_helper_precomp(
            creds, out_dec, tx_scan_info.received[1], i, tx_scan_info.received[0]
        )
        tx_scan_info.in_ephemeral, tx_scan_info.ki = res
        if not tx_scan_info.ki:
            raise ValueError("Key error generation failed")

    outs.append(i)
    if tx_scan_info.money_transfered == 0:
        res2 = ecdh_decode_rv(tx.rct_signatures, tx_scan_info.received[1], i)
        tx_scan_info.money_transfered, tx_scan_info.mask = res2
        tx_scan_info.money_transfered = crypto.sc_get64(tx_scan_info.money_transfered)

    tx_money_got_in_outs[tx_scan_info.received[0]] += tx_scan_info.money_transfered
    tx_scan_info.amount = tx_scan_info.money_transfered
    return tx_scan_info


def ecdh_decode_rv(rv, derivation, i):
    """
    Decodes ECDH info from transaction.
    """
    scalar = crypto.derivation_to_scalar(derivation, i)
    if rv.type in [xmrtypes.RctType.Full, xmrtypes.RctType.Simple, xmrtypes.RctType.Bulletproof]:
        return ecdh_decode_simple(rv, scalar, i)

    elif rv.type in [xmrtypes.RctType.Bulletproof2]:
        return ecdh_decode_simple(rv, scalar, i, v2=True)

    else:
        raise ValueError("Unknown rv type")


def ecdh_decode_simple(rv, sk, i, v2=False):
    """
    Decodes ECDH from the transaction, checks mask (decoding validity).
    """
    if i >= len(rv.ecdhInfo):
        raise ValueError("Bad index")
    if len(rv.outPk) != len(rv.ecdhInfo):
        raise ValueError("outPk vs ecdhInfo mismatch")

    ecdh_info = rv.ecdhInfo[i]
    ecdh_info = recode_ecdh(ecdh_info, False)

    ecdh_info = ring_ct.ecdh_decode(ecdh_info, derivation=crypto.encodeint(sk), v2=v2)

    c_tmp = crypto.add_keys2(ecdh_info.mask, ecdh_info.amount, crypto.xmr_H())
    if not crypto.point_eq(c_tmp, crypto.decodepoint(rv.outPk[i].mask)):
        raise ValueError("Amount decoded incorrectly")

    return ecdh_info.amount, ecdh_info.mask


async def get_transaction_prefix_hash(tx):
    """
    Computes transaction prefix in one step
    """
    writer = get_keccak_writer()
    ar1 = xmrserialize.Archive(writer, True)
    await ar1.message(tx, msg_type=xmrtypes.TransactionPrefixExtraBlob)
    return writer.get_digest()


def expand_transaction(tx):
    """
    Expands transaction - recomputes fields not serialized.
    Recomputes only II, does not have access to the blockchain to get public keys for inputs
    for mix ring reconstruction.
    """
    rv = tx.rct_signatures
    if rv.type in [xmrtypes.RctType.Full]:
        rv.p.MGs[0].II = [None] * len(tx.vin)
        for n in range(len(tx.vin)):
            rv.p.MGs[0].II[n] = tx.vin[n].k_image

    elif rv.type in [
        xmrtypes.RctType.Simple,
        xmrtypes.RctType.FullBulletproof,
        xmrtypes.RctType.SimpleBulletproof,
    ]:
        if len(rv.p.MGs) != len(tx.vin):
            raise ValueError("Bad MGs size")
        for n in range(len(tx.vin)):
            rv.p.MGs[n].II = [tx.vin[n].k_image]

    else:
        raise ValueError("Unsupported rct tx type %s" % rv.type)

    return tx


def compute_subaddresses(creds, account, indices, subaddresses=None):
    """
    Computes subaddress public spend key for receiving transactions.

    :param creds: credentials
    :param account: major index
    :param indices: array of minor indices
    :param subaddresses: subaddress dict. optional.
    :return:
    """
    if subaddresses is None:
        subaddresses = {}

    for idx in indices:
        if account == 0 and idx == 0:
            subaddresses[crypto.encodepoint(creds.spend_key_public)] = (0, 0)
            continue

        pub = get_subaddress_spend_public_key(
            creds.view_key_private, creds.spend_key_public, major=account, minor=idx
        )
        pub = crypto.encodepoint(pub)
        subaddresses[pub] = (account, idx)
    return subaddresses


async def get_tx_pub_key_from_received_outs(td):
    """
    Extracts tx pub key from extras.
    Handles previous bug in Monero.

    :param td:
    :type td: xmrtypes.TransferDetails
    :return:
    """
    extras = await parse_extra_fields(list(td.m_tx.extra))
    tx_pub = find_tx_extra_field_by_type(extras, xmrtypes.TxExtraPubKey, 0)

    # Due to a previous bug, there might be more than one tx pubkey in extra, one being
    # the result of a previously discarded signature.
    # For speed, since scanning for outputs is a slow process, we check whether extra
    # contains more than one pubkey. If not, the first one is returned. If yes, they're
    # checked for whether they yield at least one output
    second_pub = find_tx_extra_field_by_type(extras, xmrtypes.TxExtraPubKey, 1)
    if second_pub is None:
        return tx_pub.pub_key

    # Workaround: resend all your funds to the wallet in a different transaction.
    # Proper handling would require derivation -> need trezor roundtrips.
    raise ValueError("Input transaction is buggy, contains two tx keys")


def generate_keys(recovery_key):
    """
    Wallet gen.
    :param recovery_key:
    :return:
    """
    pub = crypto.scalarmult_base(recovery_key)
    return recovery_key, pub


def generate_monero_keys(seed: Sc25519) -> Tuple[Sc25519, Ge25519, Sc25519, Ge25519]:
    """
    Generates spend key / view key from the seed in the same manner as Monero code does.

    account.cpp:
    crypto::secret_key account_base::generate(const crypto::secret_key& recovery_key, bool recover, bool two_random).
    :param seed:
    :return:
    """
    spend_sec, spend_pub = generate_keys(crypto.decodeint(seed))
    hash = crypto.cn_fast_hash(crypto.encodeint(spend_sec))
    view_sec, view_pub = generate_keys(crypto.decodeint(hash))
    return spend_sec, spend_pub, view_sec, view_pub


def generate_sub_address_keys(view_sec: Sc25519, spend_pub: Ge25519, major, minor) -> Tuple[Ge25519, Ge25519]:
    """
    Computes generic public sub-address
    :param view_sec:
    :param spend_pub:
    :param major:
    :param minor:
    :return: spend public, view public
    """
    if major == 0 and minor == 0:  # special case, Monero-defined
        return spend_pub, crypto.scalarmult_base(view_sec)

    m = get_subaddress_secret_key(view_sec, major=major, minor=minor)
    M = crypto.scalarmult_base(m)
    D = crypto.point_add(spend_pub, M)
    C = crypto.scalarmult(D, view_sec)
    return D, C


def commitment_mask(key, buff=None):
    """
    Generates deterministic commitment mask for Bulletproof2
    """
    data = bytearray(15 + 32)
    data[0:15] = b"commitment_mask"
    data[15:] = key
    if buff:
        return crypto.hash_to_scalar_into(buff, data)
    else:
        return crypto.hash_to_scalar(data)


def ecdh_hash(shared_sec):
    """
    Generates ECDH hash for amount masking for Bulletproof2
    """
    data = bytearray(38)
    data[0:6] = b"amount"
    data[6:] = shared_sec
    return crypto.cn_fast_hash(data)


def build_address_info(creds, subidx=None, payment_id=None, net_type=NetworkTypes.MAINNET):
    if (subidx is not None and subidx != (0, 0)) and payment_id:
        raise ValueError('Subaddress cannot be integrated')

    pub_spend, pub_view = creds.spend_key_public, creds.view_key_public
    if subidx:
        pub_spend, pub_view = generate_sub_address_keys(
            creds.view_key_private, creds.spend_key_public, subidx[0], subidx[1]
        )

    ai = AddrInfo()
    ai.spend_key = crypto.encodepoint(pub_spend)
    ai.view_key = crypto.encodepoint(pub_view)
    ai.payment_id = payment_id
    ai.net_type = net_type
    ai.is_integrated = payment_id is not None
    ai.is_sub_address = subidx is not None
    ai.recompute_addr()
    return ai
