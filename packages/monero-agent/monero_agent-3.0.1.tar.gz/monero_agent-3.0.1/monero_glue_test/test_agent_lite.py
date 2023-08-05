#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import binascii
import os
import unittest
import zlib

from monero_serialize import xmrboost, xmrserialize, xmrtypes

from monero_glue.agent import agent_lite
from monero_glue.hwtoken import token
from monero_glue.xmr import crypto, monero, wallet
from monero_glue_test.base_agent_test import BaseAgentTest


class AgentLiteTest(BaseAgentTest):
    """Simple tests"""

    def __init__(self, *args, **kwargs):
        super(AgentLiteTest, self).__init__(*args, **kwargs)

    async def test_tx_sign_simple(self):
        """
        Testing tx signature, simple, multiple inputs
        :return:
        """
        unsigned_tx_c = self.get_data_file("tsx_uns01.txt")
        unsigned_tx = zlib.decompress(binascii.unhexlify(unsigned_tx_c))
        await self.tx_sign_unsigned(unsigned_tx, "tsx_uns01.txt")

    async def test_tx_sign(self):
        """
        Testing tx signature, one input. non-simple RCT
        :return:
        """
        unsigned_tx_c = self.get_data_file("tsx_uns02.txt")
        unsigned_tx = zlib.decompress(binascii.unhexlify(unsigned_tx_c))
        await self.tx_sign_unsigned(unsigned_tx, "tsx_uns02.txt")

    async def test_tx_sign_sub_dest(self):
        """
        Testing tx signature, one input. non-simple RCT
        :return:
        """
        unsigned_tx_c = self.get_data_file("tsx_uns03.txt")
        unsigned_tx = zlib.decompress(binascii.unhexlify(unsigned_tx_c))
        await self.tx_sign_unsigned(unsigned_tx, "tsx_uns03.txt")

    async def test_tx_sign_sub_2dest(self):
        """
        Testing tx signature, one input. non-simple RCT
        :return:
        """
        unsigned_tx_c = self.get_data_file("tsx_uns04.txt")
        unsigned_tx = zlib.decompress(binascii.unhexlify(unsigned_tx_c))
        await self.tx_sign_unsigned(unsigned_tx, "tsx_uns04.txt")

    async def test_tx_sign_pending01_boost_full_2dest(self):
        """
        Testing tx signature, one input. full RCT, boost serialized
        :return:
        """
        pending_hex = self.get_data_file("tsx_pending01.txt")
        pending_bin = binascii.unhexlify(pending_hex)
        await self.tx_sign_pending_boost(pending_bin, "tsx_pending01.txt")

    async def test_tx_sign_pending02_boost_full_sub_3dest(self):
        """
        Testing tx signature, one input. full RCT, boost serialized
        :return:
        """
        pending_hex = self.get_data_file("tsx_pending02.txt")
        pending_bin = binascii.unhexlify(pending_hex)
        await self.tx_sign_pending_boost(pending_bin, "tsx_pending02.txt")

    async def test_tx_sign_uns01_boost_full_2dest(self):
        """
        Testing tx signature, one input. full RCT, boost serialized
        :return:
        """
        self.skipTest('Boost test skipped, wallet regeneration needed (SLIP-0010 change)')
        unsigned_tx_c = self.get_data_file("tsx_uns_enc01.txt")
        creds = self.get_creds()
        unsigned_tx = await wallet.load_unsigned_tx(
            creds.view_key_private, unsigned_tx_c
        )
        await self.tx_sign_unsigned_msg(unsigned_tx, "tsx_uns_enc01.txt")

    async def test_tx_sign_uns01_boost_full_2dest_sub(self):
        """
        Testing tx signature, one input. full RCT, boost serialized
        :return:
        """
        self.skipTest('Boost test skipped, wallet regeneration needed (SLIP-0010 change)')
        unsigned_tx_c = self.get_data_file("tsx_uns_enc02.txt")
        creds = self.get_creds()
        unsigned_tx = await wallet.load_unsigned_tx(
            creds.view_key_private, unsigned_tx_c
        )
        await self.tx_sign_unsigned_msg(unsigned_tx, "tsx_uns_enc02.txt")

    async def test_trezor_ki(self):
        creds = self.get_trezor_creds(0)
        ki_data = self.get_data_file("ki_sync_01.txt")
        ki_loaded = await wallet.load_exported_outputs(
            creds.view_key_private, ki_data
        )

        self.assertEqual(ki_loaded.m_spend_public_key, crypto.encodepoint(creds.spend_key_public))
        self.assertEqual(ki_loaded.m_view_public_key, crypto.encodepoint(creds.view_key_public))

        tagent = self.init_agent(creds=creds)
        res = await tagent.import_outputs(ki_loaded.tds)
        await self.verify_ki_export(res, ki_loaded)

    async def test_trezor_txs_bp_c1_hf10(self):
        if not crypto.get_backend().has_rangeproof_bulletproof():
            self.skipTest('Crypto backend does not support BPs')
        await self._int_test_trezor_txs(as_bulletproof=True, client_version=1, hf=10)

    async def _int_test_trezor_txs(self, as_bulletproof=False, client_version=1, hf=10):
        if os.getenv('SKIP_TREZOR_TSX', False):
            self.skipTest('Skipped by ENV var')

        files = self.get_trezor_tsx_tests()
        creds = self.get_trezor_creds(0)
        all_creds = self.get_all_trezor_creds()

        if not os.getenv('FORCE_ALL_TESTS', False) and not crypto.get_backend().is_fast():
            files = files[0:3]

        for fl in files:
            with self.subTest(msg=fl):
                unsigned_tx_c = self.get_data_file(fl)
                unsigned_tx = await wallet.load_unsigned_tx(
                    creds.view_key_private, unsigned_tx_c
                )

                for tx in unsigned_tx.txes:
                    if as_bulletproof:
                        tx.use_rct = False
                        tx.use_bulletproofs = True

                tagent = self.init_agent(creds=creds)
                tagent.client_version = client_version
                tagent.hf = hf
                await self.tx_sign_test(tagent, unsigned_tx, creds, all_creds, fl)

    async def tx_sign_unsigned_msg(self, unsigned_tx, fl=None):
        """
        Signs tx stored in unsigned tx message
        :param unsigned_tx:
        :param fl:
        :return:
        """
        self.skipTest('HP <= 8 not supported anymore')
        tagent = self.init_agent()
        await self.tx_sign_test(tagent, unsigned_tx, self.get_creds(), self.get_all_creds(), fl)

    def _get_bc_ver(self):
        """
        Returns version settings for the used data. Testing data are fixed at these versions.
        :return:
        """
        return xmrtypes.hf_versions(9)

    async def tx_sign_unsigned(self, unsigned_tx, fl=None):
        """
        Tx sign test with given unsigned transaction data
        :param unsigned_tx:
        :param fl:
        :return:
        """
        self.skipTest('HP <= 8 not supported anymore')
        reader = xmrserialize.MemoryReaderWriter(bytearray(unsigned_tx))
        ar = xmrserialize.Archive(reader, False, self._get_bc_ver())
        unsig = xmrtypes.UnsignedTxSet()
        await ar.message(unsig)
        await self.tx_sign_unsigned_msg(unsig, fl)

    async def tx_sign_unsigned_boost(self, unsigned_tx, fl=None):
        """
        Tx sign test with given unsigned transaction data, serialized by boost -
        unsigned tx produced by watch-only cli wallet.

        :param unsigned_tx:
        :param fl:
        :return:
        """
        self.skipTest('HP <= 8 not supported anymore')
        reader = xmrserialize.MemoryReaderWriter(bytearray(unsigned_tx))
        ar = xmrboost.Archive(reader, False)
        unsig = xmrtypes.UnsignedTxSet()
        await ar.root()
        await ar.message(unsig)
        await self.tx_sign_unsigned_msg(unsig, fl)

    async def tx_sign_pending_boost(self, pending_tx, fl=None):
        """
        Signs transaction produced by the wallet-rpc, metadata parser, boost
        :param metadata:
        :param fl:
        :return:
        """
        self.skipTest('HP <= 8 not supported anymore')
        reader = xmrserialize.MemoryReaderWriter(bytearray(pending_tx))
        ar = xmrboost.Archive(reader, False)
        pending = xmrtypes.PendingTransaction()
        await ar.root()
        await ar.message(pending)

        tagent = self.init_agent()
        await self.tx_sign_test(tagent, pending.construction_data, self.get_creds(), self.get_all_creds(), fl, sign_tx=True)

    def init_trezor(self, creds=None):
        """
        Initialize new trezor instance
        :type creds: object
        :return:
        """
        trez = token.TokenLite()
        trez.creds = self.get_creds() if creds is None else creds
        return trez

    def init_agent(self, creds=None):
        """
        Initialize new agent instance
        :return:
        """
        return agent_lite.Agent(self.init_trezor(creds=creds))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
