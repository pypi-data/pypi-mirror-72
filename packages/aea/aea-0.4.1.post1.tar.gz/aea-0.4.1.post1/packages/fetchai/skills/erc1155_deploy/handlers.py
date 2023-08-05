# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
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

"""This package contains the handlers of the erc1155 deploy skill AEA."""

import time
from typing import Optional, cast

from aea.configurations.base import ProtocolId
from aea.decision_maker.messages.transaction import TransactionMessage
from aea.helpers.search.models import Description
from aea.protocols.base import Message
from aea.protocols.default.message import DefaultMessage
from aea.skills.base import Handler

from packages.fetchai.contracts.erc1155.contract import ERC1155Contract
from packages.fetchai.protocols.fipa.message import FipaMessage
from packages.fetchai.skills.erc1155_deploy.dialogues import Dialogue, Dialogues
from packages.fetchai.skills.erc1155_deploy.strategy import Strategy


class FIPAHandler(Handler):
    """This class implements a FIPA handler."""

    SUPPORTED_PROTOCOL = FipaMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """Implement the setup for the handler."""
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        fipa_msg = cast(FipaMessage, message)

        # recover dialogue
        dialogues = cast(Dialogues, self.context.dialogues)
        fipa_dialogue = cast(Dialogue, dialogues.update(fipa_msg))
        if fipa_dialogue is None:
            self._handle_unidentified_dialogue(fipa_msg)
            return

        if fipa_msg.performative == FipaMessage.Performative.CFP:
            self._handle_cfp(fipa_msg, fipa_dialogue)
        elif fipa_msg.performative == FipaMessage.Performative.ACCEPT_W_INFORM:
            self._handle_accept_w_inform(fipa_msg, fipa_dialogue)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass

    def _handle_unidentified_dialogue(self, msg: FipaMessage) -> None:
        """
        Handle an unidentified dialogue.

        Respond to the sender with a default message containing the appropriate error information.

        :param msg: the message
        :return: None
        """
        self.context.logger.info(
            "[{}]: unidentified dialogue.".format(self.context.agent_name)
        )
        default_msg = DefaultMessage(
            dialogue_reference=("", ""),
            message_id=1,
            target=0,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"fipa_message": msg.encode()},
        )
        default_msg.counterparty = msg.counterparty
        self.context.outbox.put_message(message=default_msg)

    def _handle_cfp(self, msg: FipaMessage, dialogue: Dialogue) -> None:
        """
        Handle the CFP.

        If the CFP matches the supplied services then send a PROPOSE, otherwise send a DECLINE.

        :param msg: the message
        :param dialogue: the dialogue object
        :return: None
        """
        new_message_id = msg.message_id + 1
        new_target = msg.message_id
        self.context.logger.info(
            "[{}]: received CFP from sender={}".format(
                self.context.agent_name, msg.counterparty[-5:]
            )
        )
        if self.context.behaviours.service_registration.is_items_minted:
            # simply send the same proposal, independent of the query
            strategy = cast(Strategy, self.context.strategy)
            contract = cast(ERC1155Contract, self.context.contracts.erc1155)
            trade_nonce = contract.generate_trade_nonce(self.context.agent_address)
            token_id = self.context.behaviours.service_registration.token_ids[0]
            proposal = Description(
                {
                    "contract_address": contract.instance.address,
                    "token_id": str(token_id),
                    "trade_nonce": str(trade_nonce),
                    "from_supply": str(strategy.from_supply),
                    "to_supply": str(strategy.to_supply),
                    "value": str(strategy.value),
                }
            )
            dialogue.proposal = proposal
            proposal_msg = FipaMessage(
                message_id=new_message_id,
                dialogue_reference=dialogue.dialogue_label.dialogue_reference,
                target=new_target,
                performative=FipaMessage.Performative.PROPOSE,
                proposal=proposal,
            )
            proposal_msg.counterparty = msg.counterparty
            dialogue.update(proposal_msg)
            self.context.logger.info(
                "[{}]: Sending PROPOSE to agent={}: proposal={}".format(
                    self.context.agent_name, msg.counterparty[-5:], proposal.values
                )
            )
            self.context.outbox.put_message(message=proposal_msg)
        else:
            self.context.logger.info("Contract items not minted yet. Try again later.")

    def _handle_accept_w_inform(self, msg: FipaMessage, dialogue: Dialogue) -> None:
        """
        Handle the ACCEPT_W_INFORM.

        If the ACCEPT_W_INFORM message contains the signed transaction, sign it too, otherwise do nothing.

        :param msg: the message
        :param dialogue: the dialogue object
        :return: None
        """
        tx_signature = msg.info.get("tx_signature", None)
        if tx_signature is not None:
            self.context.logger.info(
                "[{}]: received ACCEPT_W_INFORM from sender={}: tx_signature={}".format(
                    self.context.agent_name, msg.counterparty[-5:], tx_signature
                )
            )
            contract = cast(ERC1155Contract, self.context.contracts.erc1155)
            strategy = cast(Strategy, self.context.strategy)
            tx = contract.get_atomic_swap_single_transaction_msg(
                from_address=self.context.agent_address,
                to_address=msg.counterparty,
                token_id=int(dialogue.proposal.values["token_id"]),
                from_supply=int(dialogue.proposal.values["from_supply"]),
                to_supply=int(dialogue.proposal.values["to_supply"]),
                value=int(dialogue.proposal.values["value"]),
                trade_nonce=int(dialogue.proposal.values["trade_nonce"]),
                ledger_api=self.context.ledger_apis.get_api(strategy.ledger_id),
                skill_callback_id=self.context.skill_id,
                signature=tx_signature,
            )
            self.context.logger.debug(
                "[{}]: sending single atomic swap to decision maker.".format(
                    self.context.agent_name
                )
            )
            self.context.decision_maker_message_queue.put(tx)
        else:
            self.context.logger.info(
                "[{}]: received ACCEPT_W_INFORM from sender={} with no signature.".format(
                    self.context.agent_name, msg.counterparty[-5:]
                )
            )


class TransactionHandler(Handler):
    """Implement the transaction handler."""

    SUPPORTED_PROTOCOL = TransactionMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """Implement the setup for the handler."""
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        tx_msg_response = cast(TransactionMessage, message)
        contract = cast(ERC1155Contract, self.context.contracts.erc1155)
        strategy = cast(Strategy, self.context.strategy)
        if tx_msg_response.tx_id == contract.Performative.CONTRACT_DEPLOY.value:
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            tx_digest = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).send_signed_transaction(tx_signed=tx_signed)
            # TODO; handle case when no tx_digest returned and remove loop
            assert tx_digest is not None, "Error when submitting tx."
            while not self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).is_transaction_settled(tx_digest):
                time.sleep(3.0)
            tx_receipt = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).get_transaction_receipt(tx_digest=tx_digest)
            if tx_receipt is None:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to get tx receipt for deploy. Aborting...".format(
                        self.context.agent_name
                    )
                )
            elif tx_receipt.status != 1:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to deploy. Aborting...".format(
                        self.context.agent_name
                    )
                )
            else:
                contract.set_address(
                    self.context.ledger_apis.get_api(strategy.ledger_id),
                    tx_receipt.contractAddress,
                )
                self.context.logger.info(
                    "[{}]: Successfully deployed the contract. Transaction digest: {}".format(
                        self.context.agent_name, tx_digest
                    )
                )

        elif tx_msg_response.tx_id == contract.Performative.CONTRACT_CREATE_BATCH.value:
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            tx_digest = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).send_signed_transaction(tx_signed=tx_signed)
            # TODO; handle case when no tx_digest returned and remove loop
            assert tx_digest is not None, "Error when submitting tx."
            while not self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).is_transaction_settled(tx_digest):
                time.sleep(3.0)
            tx_receipt = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).get_transaction_receipt(tx_digest=tx_digest)
            if tx_receipt is None:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to get tx receipt for create items. Aborting...".format(
                        self.context.agent_name
                    )
                )
            elif tx_receipt.status != 1:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to create items. Aborting...".format(
                        self.context.agent_name
                    )
                )
            else:
                self.context.behaviours.service_registration.is_items_created = True
                self.context.logger.info(
                    "[{}]: Successfully created items. Transaction digest: {}".format(
                        self.context.agent_name, tx_digest
                    )
                )
        elif tx_msg_response.tx_id == contract.Performative.CONTRACT_MINT_BATCH.value:
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            tx_digest = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).send_signed_transaction(tx_signed=tx_signed)
            # TODO; handle case when no tx_digest returned and remove loop
            assert tx_digest is not None, "Error when submitting tx."
            while not self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).is_transaction_settled(tx_digest):
                time.sleep(3.0)
            tx_receipt = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).get_transaction_receipt(tx_digest=tx_digest)
            if tx_receipt is None:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to get tx receipt for mint items. Aborting...".format(
                        self.context.agent_name
                    )
                )
            elif tx_receipt.status != 1:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to mint items. Aborting...".format(
                        self.context.agent_name
                    )
                )
            else:
                self.context.behaviours.service_registration.is_items_minted = True
                self.context.logger.info(
                    "[{}]: Successfully minted items. Transaction digest: {}".format(
                        self.context.agent_name, tx_digest
                    )
                )
                result = contract.get_balances(
                    address=self.context.agent_address,
                    token_ids=self.context.behaviours.service_registration.token_ids,
                )
                self.context.logger.info(
                    "[{}]: Current balances: {}".format(self.context.agent_name, result)
                )
        elif (
            tx_msg_response.tx_id
            == contract.Performative.CONTRACT_ATOMIC_SWAP_SINGLE.value
        ):
            tx_signed = tx_msg_response.signed_payload.get("tx_signed")
            tx_digest = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).send_signed_transaction(tx_signed=tx_signed)
            # TODO; handle case when no tx_digest returned and remove loop
            assert tx_digest is not None, "Error when submitting tx."
            while not self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).is_transaction_settled(tx_digest):
                time.sleep(3.0)
            tx_receipt = self.context.ledger_apis.get_api(
                strategy.ledger_id
            ).get_transaction_receipt(tx_digest=tx_digest)
            if tx_receipt is None:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to get tx receipt for atomic swap. Aborting...".format(
                        self.context.agent_name
                    )
                )
            elif tx_receipt.status != 1:
                self.context.is_active = False
                self.context.logger.info(
                    "[{}]: Failed to conduct atomic swap. Aborting...".format(
                        self.context.agent_name
                    )
                )
            else:
                self.context.logger.info(
                    "[{}]: Successfully conducted atomic swap. Transaction digest: {}".format(
                        self.context.agent_name, tx_digest
                    )
                )
                result = contract.get_balances(
                    address=self.context.agent_address,
                    token_ids=self.context.behaviours.service_registration.token_ids,
                )
                self.context.logger.info(
                    "[{}]: Current balances: {}".format(self.context.agent_name, result)
                )

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass
