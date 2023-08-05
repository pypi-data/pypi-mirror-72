#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018


import os
import logging

from trezorlib import ui
from trezorlib.debuglink import TrezorClientDebugLink

from monero_glue.hwtoken import token
from monero_glue.protocol_base.messages import MessageConverter

from trezorlib.client import TrezorClient
from trezorlib.transport import enumerate_devices, get_transport


logger = logging.getLogger(__name__)


class TrezorSession(object):
    def __init__(self, client, **kwargs):
        self.client = client

    def __enter__(self):
        self.client.open()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class Trezor(token.TokenLite):
    """
    Trezor proxy calls to the trezor
    """

    def __init__(
        self, path=None, debug=False, address_n=None, network_type=0, *args, **kwargs
    ):
        super().__init__()
        if path is None:
            path = os.environ.get("TREZOR_PATH", "udp:127.0.0.1:21324")

        self.debug = debug
        self.path = path
        self.msg_conv = MessageConverter(fix_bytes=True)
        self._connect()

    def _connect(self):
        self.wirelink = get_transport(self.path)
        self.client = (
            TrezorClientDebugLink(self.wirelink)
            if self.debug
            else TrezorClient(self.wirelink, ui=ui.ClickUI())
        )

        # if self.debug:
        #     try:
        #         self.debuglink = self.wirelink.find_debug()
        #         self.client.set_debuglink(self.debuglink)
        #     except Exception as e:
        #         logger.warning(e)

    def _to_tlib(self, msg):
        return self.msg_conv.to_trezorlib(msg)

    def _from_tlib(self, msg):
        return self.msg_conv.to_phlib(msg)

    @staticmethod
    def enumerate():
        return enumerate_devices()

    def reconnect(self):
        self._connect()

    def close(self):
        self.client.close()

    def session(self):
        return TrezorSession(self.client)

    async def call(self, msg, recode=True):
        with self.session():
            return await self.call_in_session(msg, recode)

    async def call_in_session(self, msg, recode=True):
        if recode:
            msg = self._to_tlib(msg)

        res = self.client.call(msg)

        if recode:
            res = self._from_tlib(res)
        return res

    async def ping(self, message=None, **kwargs):
        with self.session():
            return self.client.ping(message if message else "monero", **kwargs)

    async def get_view_key(self, msg):
        with self.session():
            res = self.client.call(self._to_tlib(msg))
            return self._from_tlib(res)

    async def tsx_sign(self, msg):
        with self.session():
            res = self.client.call(self._to_tlib(msg))
            return self._from_tlib(res)

    async def key_image_sync(self, msg, *args, **kwargs):
        with self.session():
            res = self.client.call(self._to_tlib(msg))
            return self._from_tlib(res)

    async def get_tx_key(self, msg, *args, **kwargs):
        with self.session():
            res = self.client.call(self._to_tlib(msg))
            return self._from_tlib(res)

    async def live_refresh(self, msg, *args, **kwargs):
        with self.session():
            res = self.client.call(self._to_tlib(msg))
            return self._from_tlib(res)
