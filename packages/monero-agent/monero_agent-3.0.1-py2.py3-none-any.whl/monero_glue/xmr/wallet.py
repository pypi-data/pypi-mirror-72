#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import json
import re
import datetime
import logging

from monero_glue.xmr import common, crypto, monero
from monero_glue.xmr.enc import chacha
from monero_serialize import xmrboost, xmrjson, xmrrpc, xmrserialize, xmrtypes

logger = logging.getLogger(__name__)


UNSIGNED_TX_PREFIX = b"Monero unsigned tx set\004"
SIGNED_TX_PREFIX = b"Monero signed tx set\004"
MULTISIG_UNSIGNED_TX_PREFIX = b"Monero multisig unsigned tx set\001"
OUTPUTS_PREFIX = b"Monero output export\003"


class WalletKeyData(xmrtypes.WalletKeyData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.m_creation_timestamp = kwargs.pop("m_creation_timestamp", 0)
        self.m_keys = kwargs.pop("m_keys", None)  # type: xmrtypes.AccountKeys

    def to_json(self):
        return self.__dict__


class WalletKeyFile(object):
    def __init__(self, **kwargs):
        self.seed_language = kwargs.pop("seed_language", "English")
        self.watch_only = kwargs.pop("watch_only", 1)
        self.multisig = kwargs.pop("multisig", 0)
        self.multisig_threshold = kwargs.pop("multisig_threshold", 0)
        self.always_confirm_transfers = kwargs.pop("always_confirm_transfers", 1)
        self.print_ring_members = kwargs.pop("print_ring_members", 1)
        self.store_tx_info = kwargs.pop("store_tx_info", 1)
        self.default_mixin = kwargs.pop("default_mixin", 7)
        self.default_priority = kwargs.pop("default_priority", 7)
        self.auto_refresh = kwargs.pop("auto_refresh", 1)
        self.refresh_type = kwargs.pop("refresh_type", 1)
        self.refresh_height = kwargs.pop("refresh_height", 0)
        self.confirm_missing_payment_id = kwargs.pop("confirm_missing_payment_id", 1)
        self.ask_password = kwargs.pop("ask_password", 1)
        self.min_output_count = kwargs.pop("min_output_count", 0)
        self.min_output_value = kwargs.pop("min_output_value", 0)
        self.default_decimal_point = kwargs.pop("default_decimal_point", 12)
        self.merge_destinations = kwargs.pop("merge_destinations", 0)
        self.confirm_backlog = kwargs.pop("confirm_backlog", 1)
        self.confirm_backlog_threshold = kwargs.pop("confirm_backlog_threshold", 0)
        self.confirm_export_overwrite = kwargs.pop("confirm_export_overwrite", 1)
        self.auto_low_priority = kwargs.pop("auto_low_priority", 1)
        self.testnet = kwargs.pop("testnet", 0)
        self.key_data = kwargs.pop("key_data", None)

    def to_json(self):
        return self.__dict__


class ExportedOutputs(xmrserialize.ContainerType):
    BOOST_VERSION = 0
    ELEM_TYPE = xmrtypes.TransferDetails


class ExportedOutputsV4(xmrserialize.TupleType):
    BOOST_VERSION = 0
    MFIELDS = [
        xmrserialize.SizeT, ExportedOutputs,
    ]


class OutputsDump(object):
    def __init__(self, **kwargs):
        self.m_spend_public_key = kwargs.get("m_spend_public_key", None)
        self.m_view_public_key = kwargs.get("m_view_public_key", None)
        self.tds = kwargs.get("tds", None)


async def load_keys_file(file, password):
    """
    Load wallet keys file
    :param file:
    :param password:
    :return:
    """
    with open(file, "rb") as fh:
        data = fh.read()
    return await load_keys_data(data, password)


async def load_keys_data(data, password):
    """
    Loads wallet keys file passed as byte string
    :param file:
    :param password:
    :return:
    """
    reader = xmrserialize.MemoryReaderWriter(bytearray(data))
    ar = xmrserialize.Archive(reader, False)
    msg = xmrtypes.KeysFileData()
    await ar.message(msg)

    key = chacha.generate_key(password)
    buff = bytes(msg.iv + msg.account_data)
    dec = chacha.decrypt(key, buff)

    m = re.search(b'(.*)"key_data":"(.+?)",(.*)', dec)
    key_data = m.group(2)

    dat = xmrjson.unescape_json_str(key_data)
    reader = xmrserialize.MemoryReaderWriter(bytearray(dat))
    ar = xmrrpc.Archive(reader, False)

    key_data = {}
    await ar.root()
    await ar.section(key_data)

    rest_json = m.group(1) + m.group(3)
    wallet_key = json.loads(rest_json)
    wallet_key["key_data"] = key_data
    return wallet_key


async def save_keys_file(file, password, wkeyfile):
    """
    Stores the wallet key file

    :param file:
    :param password:
    :param wkeyfile:
    :type wkeyfile: WalletKeyFile
    :return:
    """
    data = await gen_keys_file(password, wkeyfile)
    with open(file, "wb") as fh:
        fh.write(data)


async def gen_keys_file(password, wkeyfile):
    """
    Generates wallet keys file as bytestring
    :param password:
    :param wkeyfile:
    :return:
    """
    key_data = wkeyfile.key_data  # type: WalletKeyData
    js = wkeyfile.to_json()
    del js["key_data"]

    # encode wallet key file wth classical json encoder, key data added later with monero encoding.
    enc = json.dumps(js, cls=xmrjson.AutoJSONEncoder)

    # key_data KV serialization. Message -> Model.
    modeler = xmrrpc.Modeler(writing=True, modelize=True)
    mdl = await modeler.message(msg=key_data)

    # Model -> binary
    writer = xmrserialize.MemoryReaderWriter()
    ar = xmrrpc.Archive(writer, True)

    await ar.root()
    await ar.section(mdl)
    ser = bytes(writer.get_buffer())

    ser2 = xmrjson.escape_string_json(ser)
    enc2 = b'{"key_data":"' + ser2 + b'",' + enc[1:].encode("utf8")

    key = chacha.generate_key(password)
    enc_enc = chacha.encrypt(key, enc2)

    writer = xmrserialize.MemoryReaderWriter()
    ar = xmrserialize.Archive(writer, True)
    msg = xmrtypes.KeysFileData()
    msg.iv = enc_enc[0:8]
    msg.account_data = enc_enc[8:]
    await ar.message(msg)

    return bytes(writer.get_buffer())


async def load_unsigned_tx(priv_key, data, hf=9):
    """
    Loads unsigned transaction from the encrypted file
    :param priv_key:
    :param data:
    :param hf:
    :return:
    """
    magic_len = len(UNSIGNED_TX_PREFIX)
    magic = data[: magic_len - 1]
    version = int(data[magic_len - 1])
    data = data[magic_len:]

    if magic != UNSIGNED_TX_PREFIX[:-1]:
        raise ValueError("Invalid file header")
    if version != 4:
        raise ValueError("Unsigned transaction v4 is supported only")

    tx_uns_ser = chacha.decrypt_xmr(priv_key, data, authenticated=True)

    reader = xmrserialize.MemoryReaderWriter(bytearray(tx_uns_ser))
    ar = xmrboost.Archive(reader, False, xmrtypes.hf_versions(hf))

    msg = xmrtypes.UnsignedTxSet()
    await ar.root()
    await ar.message(msg)
    return msg


async def dump_unsigned_tx(priv_key, unsigned_tx, hf=9):
    """
    Dumps unsigned transaction
    :param priv_key:
    :param unsigned_tx:
    :param hf:
    :return:
    """
    writer = xmrserialize.MemoryReaderWriter()
    ar = xmrboost.Archive(writer, True, xmrtypes.hf_versions(hf))
    await ar.root()
    await ar.message(unsigned_tx)

    ciphertext = chacha.encrypt_xmr(
        priv_key, bytes(writer.get_buffer()), authenticated=True
    )
    return UNSIGNED_TX_PREFIX + ciphertext


async def dump_signed_tx(priv_key, signed_tx):
    """
    Dumps signed_tx to a file as wallet produces

    :param priv_key:
    :param signed_tx:
    :return:
    """
    writer = xmrserialize.MemoryReaderWriter()
    ar = xmrboost.Archive(writer, True)
    try:
        await ar.root()
        await ar.message(signed_tx)
    except Exception as e:
        logger.error('Exception in signed tx serialization: %s, field: %s' % (e, ar.tracker))
        raise

    ciphertext = chacha.encrypt_xmr(
        priv_key, bytes(writer.get_buffer()), authenticated=True
    )
    return SIGNED_TX_PREFIX + ciphertext


def construct_pending_tsx(tx, cd):
    """
    Dummy pending transaction record from real transaction + construction data.
    Tx key is not sent to untrusted wallet.
    Same logic as in wallet2.cpp:sign_tx

    :param tx:
    :param cd:
    :return:
    """
    pending = xmrtypes.PendingTransaction(
        tx=tx,
        dust=0,
        fee=0,
        dust_added_to_fee=False,
        change_dts=cd.change_dts,
        selected_transfers=cd.selected_transfers,
        key_images="",
        tx_key=crypto.identity(True),
        additional_tx_keys=[],
        dests=cd.dests,
        multisig_sigs=[],
        construction_data=cd,
    )
    return pending


def conv_disp_amount(amount):
    """
    Monero uint64 to display val.
    :param amount:
    :return:
    """
    return amount / float(10 ** monero.DISPLAY_DECIMAL_POINT)


async def load_exported_outputs(priv_key, data):
    """
    Loads exported outputs file
    :param data:
    :return:
    """
    magic_len = len(OUTPUTS_PREFIX)
    magic = data[: magic_len - 1]
    version = int(data[magic_len - 1])
    data = data[magic_len:]

    if magic != OUTPUTS_PREFIX[:-1]:
        raise ValueError("Invalid file header")
    if version not in [3, 4]:
        raise ValueError("Exported outputs v3, v4 are supported only")
    msg_to_parse = ExportedOutputsV4 if version == 4 else ExportedOutputs

    data_dec = chacha.decrypt_xmr(priv_key, data, authenticated=True)

    spend_pub = data_dec[:32]
    view_pub = data_dec[32:64]
    data_dec = data_dec[64:]

    reader = xmrserialize.MemoryReaderWriter(bytearray(data_dec))
    ar = xmrboost.Archive(reader, False)

    await ar.root()
    if version == 3:
        exps = await ar.container(container_type=ExportedOutputs)
    elif version == 4:
        exps_root = await ar.tuple(elem_type=ExportedOutputsV4)
        exps = exps_root[1]
        if exps_root[0] != 0:
            raise ValueError('Offset has to be 0')

    return OutputsDump(
        m_spend_public_key=spend_pub, m_view_public_key=view_pub, tds=exps
    )


async def save_exported_outputs(priv_spend, priv_view, transfers):
    writer = xmrserialize.MemoryReaderWriter()
    ar = xmrboost.Archive(writer, True)

    await ar.root()
    await ar.container(transfers, container_type=ExportedOutputs)
    trans_bin = writer.get_buffer()

    buff_dec = bytearray()
    buff_dec += crypto.encodepoint(crypto.scalarmult_base(priv_spend))
    buff_dec += crypto.encodepoint(crypto.scalarmult_base(priv_view))
    buff_dec += trans_bin

    data_enc = chacha.encrypt_xmr(priv_view, buff_dec, authenticated=True)
    return bytearray(bytes(OUTPUTS_PREFIX) + data_enc)


class Wallet(object):
    def __init__(self, daemon_rpc=None):
        self.daemon_rpc = daemon_rpc

    async def parse_block(self, bindata):
        reader = xmrserialize.MemoryReaderWriter(bytearray(bindata))
        ar = xmrserialize.Archive(reader, False)
        return await ar.message(None, xmrtypes.Block)

    async def get_height(self):
        return int((await self.daemon_rpc.get_info())["height"])

    async def get_blockchain_height_by_date(self, year, month, day):
        dt = datetime.datetime(year=year, month=month, day=day)
        timestamp = dt.replace(tzinfo=datetime.timezone.utc).timestamp()

        height_min = 0
        height_max = await self.get_height() - 1
        while True:
            height_mid = (height_min + height_max) // 2
            heights = [height_min, height_mid, height_max]
            blocks = await self.daemon_rpc.get_blocks_by_height(heights)

            blk_min = await self.parse_block(blocks["blocks"][0]["block"])
            blk_mid = await self.parse_block(blocks["blocks"][1]["block"])
            blk_max = await self.parse_block(blocks["blocks"][2]["block"])

            t_min = int(blk_min.timestamp)
            t_mid = int(blk_mid.timestamp)
            t_max = int(blk_max.timestamp)

            if not (t_min <= t_mid and t_mid <= t_max):
                return min(heights)

            if timestamp > t_max:
                raise ValueError("Specified date is in the future")

            if timestamp <= t_min + 2 * 24 * 60 * 60:
                return height_min

            if timestamp <= t_mid:
                height_max = height_mid
            else:
                height_min = height_mid

            if height_max - height_min <= 2 * 24 * 30:
                return height_min
