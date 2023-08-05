#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Dusan Klinec, ph4r05, 2018

import ctypes as ct
import hmac

from Crypto.Protocol.KDF import PBKDF2
from monero_glue.xmr.core.ec_base import *
from trezor_crypto import trezor_cfunc as tcryr

# from monero_glue.misc.devel.call_tracker import CallTracker
# tcry = CallTracker(tcryr, print_on_end=True)
tcry = tcryr

ED25519_ORD = b"\xed\xd3\xf5\x5c\x1a\x63\x12\x58\xd6\x9c\xf7\xa2\xde\xf9\xde\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10"
ED25519_ORD_BN = None
Ge25519 = tcry.ge25519
Sc25519 = tcry.bignum256modm


# Load & init the library
tcry.open_lib()


def new_point():
    return tcry.new_ge25519()


def new_scalar():
    return tcry.init256_modm_r(0)


def random_bytes(by):
    """
    Generates X random bytes, returns byte-string
    :param by:
    :return:
    """
    return tcry.random_buffer_r(by)


class KeccakWrapper(object):
    """
    Simple Keccak hasher wrapper. OOP interface to xmr_hasher_*
    """

    digest_size = 32
    block_size = 136  # 1088 bits

    def __init__(self, h=None):
        self.h = tcry.xmr_hasher_init_r() if h is None else h

    def __repr__(self):
        return "<KeccakHash: %s>" % self.h

    def reset(self):
        self.h = tcry.xmr_hasher_init_r()
        return self

    def copy(self):
        h_copy = tcry.xmr_hasher_copy_r(self.h)
        return KeccakWrapper(h_copy)

    def update(self, s):
        tcry.xmr_hasher_update(self.h, bytes(s))

    def digest(self, buff=None):
        r = tcry.xmr_hasher_final_r(self.h)
        if buff:
            for i in range(len(r)):
                buff[i] = r[i]
            r = buff
        self.h = None
        return r

    def hexdigest(self):
        return self.digest().encode("hex")


def get_keccak(*args, **kwargs):
    """
    Simple keccak 256
    :return:
    """
    k = KeccakWrapper()
    if len(args) == 1:
        k.update(args[0])
    return k


def keccak_hash(inp):
    """
    Hashesh input in one call
    :return:
    """
    return tcry.xmr_fast_hash_r(bytes(inp))


def keccak_hash_into(r, inp, size=None):
    """
    Hashesh input in one call
    :return:point_add
    """
    bf = tcry.KEY_BUFF.from_buffer(r)
    tcry.cl().xmr_fast_hash(bf, bytes(inp), size if size else len(inp))
    return r


def keccak_2hash(inp):
    """
    Keccak double hashing
    :param inp:
    :return:
    """
    return keccak_hash(keccak_hash(inp))


def get_hmac(key, msg=None):
    """
    Returns HMAC object (uses Keccak256)
    :param key:
    :param msg:
    :return:
    """
    return hmac.new(key, msg=msg, digestmod=get_keccak)


def compute_hmac(key, msg=None):
    """
    Computes and returns HMAC of the msg using Keccak256
    :param key:
    :param msg:
    :return:
    """
    h = hmac.new(key, msg=msg, digestmod=get_keccak)
    return h.digest()


def pbkdf2(inp, salt, length=32, count=1000, prf=None):
    """
    PBKDF2 with default PRF as HMAC-KECCAK-256
    :param inp:
    :param salt:
    :param length:
    :param count:
    :param prf:
    :return:
    """

    if prf is None:
        prf = lambda p, s: hmac.new(p, msg=s, digestmod=get_keccak).digest()
    return PBKDF2(inp, salt, length, count, prf)


#
# EC
#


def _offset(x, offset=0):
    if offset == 0:
        return x
    return memoryview(x)[offset:]


def decodepoint(x, offset=0):
    return tcry.ge25519_unpack_vartime_r(tcry.KEY_BUFF(*_offset(x, offset)[:32]))


def decodepoint_into(r, x, offset=0):
    tcry.ge25519_unpack_vartime(r, tcry.KEY_BUFF(*_offset(x, offset)[:32]))
    return r


def encodepoint(pt):
    return tcry.ge25519_pack_r(pt)


def encodepoint_into(b, pt, offset=0):
    bf = tcry.KEY_BUFF.from_buffer(_offset(b, offset))
    tcry.ge25519_pack(bf, pt)
    return b


def decodeint(x, offset=0):
    return tcry.expand256_modm_r(tcry.KEY_BUFF(*_offset(x, offset)))


def decodeint_noreduce(x, offset=0):
    return tcry.expand_raw256_modm_r(tcry.KEY_BUFF(*_offset(x, offset)))


def decodeint_into(r, x, offset=0):
    bb = _offset(x, offset)[:32]
    tcry.expand256_modm(r, tcry.KEY_BUFF(*bb), 32)
    return r


def decodeint_into_noreduce(r, x, offset=0):
    r = r if r else new_scalar()
    tcry.expand_raw256_modm(r, tcry.KEY_BUFF(*_offset(x, offset)))
    return r


def encodeint(x):
    return tcry.contract256_modm_r(x)


def encodeint_into(b, x, offset=0):
    bf = tcry.KEY_BUFF.from_buffer(_offset(b, offset))
    tcry.contract256_modm(bf, x)
    return b


#
# Zmod(2^255 - 19) operations, fe (field element)
# Not constant time! PoC only.
#


def fe_1():
    return tcry.curve25519_set_r(1)


def fe_mod(a):
    return tcry.curve25519_reduce_r(a)


def fe_add(a, b):
    return tcry.curve25519_add_r(a, b)


def fe_sub(a, b):
    return tcry.curve25519_sub_reduce_r(a, b)


def fe_sq(a):
    return tcry.curve25519_square_r(a)


def fe_mul(a, b):
    return tcry.curve25519_mul_r(a, b)


def fe_expmod(b, e):
    raise ValueError("Not implemented")


def fe_divpowm1(u, v):
    raise ValueError("Not implemented")


def fe_isnegative(x):
    return tcry.curve25519_isnegative(x)


def fe_isnonzero(x):
    return tcry.curve25519_isnonzero(x)


#
# Zmod(order), scalar values field
#


def sc_0():
    """
    Sets 0 to the scalar value Zmod(m)
    :return:
    """
    return tcry.init256_modm_r(0)


def sc_0_into(r):
    """
    Sets 0 to the scalar value Zmod(m)
    :return:
    """
    tcry.init256_modm(r, 0)
    return r


def sc_init(x):
    """
    Sets x to the scalar value Zmod(m)
    :return:
    """
    if x >= (1 << 64):
        raise ValueError("Initialization works up to 64-bit only")
    return tcry.init256_modm_r(x)


def sc_copy(d, x):
    d = d if d else new_scalar()
    return sc_add_into(d, x, sc_init(0))
    #return tcry.init256_modm(d, x)


def sc_init_into(r, x):
    """
    Sets x to the scalar value Zmod(m)
    :return:
    """
    r = r if r else new_scalar()
    if x >= (1 << 64):
        raise ValueError("Initialization works up to 64-bit only")
    tcry.init256_modm(r, x)
    return r


def sc_get64(x):
    """
    Returns 64bit value from the sc
    :param x:
    :return:
    """
    return tcry.get256_modm_r(x)


def sc_check(key):
    """
    sc_check is not relevant for long-integer scalar representation.

    :param key:
    :return:
    """
    return not tcry.check256_modm(key)


def check_sc(key):
    """
    throws exception on invalid key
    :param key:
    :return:
    """
    if sc_check(key) != 0:
        raise ValueError("Invalid scalar value")


def sc_reduce32(data):
    return tcry.barrett_reduce256_modm_r(sc_0(), data)


def sc_add(aa, bb):
    return tcry.add256_modm_r(aa, bb)


def sc_add_into(r, aa, bb):
    r = r if r else new_scalar()
    tcry.add256_modm(r, aa, bb)
    return r


def sc_sub(aa, bb):
    return tcry.sub256_modm_r(aa, bb)


def sc_sub_into(r, aa, bb):
    r = r if r else new_scalar()
    tcry.sub256_modm(r, aa, bb)
    return r


def sc_mul(aa, bb):
    return tcry.mul256_modm_r(aa, bb)


def sc_mul_into(r, aa, bb):
    r = r if r else new_scalar()
    tcry.mul256_modm(r, aa, bb)
    return r


def sc_isnonzero(c):
    return not tcry.iszero256_modm(c)


def sc_eq(a, b):
    return tcry.eq256_modm(a, b)


def sc_mulsub(aa, bb, cc):
    """
    (cc - aa * bb) % l
    """
    return tcry.mulsub256_modm_r(aa, bb, cc)


def sc_mulsub_into(r, aa, bb, cc):
    """
    (cc - aa * bb) % l
    """
    r = r if r else new_scalar()
    tcry.mulsub256_modm(r, aa, bb, cc)
    return r


def sc_muladd(aa, bb, cc):
    """
    (cc + aa * bb) % l
    """
    return tcry.muladd256_modm_r(aa, bb, cc)


def sc_muladd_into(r, aa, bb, cc):
    """
    (cc + aa * bb) % l
    """
    r = r if r else new_scalar()
    tcry.muladd256_modm(r, aa, bb, cc)
    return r


def sc_inv(x):
    return sc_inv_into(new_scalar(), x)


def sc_inv_into(r, x):
    """
    Modular inversion mod curve order L
    :param r:
    :param x:
    :return:
    """
    r = r if r else new_scalar()
    global ED25519_ORD_BN
    if ED25519_ORD_BN is None:
        bf_p = tcry.KEY_BUFF.from_buffer(bytearray(ED25519_ORD))
        ED25519_ORD_BN = tcry.bn_zero_r()
        tcry.bn_read_le(bf_p, ED25519_ORD_BN)

    rr = bytearray(32)
    xx = bytearray(32)
    encodeint_into(xx, x)
    bf_x = tcry.KEY_BUFF.from_buffer(xx)
    bf_r = tcry.KEY_BUFF.from_buffer(rr)

    bn_x = tcry.bn_zero_r()
    tcry.bn_read_le(bf_x, bn_x)
    tcry.bn_inverse(bn_x, ED25519_ORD_BN)
    tcry.bn_write_le(bn_x, bf_r)
    return decodeint_into_noreduce(r, rr)


def random_scalar():
    return tcry.xmr_random_scalar_r()


def random_scalar_into(r):
    r = r if r else new_scalar()
    tcry.xmr_random_scalar(r)
    return r


#
# GE - ed25519 group
#

ZERO = b"\x00" * 32
INV_EIGHT = b"\x79\x2f\xdc\xe2\x29\xe5\x06\x61\xd0\xda\x1c\x7d\xb3\x9d\xd3\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06"
INV_EIGHT_SC = decodeint(INV_EIGHT)


def check_ed25519point(x):
    if tcry.ge25519_check(x) != 1:
        raise ValueError("P is not on ed25519 curve")


def scalarmult_base(a):
    return tcry.ge25519_scalarmult_base_wrapper_r(a)


def scalarmult_base_into(r, a):
    r = r if r else new_point()
    tcry.ge25519_scalarmult_base_wrapper(r, a)
    return r


def scalarmult(P, e):
    return tcry.ge25519_scalarmult_r(P, e)


def scalarmult_into(r, P, e):
    r = r if r else new_point()
    tcry.ge25519_scalarmult(r, P, e)
    return r


def point_add(P, Q):
    return tcry.ge25519_add_r(P, Q, 0)


def point_add_into(r, P, Q):
    r = r if r else new_point()
    tcry.ge25519_add(r, P, Q, 0)
    return r


def point_sub(P, Q):
    return tcry.ge25519_add_r(P, Q, 1)


def point_sub_into(r, P, Q):
    r = r if r else new_point()
    tcry.ge25519_add(r, P, Q, 1)
    return r


def point_eq(P, Q):
    return tcry.ge25519_eq(P, Q)


def point_double(P):
    return tcry.ge25519_double_r(P)


def point_double_into(r, P):
    r = r if r else new_point()
    tcry.ge25519_double(r, P)
    return r


def point_norm(P):
    """
    Normalizes point after multiplication
    Extended edwards coordinates (X,Y,Z,T)
    :param P:
    :return:
    """
    return tcry.ge25519_norm_r(P)


def point_mul8(P):
    return tcry.ge25519_mul8_r(P)


def point_mulinv8(P):
    return scalarmult(P, INV_EIGHT_SC)


def point_mul8_into(r, P):
    r = r if r else new_point()
    tcry.ge25519_mul8(r, P)
    return r


def sc_inv_eight():
    return INV_EIGHT_SC


def ge_double_scalarmult_base_vartime(a, A, b):
    """
    void ge25519_double_scalarmult_vartime(ge25519 *r, const ge25519 *p1, const bignum256modm s1, const bignum256modm s2);
    r = a * A + b * B

    :param a:
    :param A:
    :param b:
    :return:
    """
    R = tcry.ge25519_double_scalarmult_vartime_r(A, a, b)
    tcry.ge25519_norm(R, R)
    return R


def ge_double_scalarmult_base_vartime2(a, A, b, B):
    """
    void ge25519_double_scalarmult_vartime2(ge25519 *r, const ge25519 *p1, const bignum256modm s1, const ge25519 *p2, const bignum256modm s2);
    r = a * A + b * B

    :param a:
    :param A:
    :param b:
    :param B:
    :return:
    """
    R = tcry.ge25519_double_scalarmult_vartime2_r(A, a, B, b)
    tcry.ge25519_norm(R, R)
    return R


def ge_double_scalarmult_precomp_vartime(a, A, b, Bi):
    """
    void ge_double_scalarmult_precomp_vartime(ge_p2 *r, const unsigned char *a, const ge_p3 *A, const unsigned char *b, const ge_dsmp Bi)
    :return:
    """
    return ge_double_scalarmult_precomp_vartime2(a, A, b, Bi)


def ge_double_scalarmult_precomp_vartime2(a, Ai, b, Bi):
    """
    void ge_double_scalarmult_precomp_vartime2(ge_p2 *r, const unsigned char *a, const ge_dsmp Ai, const unsigned char *b, const ge_dsmp Bi)
    :param a:
    :param Ai:
    :param b:
    :param Bi:
    :return:
    """
    return tcry.xmr_add_keys3_r(a, Ai, b, Bi)


def identity(byte_enc=False):
    """
    Identity point
    :return:
    """
    idd = tcry.ge25519_set_neutral_r()
    return idd if not byte_enc else encodepoint(idd)


def identity_into(r):
    """
    Identity point
    :return:
    """
    r = r if r else new_point()
    tcry.ge25519_set_neutral(r)
    return r


def ge_frombytes_vartime_check(point):
    """
    https://www.imperialviolet.org/2013/12/25/elligator.html
    http://elligator.cr.yp.to/
    http://elligator.cr.yp.to/elligator-20130828.pdf
    :param key:
    :return:
    """
    return 0 if tcry.ge25519_check(point) == 1 else -1


def ge_frombytes_vartime(point):
    """
    https://www.imperialviolet.org/2013/12/25/elligator.html

    :param key:
    :return:
    """
    ge_frombytes_vartime_check(point)
    return point


def precomp(point):
    """
    Precomputation placeholder
    :param point:
    :return:
    """
    return point


def ge_dsm_precomp(point):
    """
    void ge_dsm_precomp(ge_dsmp r, const ge_p3 *s)
    :param point:
    :return:
    """
    return point


#
# Monero specific
#


def cn_fast_hash(buff):
    """
    Keccak 256, original one (before changes made in SHA3 standard)
    :param buff:
    :return:
    """
    return keccak_hash(buff)


def hash_to_scalar(data, length=None):
    """
    H_s(P)
    :param data:
    :param length:
    :return:
    """
    dt = data[:length] if length else data
    return tcry.xmr_hash_to_scalar_r(bytes(dt))


def hash_to_scalar_into(r, data, length=None):
    """
    H_s(P)
    :param data:
    :param length:
    :return:
    """
    dt = data[:length] if length else data
    tcry.xmr_hash_to_scalar(r, bytes(dt))
    return r


def hash_to_point(buf):
    """
    H_p(buf)

    https://github.com/monero-project/research-lab/blob/master/whitepaper/ge_fromfe_writeup/ge_fromfe.pdf
    http://archive.is/yfINb
    :param key:
    :return:
    """
    return tcry.xmr_hash_to_ec_r(buf)


def hash_to_point_into(r, buf):
    """
    H_p(buf)

    https://github.com/monero-project/research-lab/blob/master/whitepaper/ge_fromfe_writeup/ge_fromfe.pdf
    http://archive.is/yfINb
    :param key:
    :return:
    """
    bf = tcry.KEY_BUFF.from_buffer_copy(buf)
    tcry.xmr_hash_to_ec(r, bf)
    return r


#
# XMR
#


def xmr_H():
    """
    Returns point H
    8b655970153799af2aeadc9ff1add0ea6c7251d54154cfa92c173a0dd39c1f94
    :return:
    """
    return tcry.ge25519_set_xmr_h_r()


def scalarmult_h(i):
    return scalarmult(xmr_H(), sc_init(i) if isinstance(i, int) else i)


def add_keys2(a, b, B):
    """
    aG + bB, G is basepoint
    :param a:
    :param b:
    :param B:
    :return:
    """
    return tcry.xmr_add_keys2_vartime_r(a, b, B)


def add_keys2_into(r, a, b, B):
    """
    aG + bB, G is basepoint
    :param r:
    :param a:
    :param b:
    :param B:
    :return:
    """
    tcry.xmr_add_keys2_vartime(r, a, b, B)
    return r


def add_keys3(a, A, b, B):
    """
    aA + bB
    :param a:
    :param A:
    :param b:
    :param B:
    :return:
    """
    return tcry.xmr_add_keys3_vartime_r(a, A, b, B)


def add_keys3_into(r, a, A, b, B):
    """
    aA + bB
    :param r:
    :param a:
    :param A:
    :param b:
    :param B:
    :return:
    """
    tcry.xmr_add_keys3_vartime(r, a, A, b, B)
    return r


def gen_c(a, amount):
    """
    Generates Pedersen commitment
    C = aG + bH

    :param a:
    :param amount:
    :return:
    """
    return tcry.xmr_gen_c_r(a, amount)


def generate_key_derivation(key1, key2):
    """
    Key derivation: 8*(key2*key1)

    :param key1: public key of receiver Bob (see page 7)
    :param key2: Alice's private
    :return:
    """
    if sc_check(key2) != 0:
        # checks that the secret key is uniform enough...
        raise ValueError("error in sc_check in keyder")
    if ge_frombytes_vartime_check(key1) != 0:
        raise ValueError("didn't pass curve checks in keyder")

    return tcry.xmr_generate_key_derivation_r(key1, key2)


def derivation_to_scalar(derivation, output_index):
    """
    H_s(derivation || varint(output_index))
    :param derivation:
    :param output_index:
    :return:
    """
    check_ed25519point(derivation)
    return tcry.xmr_derivation_to_scalar_r(derivation, output_index)


def derive_public_key(derivation, output_index, base):
    """
    H_s(derivation || varint(output_index))G + base

    :param derivation:
    :param output_index:
    :param base:
    :return:
    """
    if ge_frombytes_vartime_check(base) != 0:  # check some conditions on the point
        raise ValueError("derive pub key bad point")
    check_ed25519point(base)

    return tcry.xmr_derive_public_key_r(derivation, output_index, base)


def derive_secret_key(derivation, output_index, base):
    """
    base + H_s(derivation || varint(output_index))
    :param derivation:
    :param output_index:
    :param base:
    :return:
    """
    if sc_check(base) != 0:
        raise ValueError("cs_check in derive_secret_key")
    return tcry.xmr_derive_private_key_r(derivation, output_index, base)


def get_subaddress_secret_key(secret_key, major=0, minor=0):
    """
    Builds subaddress secret key from the subaddress index
    Hs(SubAddr || a || index_major || index_minor)

    :param secret_key:
    :param index:
    :param major:
    :param minor:
    :return:
    """
    return tcry.xmr_get_subaddress_secret_key_r(major, minor, secret_key)


def prove_range(amount, last_mask=None):
    """
    Range proof provided by the backend. Implemented in C for speed.

    :param amount:
    :param last_mask:
    :return:
    """
    C, a, R = tcry.gen_range_proof(amount, last_mask)

    # Trezor micropython extmod returns byte-serialized/flattened rsig
    nrsig = b""
    for i in range(len(R.asig.s0)):
        nrsig += bytes(R.asig.s0[i])
    for i in range(len(R.asig.s1)):
        nrsig += bytes(R.asig.s1[i])
    nrsig += bytes(R.asig.ee)
    for i in range(len(R.Ci)):
        nrsig += bytes(R.Ci[i])
    return C, a, nrsig

    # # Rewrap to serializable structures
    # nrsig = xmrtypes.RangeSig()
    # nrsig.asig = xmrtypes.BoroSig()
    # nrsig.asig.ee = bytes(R.asig.ee)
    # nrsig.Ci = list(R.Ci)
    # nrsig.asig.s0 = list(R.asig.s0)
    # nrsig.asig.s1 = list(R.asig.s1)
    # del R
    #
    # for i in range(64):
    #     nrsig.Ci[i] = bytes(nrsig.Ci[i])
    #     nrsig.asig.s0[i] = bytes(nrsig.asig.s0[i])
    #     nrsig.asig.s1[i] = bytes(nrsig.asig.s1[i])
    #
    # return C, a, nrsig


ge25519_double_scalarmult_base_vartime = ge_double_scalarmult_base_vartime


#
# Backend config
#


class TcryECBackend(ECBackendBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_rangeproof_borromean(self):
        return True

    def has_rangeproof_bulletproof(self):
        return True

    def has_crypto_into_functions(self):
        return True

    def is_fast(self):
        return True


BACKEND_OBJ = None


def get_backend():
    global BACKEND_OBJ
    if BACKEND_OBJ is None:
        BACKEND_OBJ = TcryECBackend()
    return BACKEND_OBJ
