import hmac
from binascii import hexlify, unhexlify
from hashlib import sha256, sha512

import six
from ecdsa import SECP256k1
from ecdsa.ecdsa import Public_key as _ECDSA_Public_key
from ecdsa.ellipticcurve import INFINITY
from monero_glue.misc import b58 as base58
from monero_glue.misc.bip import bip39
from monero_glue.xmr import crypto

from .keys import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
    PrivateKey,
    PublicKey,
    PublicPair,
    incompatible_network_exception_factory,
)
from .network import *
from .utils import (
    chr_py2,
    ensure_bytes,
    ensure_str,
    hash160,
    is_hex_string,
    long_or_int,
    long_to_hex,
    memoize,
)


class Wallet(object):
    """A BIP32 wallet is made up of Wallet nodes.
    A Private node contains both a public and private key, while a public
    node contains only a public key.
    **WARNING**:
    When creating a NEW wallet you MUST back up the private key. If
    you don't then any coins sent to your address will be LOST FOREVER.
    You need to save the private key somewhere. It is OK to just write
    it down on a piece of paper! Don't share this key with anyone!
    >>> my_wallet = Wallet.from_master_secret(
    ...     key='correct horse battery staple')
    >>> private = my_wallet.serialize(private=True)
    >>> private  # doctest: +ELLIPSIS
    u'xprv9s21ZrQH143K2mDJW8vDeFwbyDbFv868mM2Zr87rJSTj8q16Unkaq1pryiV...'
    If you want to use this wallet on your website to accept bitcoin or
    altcoin payments, you should first create a primary child.
    BIP32 Hierarchical Deterministic Wallets are described in this BIP:
    https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
    """

    def __init__(
        self,
        chain_code,
        depth=0,
        parent_fingerprint=0,
        child_number=0,
        private_exponent=None,
        private_key=None,
        public_pair=None,
        public_key=None,
        network="bitcoin_testnet",
        seed_secret=None,
        use_ed25519=False,
        use_slip0010=False,
    ):
        """Construct a new BIP32 compliant wallet.
        You probably don't want to use this init methd. Instead use one
        of the 'from_master_secret' or 'deserialize' cosntructors.
        """

        if not (private_exponent or private_key) and (
            not use_ed25519 and not (public_pair or public_key)
        ):
            raise InsufficientKeyDataError(
                "You must supply one of private_exponent or public_pair"
            )

        network = Wallet.get_network(network)
        self.private_key = None
        self.public_key = None
        self.seed_secret = seed_secret
        self.use_ed25519 = use_ed25519
        self.use_slip0010 = use_slip0010
        if use_slip0010:
            raise NotImplementedError()

        if private_key:
            if not isinstance(private_key, PrivateKey):
                raise InvalidPrivateKeyError(
                    "private_key must be of type " "bitmerchant.wallet.keys.PrivateKey"
                )
            self.private_key = private_key
        elif private_exponent:
            self.private_key = PrivateKey(private_exponent, network=network)

        if use_ed25519 and public_key:
            self.public_key = public_key
        elif use_ed25519:
            self.public_key = self.private_key.get_public_key()
        elif public_key:
            if not isinstance(public_key, PublicKey):
                raise InvalidPublicKeyError(
                    "public_key must be of type " "bitmerchant.wallet.keys.PublicKey"
                )
            self.public_key = public_key
        elif public_pair:
            self.public_key = PublicKey.from_public_pair(public_pair, network=network)
        else:
            self.public_key = self.private_key.get_public_key()

        if (
            not self.use_ed25519
            and self.private_key
            and self.private_key.get_public_key() != self.public_key
        ):
            raise KeyMismatchError("Provided private and public values do not match")

        def h(val, hex_len):
            if isinstance(val, six.integer_types):
                return long_to_hex(val, hex_len)
            elif (
                isinstance(val, six.string_types) or isinstance(val, six.binary_type)
            ) and is_hex_string(val):
                val = ensure_bytes(val)
                if len(val) != hex_len:
                    raise ValueError("Invalid parameter length")
                return val
            else:
                raise ValueError("Invalid parameter type")

        def l(val):
            if isinstance(val, six.integer_types):
                return long_or_int(val)
            elif isinstance(val, six.string_types) or isinstance(val, six.binary_type):
                val = ensure_bytes(val)
                if not is_hex_string(val):
                    val = hexlify(val)
                return long_or_int(val, 16)
            else:
                raise ValueError("parameter must be an int or long")

        self.network = Wallet.get_network(network)
        self.depth = l(depth)
        if isinstance(parent_fingerprint, six.string_types) or isinstance(
            parent_fingerprint, six.binary_type
        ):
            val = ensure_bytes(parent_fingerprint)
            if val.startswith(b"0x"):
                parent_fingerprint = val[2:]
        self.parent_fingerprint = b"0x" + h(parent_fingerprint, 8)
        self.child_number = l(child_number)
        self.chain_code = h(chain_code, 64)

    def get_private_key_hex(self):
        """
        Get the hex-encoded (I guess SEC1?) representation of the private key.
        DO NOT share this private key with anyone.
        """
        return ensure_bytes(self.private_key.get_key())

    def get_public_key_hex(self, compressed=True):
        """Get the sec1 representation of the public key."""
        return ensure_bytes(self.public_key.get_key(compressed))

    @property
    def identifier(self):
        """Get the identifier for this node.
        Extended keys can be identified by the Hash160 (RIPEMD160 after SHA256)
        of the public key's `key`. This corresponds exactly to the data used in
        traditional Bitcoin addresses. It is not advised to represent this data
        in base58 format though, as it may be interpreted as an address that
        way (and wallet software is not required to accept payment to the chain
        key itself).
        """
        key = self.get_public_key_hex()
        return ensure_bytes(hexlify(hash160(unhexlify(key))))

    @property
    def fingerprint(self):
        """The first 32 bits of the identifier are called the fingerprint."""
        # 32 bits == 4 Bytes == 8 hex characters
        return b"0x" + self.identifier[:8]

    @staticmethod
    def bytes_to_indices(seed, bits=11):
        """
        Transforms byte stream to list of bits-sized integers.
        Used to transform secret seed to word list.
        Consistent with https://iancoleman.io/bip39/
        
        :param seed:
        :param bits:
        :return:
        """
        seed_len = len(seed)
        indices = []
        carry = 0
        carry_bits = 0
        for idx, b in enumerate(seed):
            cleft = min(8, bits - carry_bits)
            cleft_bl = 8 - cleft
            flush = cleft == bits - carry_bits

            carry_bits += cleft
            carry <<= cleft
            carry |= (int(b) >> cleft_bl) & (2 ** cleft - 1)

            if idx + 1 == seed_len and cleft != 0:
                carry <<= bits - carry_bits
                flush = True

            if flush:
                indices.append(carry)
                carry = int(b) & (2 ** cleft_bl - 1)
                carry_bits = cleft_bl

        return indices

    @staticmethod
    def indices_to_bytes(indices, bits=11):
        """
        Converts indices to byte array
        :param indices:
        :param bits:
        :return:
        """
        ind_len = len(indices)
        barr = []

        cidx = 0
        carry = 0
        carry_bits = 0
        avail = bits

        while True:
            cb = 8 - carry_bits
            cons = min(cb, avail)
            carry <<= cons
            carry |= indices[cidx] >> (avail - cons) & ((1 << cons) - 1)
            carry_bits += cons
            avail -= cons

            if cb == cons:
                barr.append(carry)
                carry = 0
                carry_bits = 0

            if avail == 0:
                if cidx + 1 == ind_len:
                    break
                cidx += 1
                avail = bits
        return bytes(barr)

    def to_seed_words(self):
        """
        Generates word-based seed:
        secret seed bits + SHA256 checksum -> words.
        :return:
        """
        if self.seed_secret is None:
            return None

        checksum = sha256(self.seed_secret).digest()
        seed = self.seed_secret + checksum[:1]

        indices = Wallet.bytes_to_indices(seed)
        words = [bip39.english_words[x] for x in indices]
        return words, indices

    def create_new_address_for_user(self, user_id):
        """Create a new bitcoin address to accept payments for a User.
        This is a convenience wrapper around `get_child` that helps you do
        the right thing. This method always creates a public, non-prime
        address that can be generated from a BIP32 public key on an
        insecure server."""
        max_id = 0x80000000
        if user_id < 0 or user_id > max_id:
            raise ValueError("Invalid UserID. Must be between 0 and %s" % max_id)
        return self.get_child(user_id, is_prime=False, as_private=False)

    def get_child_for_path(self, path):
        """Get a child for a given path.
        Rather than repeated calls to get_child, children can be found
        by a derivation path. Paths look like:
            m/0/1'/10
        Which is the same as
            self.get_child(0).get_child(-1).get_child(10)
        Or, in other words, the 10th publicly derived child of the 1st
        privately derived child of the 0th publicly derived child of master.
        You can use either ' or p to denote a prime (that is, privately
        derived) child.
        A child that has had its private key stripped can be requested by
        either passing a capital M or appending '.pub' to the end of the path.
        These three paths all give the same child that has had its private
        key scrubbed:
            M/0/1
            m/0/1.pub
            M/0/1.pub
        """
        path = ensure_str(path)

        if not path:
            raise InvalidPathError("%s is not a valid path" % path)

        # Figure out public/private derivation
        as_private = True
        if path.startswith("M"):
            as_private = False
        if path.endswith(".pub"):
            as_private = False
            path = path[:-4]

        parts = path.split("/")
        if len(parts) == 0:
            raise InvalidPathError()

        child = self
        for part in parts:
            if part.lower() == "m":
                continue
            is_prime = None  # Let primeness be figured out by the child number
            if part[-1] in "'p":
                is_prime = True
                part = part.replace("'", "").replace("p", "")
            try:
                child_number = long_or_int(part)
            except ValueError:
                raise InvalidPathError("%s is not a valid path" % path)
            child = child.get_child(child_number, is_prime)
        if not as_private:
            return child.public_copy()
        return child

    @memoize
    def get_child(self, child_number, is_prime=None, as_private=True):
        """Derive a child key.
        :param child_number: The number of the child key to compute
        :type child_number: int
        :param is_prime: If True, the child is calculated via private
            derivation. If False, then public derivation is used. If None,
            then it is figured out from the value of child_number.
        :type is_prime: bool, defaults to None
        :param as_private: If True, strips private key from the result.
            Defaults to False. If there is no private key present, this is
            ignored.
        :type as_private: bool
        Positive child_numbers (less than 2,147,483,648) produce publicly
        derived children.
        Negative numbers (greater than -2,147,483,648) uses private derivation.
        NOTE: Python can't do -0, so if you want the privately derived 0th
        child you need to manually set is_prime=True.
        NOTE: negative numbered children are provided as a convenience
        because nobody wants to remember the above numbers. Negative numbers
        are considered 'prime children', which is described in the BIP32 spec
        as a leading 1 in a 32 bit unsigned int.
        This derivation is fully described at
        https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#child-key-derivation-functions  # nopep8
        """
        boundary = 0x80000000

        if abs(child_number) >= boundary:
            raise ValueError("Invalid child number %s" % child_number)

        # If is_prime isn't set, then we can infer it from the child_number
        if is_prime is None:
            # Prime children are either < 0 or > 0x80000000
            if child_number < 0:
                child_number = abs(child_number)
                is_prime = True
            elif child_number >= boundary:
                child_number -= boundary
                is_prime = True
            else:
                is_prime = False
        else:
            # Otherwise is_prime is set so the child_number should be between
            # 0 and 0x80000000
            if child_number < 0 or child_number >= boundary:
                raise ValueError(
                    "Invalid child number. Must be between 0 and %s" % boundary
                )

        if not self.private_key and is_prime:
            raise ValueError("Cannot compute a prime child without a private key")

        if is_prime:
            # Even though we take child_number as an int < boundary, the
            # internal derivation needs it to be the larger number.
            child_number = child_number + boundary
        child_number_hex = long_to_hex(child_number, 8)

        if is_prime:
            # Let data = concat(0x00, self.key, child_number)
            data = b"00" + self.private_key.get_key()
        else:
            data = self.get_public_key_hex()
            if self.use_ed25519:
                raise InvalidPathError("Ed25519 public derivation is not implemented")

        data += child_number_hex

        # Compute a 64 Byte I that is the HMAC-SHA512, using self.chain_code
        # as the seed, and data as the message.
        I = hmac.new(
            unhexlify(self.chain_code), msg=unhexlify(data), digestmod=sha512
        ).digest()
        # Split I into its 32 Byte components.
        I_L, I_R = I[:32], I[32:]
        if not self.use_ed25519 and long_or_int(hexlify(I_L), 16) >= SECP256k1.order:
            raise InvalidPrivateKeyError("The derived key is too large.")

        c_i = hexlify(I_R)
        private_exponent = None
        private_key = None
        public_key = None

        if self.use_ed25519 and not self.private_key:
            raise InvalidPathError("Ed25519 public derivation is not implemented")

        if self.use_ed25519:
            private_key = Ed25519PrivateKey.from_hex_key(I_L)
            public_key = private_key.get_public_key()

        elif not self.use_ed25519 and self.private_key:
            # Use private information for derivation
            # I_L is added to the current key's secret exponent (mod n), where
            # n is the order of the ECDSA curve in use.
            private_exponent = (
                long_or_int(hexlify(I_L), 16)
                + long_or_int(self.private_key.get_key(), 16)
            ) % SECP256k1.order
            # I_R is the child's chain code
            private_key = PrivateKey(private_exponent)
            public_key = private_key.get_public_key()

        elif not self.use_ed25519:
            # Only use public information for this derivation
            g = SECP256k1.generator
            I_L_long = long_or_int(hexlify(I_L), 16)
            point = (
                _ECDSA_Public_key(g, g * I_L_long).point + self.public_key.to_point()
            )
            # I_R is the child's chain code
            private_key = PrivateKey(private_exponent)
            public_key = PublicKey.from_public_pair(PublicPair(point.x(), point.y()))

        if public_key.to_point() == INFINITY:
            raise InfinityPointException("The point at infinity is invalid.")

        child = self.__class__(
            chain_code=c_i,
            depth=self.depth + 1,  # we have to go deeper...
            parent_fingerprint=self.fingerprint,
            child_number=child_number_hex,
            private_key=private_key,
            public_key=public_key,
            network=self.network,
            use_slip0010=self.use_slip0010,
            use_ed25519=self.use_ed25519,
        )

        if not as_private:
            return child.public_copy()
        return child

    def public_copy(self):
        """Clone this wallet and strip it of its private information."""
        return self.__class__(
            chain_code=self.chain_code,
            depth=self.depth,
            parent_fingerprint=self.parent_fingerprint,
            child_number=self.child_number,
            public_pair=self.public_key.to_public_pair(),
            network=self.network,
        )

    def crack_private_key(self, child_private_key):
        """Crack the parent private key given a child private key.
        BIP32 has a vulnerability/feature that allows you to recover the
        master private key if you're given a master public key and any of its
        publicly-derived child private keys. This is a pretty serious security
        vulnerability that looks as innocuous as this:
        >>> w = Wallet.new_random_wallet()
        >>> child = w.get_child(0, is_prime=False)
        >>> w_pub = w.public_copy()
        >>> assert w_pub.private_key is None
        >>> master_public_key = w_pub.serialize_b58(private=False)
        >>> # Now you put master_public_key on your website
        >>> # and give somebody a private key
        >>> public_master = Wallet.deserialize(master_public_key)
        >>> cracked_private_master = public_master.crack_private_key(child)
        >>> assert w == cracked_private_master  # :(
        Implementation details from http://bitcoinmagazine.com/8396/deterministic-wallets-advantages-flaw/  # nopep8
        """
        if self.private_key:
            raise AssertionError("You already know the private key")
        if child_private_key.parent_fingerprint != self.fingerprint:
            raise ValueError("This is not a valid child")
        if child_private_key.child_number >= 0x80000000:
            raise ValueError("Cannot crack private keys from private derivation")

        # Duplicate the public child derivation
        child_number_hex = long_to_hex(child_private_key.child_number, 8)
        data = self.get_public_key_hex() + child_number_hex
        I = hmac.new(
            unhexlify(self.chain_code), msg=unhexlify(data), digestmod=sha512
        ).digest()
        I_L, I_R = I[:32], I[32:]
        # Public derivation is the same as private derivation plus some offset
        # knowing the child's private key allows us to find this offset just
        # by subtracting the child's private key from the parent I_L data
        privkey = PrivateKey(long_or_int(hexlify(I_L), 16), network=self.network)
        parent_private_key = child_private_key.private_key - privkey
        return self.__class__(
            chain_code=self.chain_code,
            depth=self.depth,
            parent_fingerprint=self.parent_fingerprint,
            child_number=self.child_number,
            private_key=parent_private_key,
            network=self.network,
        )

    def export_to_wif(self):
        """Export a key to WIF.
        See https://en.bitcoin.it/wiki/Wallet_import_format for a full
        description.
        """
        # Add the network byte, creating the "extended key"
        extended_key_hex = self.private_key.get_extended_key()
        # BIP32 wallets have a trailing \01 byte
        extended_key_bytes = unhexlify(extended_key_hex) + b"\01"
        # And return the base58-encoded result with a checksum
        return base58.b58encode_check(extended_key_bytes)

    def serialize(self, private=True):
        """Serialize this key.
        :param private: Whether or not the serialized key should contain
            private information. Set to False for a public-only representation
            that cannot spend funds but can create children. You want
            private=False if you are, for example, running an e-commerce
            website and want to accept bitcoin payments. See the README
            for more information.
        :type private: bool, defaults to True
        See the spec in `deserialize` for more details.
        """
        if private and not self.private_key:
            raise ValueError("Cannot serialize a public key as private")

        if private:
            network_version = long_to_hex(self.network.EXT_SECRET_KEY, 8)
        else:
            network_version = long_to_hex(self.network.EXT_PUBLIC_KEY, 8)
        depth = long_to_hex(self.depth, 2)
        parent_fingerprint = self.parent_fingerprint[2:]  # strip leading 0x
        child_number = long_to_hex(self.child_number, 8)
        chain_code = self.chain_code
        ret = network_version + depth + parent_fingerprint + child_number + chain_code
        # Private and public serializations are slightly different
        if private:
            ret += b"00" + self.private_key.get_key()
        else:
            ret += self.get_public_key_hex(compressed=True)
        return ensure_bytes(ret.lower())

    def serialize_b58(self, private=True):
        """Encode the serialized node in base58."""
        return ensure_str(base58.b58encode_check(unhexlify(self.serialize(private))))

    def to_address(self):
        """Create a public address from this Wallet.
        Public addresses can accept payments.
        https://en.bitcoin.it/wiki/Technical_background_of_Bitcoin_addresses
        """
        key = unhexlify(self.get_public_key_hex())
        # First get the hash160 of the key
        hash160_bytes = hash160(key)
        # Prepend the network address byte
        network_hash160_bytes = chr_py2(self.network.PUBKEY_ADDRESS) + hash160_bytes
        # Return a base58 encoded address with a checksum
        return ensure_str(base58.b58encode_check(network_hash160_bytes))

    @classmethod  # @memoize
    def deserialize(cls, key, network="bitcoin_testnet"):
        """Load the ExtendedBip32Key from a hex key.
        The key consists of
            * 4 byte version bytes (network key)
            * 1 byte depth:
                - 0x00 for master nodes,
                - 0x01 for level-1 descendants, ....
            * 4 byte fingerprint of the parent's key (0x00000000 if master key)
            * 4 byte child number. This is the number i in x_i = x_{par}/i,
              with x_i the key being serialized. This is encoded in MSB order.
              (0x00000000 if master key)
            * 32 bytes: the chain code
            * 33 bytes: the public key or private key data
              (0x02 + X or 0x03 + X for public keys, 0x00 + k for private keys)
              (Note that this also supports 0x04 + X + Y uncompressed points,
              but this is totally non-standard and this library won't even
              generate such data.)
        """
        network = Wallet.get_network(network)

        if len(key) in [78, (78 + 32)]:
            # we have a byte array, so pass
            pass
        else:
            key = ensure_bytes(key)
            if len(key) in [78 * 2, (78 + 32) * 2]:
                # we have a hexlified non-base58 key, continue!
                key = unhexlify(key)
            elif len(key) == 111:
                # We have a base58 encoded string
                key = base58.b58decode_check(key)
        # Now that we double checkd the values, convert back to bytes because
        # they're easier to slice
        version, depth, parent_fingerprint, child, chain_code, key_data = (
            key[:4],
            key[4],
            key[5:9],
            key[9:13],
            key[13:45],
            key[45:],
        )

        version_long = long_or_int(hexlify(version), 16)
        exponent = None
        pubkey = None
        point_type = key_data[0]
        if not isinstance(point_type, six.integer_types):
            point_type = ord(point_type)
        if point_type == 0:
            # Private key
            if version_long != network.EXT_SECRET_KEY:
                raise incompatible_network_exception_factory(
                    network.NAME, network.EXT_SECRET_KEY, version
                )
            exponent = key_data[1:]
        elif point_type in [2, 3, 4]:
            # Compressed public coordinates
            if version_long != network.EXT_PUBLIC_KEY:
                raise incompatible_network_exception_factory(
                    network.NAME, network.EXT_PUBLIC_KEY, version
                )
            pubkey = PublicKey.from_hex_key(key_data, network=network)
            # Even though this was generated from a compressed pubkey, we
            # want to store it as an uncompressed pubkey
            pubkey.compressed = False
        else:
            raise ValueError("Invalid key_data prefix, got %s" % point_type)

        def l(byte_seq):
            if byte_seq is None:
                return byte_seq
            elif isinstance(byte_seq, six.integer_types):
                return byte_seq
            return long_or_int(hexlify(byte_seq), 16)

        return cls(
            depth=l(depth),
            parent_fingerprint=l(parent_fingerprint),
            child_number=l(child),
            chain_code=l(chain_code),
            private_exponent=l(exponent),
            public_key=pubkey,
            network=network,
        )

    @classmethod
    def from_master_secret(
        cls, seed, network="monero", use_ed25519=False, use_slip0010=False
    ):
        """Generate a new PrivateKey from a secret key.
        :param seed: The key to use to generate this wallet. It may be a long
            string. Do not use a phrase from a book or song, as that will
            be guessed and is not secure. My advice is to not supply this
            argument and let me generate a new random key for you.
        :param network:
        :param use_ed25519:
        :param use_slip0010:
        See https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format  # nopep8
        See https://github.com/satoshilabs/slips/blob/master/slip-0010.md  # nopep8
        """
        network = Wallet.get_network(network)
        seed = ensure_bytes(seed)
        # Given a seed S of at least 128 bits, but 256 is advised
        # Calculate I = HMAC-SHA512(key="Bitcoin seed", msg=S)
        cv_seed = b"Bitcoin seed"
        if use_ed25519:
            cv_seed = b"ed25519 seed"

        I = hmac.new(cv_seed, msg=seed, digestmod=sha512).digest()
        # Split I into two 32-byte sequences, IL and IR.
        I_L, I_R = I[:32], I[32:]
        # Use IL as master secret key, and IR as master chain code.
        return cls(
            private_exponent=long_or_int(hexlify(I_L), 16),
            chain_code=long_or_int(hexlify(I_R), 16),
            network=network,
            seed_secret=seed,
            use_ed25519=use_ed25519,
            use_slip0010=use_slip0010,
        )

    @classmethod
    def from_master_secret_slow(cls, password, network=BitcoinMainNet):
        """
        Generate a new key from a password using 50,000 rounds of HMAC-SHA256.
        This should generate the same result as bip32.org.
        WARNING: The security of this method has not been evaluated.
        """
        # Make sure the password string is bytes
        key = ensure_bytes(password)
        data = unhexlify(b"0" * 64)  # 256-bit 0
        for i in range(50000):
            data = hmac.new(key, msg=data, digestmod=sha256).digest()
        return cls.from_master_secret(data, network)

    def __eq__(self, other):
        attrs = [
            "chain_code",
            "depth",
            "parent_fingerprint",
            "child_number",
            "private_key",
            "public_key",
            "network",
        ]
        return other and all(
            getattr(self, attr) == getattr(other, attr) for attr in attrs
        )

    def __ne__(self, other):
        return not self == other

    __hash__ = object.__hash__

    @classmethod
    def get_network(self, network):
        # returns a network class object

        response = None
        if network == "bitcoin_testnet" or network == "BTCTEST":
            response = BitcoinTestNet
        elif network == "bitcoin" or network == "BTC":
            response = BitcoinMainNet
        elif network == "dogecoin" or network == "DOGE":
            response = DogecoinMainNet
        elif network == "dogecoin_testnet" or network == "DOGETEST":
            response = DogecoinTestNet
        elif network == "litecoin" or network == "LTC":
            response = LitecoinMainNet
        elif network == "litecoin_testnet" or network == "LTCTEST":
            response = LitecoinTestNet
        elif network == "bitcoin_cash" or network == "BCH":
            response = BitcoinCashMainNet
        elif network == "bitcoin_gold" or network == "BTG":
            response = BitcoinGoldMainNet
        elif network == "dash" or network == "DASH":
            response = DashMainNet
        elif network == "dash_testnet" or network == "DASHTEST":
            response = DashTestNet
        elif network == "monero":
            response = MoneroMainNet
        else:
            response = network
        return response

    @classmethod
    def new_random_wallet(cls, user_entropy=None, network=BitcoinMainNet):
        """
        Generate a new wallet using a randomly generated 512 bit seed.
        Args:
            user_entropy: Optional user-supplied entropy which is combined
                combined with the random seed, to help counteract compromised
                PRNGs.
        You are encouraged to add an optional `user_entropy` string to protect
        against a compromised CSPRNG. This will be combined with the output
        from the CSPRNG. Note that if you do supply this value it only adds
        additional entropy and will not be sufficient to recover the random
        wallet. If you're even saving `user_entropy` at all, you're doing it
        wrong.
        """
        seed = crypto.random_bytes(64)
        if user_entropy:
            user_entropy = str(user_entropy)  # allow for int/long
            seed += user_entropy
        return cls.from_master_secret(seed, network=network)


class InvalidPathError(Exception):
    pass


class InsufficientKeyDataError(ValueError):
    pass


class InvalidPrivateKeyError(ValueError):
    pass


class InvalidPublicKeyError(ValueError):
    pass


class KeyMismatchError(ValueError):
    pass


class InfinityPointException(Exception):
    pass
