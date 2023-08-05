# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Module wrapping all the public and private keys cryptography."""

from typing import Dict, Optional, cast

import aea.crypto
from aea.crypto.base import Crypto


class CryptoStore:
    """Utility class to store and retrieve crypto objects."""

    def __init__(
        self, crypto_id_to_path: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
        Initialize the crypto store.

        :param crypto_id_to_path: dictionary from crypto id to an (optional) path
            to the private key.
        """
        if crypto_id_to_path is None:
            crypto_id_to_path = {}
        crypto_objects = {}  # type: Dict[str, Crypto]
        public_keys = {}  # type: Dict[str, str]
        addresses = {}  # type: Dict[str, str]

        for identifier, path in crypto_id_to_path.items():
            crypto = aea.crypto.make(identifier, private_key_path=path)
            crypto_objects[identifier] = crypto
            public_keys[identifier] = cast(str, crypto.public_key)
            addresses[identifier] = cast(str, crypto.address)

        self._crypto_objects = crypto_objects
        self._public_keys = public_keys
        self._addresses = addresses

    @property
    def public_keys(self) -> Dict[str, str]:
        """Get the public_key dictionary."""
        return self._public_keys

    @property
    def crypto_objects(self) -> Dict[str, Crypto]:
        """Get the crypto objects (key pair)."""
        return self._crypto_objects

    @property
    def addresses(self) -> Dict[str, str]:
        """Get the crypto addresses."""
        return self._addresses


class Wallet:
    """
    Container for crypto objects.

    The cryptos are separated into two categories:

    - main cryptos: used by the AEA for the economic side (i.e. signing transaction)
    - connection cryptos: exposed to the connection objects for encrypted communication.

    """

    # TODO do some check after loading the keys
    #   to see whether we have duplicate cryptos?
    def __init__(
        self,
        private_key_paths: Dict[str, Optional[str]],
        connection_private_key_paths: Optional[Dict[str, Optional[str]]] = None,
    ):
        """
        Instantiate a wallet object.

        :param private_key_paths: the private key paths
        :param connection_private_key_paths: the private key paths for the connections.
        """
        self._main_cryptos = CryptoStore(private_key_paths)
        self._connection_cryptos = CryptoStore(connection_private_key_paths)

    @property
    def public_keys(self) -> Dict[str, str]:
        """Get the public_key dictionary."""
        return self._main_cryptos.public_keys

    @property
    def crypto_objects(self) -> Dict[str, Crypto]:
        """Get the crypto objects (key pair)."""
        return self._main_cryptos.crypto_objects

    @property
    def addresses(self) -> Dict[str, str]:
        """Get the crypto addresses."""
        return self._main_cryptos.addresses

    @property
    def main_cryptos(self) -> CryptoStore:
        """Get the main crypto store."""
        return self._main_cryptos

    @property
    def connection_cryptos(self) -> CryptoStore:
        """Get the connection crypto store."""
        return self._connection_cryptos
