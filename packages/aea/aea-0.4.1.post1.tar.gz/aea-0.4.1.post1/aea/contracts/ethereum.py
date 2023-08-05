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

"""The base ethereum contract."""

from typing import Any, Dict, Optional, cast

from web3.contract import Contract as EthereumContract

from aea.configurations.base import ContractConfig
from aea.contracts.base import Contract as BaseContract
from aea.crypto.base import LedgerApi
from aea.crypto.ethereum import EthereumApi


class Contract(BaseContract):
    """Definition of an ethereum contract."""

    def __init__(
        self, config: ContractConfig, contract_interface: Dict[str, Any],
    ):
        """
        Initialize the contract.

        :param config: the contract configurations.
        :param contract_interface: the contract interface.
        """
        super().__init__(config, contract_interface)
        self._abi = contract_interface["abi"]
        self._bytecode = contract_interface["bytecode"]
        self._instance = None  # type: Optional[EthereumContract]

    @property
    def abi(self) -> Dict[str, Any]:
        """Get the abi."""
        return self._abi

    @property
    def bytecode(self) -> bytes:
        """Get the bytecode."""
        return self._bytecode

    @property
    def instance(self) -> EthereumContract:
        """Get the contract instance."""
        assert self._instance is not None, "Instance not set!"
        return self._instance

    @property
    def is_deployed(self) -> bool:
        """Check if the contract is deployed."""
        return self.instance.address is not None

    def set_instance(self, ledger_api: LedgerApi) -> None:
        """
        Set the instance.

        :param ledger_api: the ledger api we are using.
        :return: None
        """
        assert self._instance is None, "Instance already set!"
        ledger_api = cast(EthereumApi, ledger_api)
        self._instance = ledger_api.api.eth.contract(
            abi=self.abi, bytecode=self.bytecode
        )

    def set_address(self, ledger_api: LedgerApi, contract_address: str) -> None:
        """
        Set the contract address.

        :param ledger_api: the ledger_api we are using.
        :param contract_address: the contract address
        :return: None
        """
        if self._instance is not None:
            assert self.instance.address is None, "Address already set!"
        ledger_api = cast(EthereumApi, ledger_api)
        self._instance = ledger_api.api.eth.contract(
            address=contract_address, abi=self.abi
        )

    def set_deployed_instance(
        self, ledger_api: LedgerApi, contract_address: str
    ) -> None:
        """
        Set the contract address.

        :param ledger_api: the ledger_api we are using.
        :param contract_address: the contract address
        :return: None
        """
        assert self._instance is None, "Instance already set!"
        ledger_api = cast(EthereumApi, ledger_api)
        self._instance = ledger_api.api.eth.contract(
            address=contract_address, abi=self._abi, bytecode=self.bytecode
        )
