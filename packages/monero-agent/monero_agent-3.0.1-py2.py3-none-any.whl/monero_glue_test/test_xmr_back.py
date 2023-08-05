#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import unittest

from monero_glue.xmr.core.backend import ed25519


class Basetest(unittest.TestCase):
    """Simple tests"""

    def __init__(self, *args, **kwargs):
        super(Basetest, self).__init__(*args, **kwargs)

    def test_ed25519(self):
        """
        Basic ED25519 invariants
        :return:
        """
        assert ed25519.b >= 10
        assert 8 * len(ed25519.H(b"hash input")) == 2 * ed25519.b
        assert pow(2, ed25519.q - 1, ed25519.q) == 1
        assert ed25519.q % 4 == 1
        assert pow(2, ed25519.l - 1, ed25519.l) == 1
        assert ed25519.l >= 2 ** (ed25519.b - 4)
        assert ed25519.l <= 2 ** (ed25519.b - 3)
        assert pow(ed25519.d, (ed25519.q - 1) // 2, ed25519.q) == ed25519.q - 1
        assert pow(ed25519.I, 2, ed25519.q) == ed25519.q - 1
        assert ed25519.isoncurve(ed25519.B)
        P = ed25519.scalarmult(ed25519.B, ed25519.l)
        assert ed25519.isoncurve(P)

    def test_ed25519_mult8(self):
        """
        Mult8 test vector
        :return:
        """
        p1 = ed25519.decodepoint(
            bytes(
                [
                    0x14,
                    0x9c,
                    0xe9,
                    0x3f,
                    0xd3,
                    0x1d,
                    0xf5,
                    0x44,
                    0x18,
                    0xa5,
                    0x29,
                    0x9b,
                    0x11,
                    0xdf,
                    0xc1,
                    0x4e,
                    0x48,
                    0xd1,
                    0x4a,
                    0x2a,
                    0x4c,
                    0xe9,
                    0x84,
                    0x0c,
                    0xf2,
                    0xff,
                    0x7c,
                    0x31,
                    0x83,
                    0xda,
                    0x89,
                    0x53,
                ]
            )
        )
        p2 = ed25519.decodepoint(
            bytes(
                [
                    0x25,
                    0x9e,
                    0xf2,
                    0xab,
                    0xa8,
                    0xfe,
                    0xb4,
                    0x73,
                    0xcf,
                    0x39,
                    0x05,
                    0x8a,
                    0x0f,
                    0xe3,
                    0x0b,
                    0x9f,
                    0xf6,
                    0xd2,
                    0x45,
                    0xb4,
                    0x2b,
                    0x68,
                    0x26,
                    0x68,
                    0x7e,
                    0xbd,
                    0x6b,
                    0x63,
                    0x12,
                    0x8a,
                    0xff,
                    0x64,
                ]
            )
        )
        self.assertEqual(ed25519.scalarmult(p1, 8), p2)

    def test_ed25519_scalarmult(self):
        """
        Scalar mult test vector
        :return:
        """
        pub = bytes(
            [
                0x22,
                0x4f,
                0xad,
                0x08,
                0x5c,
                0x7c,
                0x8b,
                0xe0,
                0xc0,
                0x58,
                0x48,
                0x46,
                0xf7,
                0x88,
                0xd9,
                0x48,
                0x1e,
                0x53,
                0x53,
                0xfb,
                0xa7,
                0xbb,
                0xff,
                0x4d,
                0x24,
                0xb0,
                0xb8,
                0xbc,
                0x43,
                0xbb,
                0x66,
                0x6f,
            ]
        )
        scal = ed25519.decodeint(
            bytes(
                [
                    0x4c,
                    0xe8,
                    0x8c,
                    0x16,
                    0x8e,
                    0x0f,
                    0x5f,
                    0x8d,
                    0x65,
                    0x24,
                    0xf7,
                    0x12,
                    0xd5,
                    0xf8,
                    0xd7,
                    0xd8,
                    0x32,
                    0x33,
                    0xb1,
                    0xe7,
                    0xa2,
                    0xa6,
                    0x0b,
                    0x5a,
                    0xba,
                    0x52,
                    0x06,
                    0xcc,
                    0x0e,
                    0xa2,
                    0xbc,
                    0x08,
                ]
            )
        )

        res = ed25519.scalarmult(ed25519.decodepointcheck(pub), scal)
        res_h = ed25519.encodepoint(res)

        exp_mul = bytes(
            [
                0x14,
                0x9c,
                0xe9,
                0x3f,
                0xd3,
                0x1d,
                0xf5,
                0x44,
                0x18,
                0xa5,
                0x29,
                0x9b,
                0x11,
                0xdf,
                0xc1,
                0x4e,
                0x48,
                0xd1,
                0x4a,
                0x2a,
                0x4c,
                0xe9,
                0x84,
                0x0c,
                0xf2,
                0xff,
                0x7c,
                0x31,
                0x83,
                0xda,
                0x89,
                0x53,
            ]
        )

        self.assertEqual(res_h, exp_mul)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
