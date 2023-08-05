from monero_glue.xmr import crypto
from monero_glue.xmr.sub.addr import encode_addr
from monero_glue.xmr.sub.xmr_net import NetworkTypes, net_version
from typing import Optional
from monero_glue.xmr.crypto import Ge25519, Sc25519


class AccountCreds(object):
    """
    Stores account private keys
    """

    def __init__(
        self,
        view_key_private: Optional[Sc25519] = None,
        spend_key_private: Optional[Sc25519] = None,
        view_key_public: Optional[Ge25519] = None,
        spend_key_public: Optional[Ge25519] = None,
        address=None,
        network_type=NetworkTypes.MAINNET,
    ):
        self.view_key_private = view_key_private
        self.view_key_public = view_key_public
        self.spend_key_private = spend_key_private
        self.spend_key_public = spend_key_public
        self.address = address
        self.network_type = network_type
        self.multisig_keys = []

    @classmethod
    def new_wallet(
        cls, priv_view_key, priv_spend_key, network_type=NetworkTypes.MAINNET
    ):
        pub_view_key = crypto.scalarmult_base(priv_view_key)
        pub_spend_key = crypto.scalarmult_base(priv_spend_key)
        addr = encode_addr(
            net_version(network_type),
            crypto.encodepoint(pub_spend_key),
            crypto.encodepoint(pub_view_key),
        )
        return cls(
            view_key_private=priv_view_key,
            spend_key_private=priv_spend_key,
            view_key_public=pub_view_key,
            spend_key_public=pub_spend_key,
            address=addr,
            network_type=network_type,
        )
