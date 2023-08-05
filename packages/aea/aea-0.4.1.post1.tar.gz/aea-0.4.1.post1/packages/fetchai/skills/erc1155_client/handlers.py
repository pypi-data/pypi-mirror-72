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

"""This package contains handlers for the erc1155-client skill."""

from typing import Dict, Optional, Tuple, cast

from aea.configurations.base import ProtocolId
from aea.decision_maker.messages.transaction import TransactionMessage
from aea.helpers.dialogue.base import DialogueLabel
from aea.protocols.base import Message
from aea.protocols.default.message import DefaultMessage
from aea.skills.base import Handler

from packages.fetchai.contracts.erc1155.contract import ERC1155Contract
from packages.fetchai.protocols.fipa.message import FipaMessage
from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.erc1155_client.dialogues import Dialogue, Dialogues
from packages.fetchai.skills.erc1155_client.strategy import Strategy


class FIPAHandler(Handler):
    """This class implements a FIPA handler."""

    SUPPORTED_PROTOCOL = FipaMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """
        Implement the setup.

        :return: None
        """
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

        # handle message
        if fipa_msg.performative == FipaMessage.Performative.PROPOSE:
            self._handle_propose(fipa_msg, fipa_dialogue)

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

    def _handle_propose(self, msg: FipaMessage, dialogue: Dialogue) -> None:
        """
        Handle the propose.

        :param msg: the message
        :param dialogue: the dialogue object
        :return: None
        """
        data = msg.proposal.values

        if all(
            key
            in [
                "contract_address",
                "from_supply",
                "to_supply",
                "value",
                "trade_nonce",
                "token_id",
            ]
            for key in data.keys()
        ):
            # accept any proposal with the correct keys
            self.context.logger.info(
                "[{}]: received valid PROPOSE from sender={}: proposal={}".format(
                    self.context.agent_name, msg.counterparty[-5:], data
                )
            )
            contract = cast(ERC1155Contract, self.context.contracts.erc1155)
            strategy = cast(Strategy, self.context.strategy)
            contract.set_address(
                ledger_api=self.context.ledger_apis.get_api(strategy.ledger_id),
                contract_address=data["contract_address"],
            )
            tx_msg = contract.get_hash_single_transaction_msg(
                from_address=msg.counterparty,
                to_address=self.context.agent_address,
                token_id=int(data["token_id"]),
                from_supply=int(data["from_supply"]),
                to_supply=int(data["to_supply"]),
                value=int(data["value"]),
                trade_nonce=int(data["trade_nonce"]),
                ledger_api=self.context.ledger_apis.get_api(strategy.ledger_id),
                skill_callback_id=self.context.skill_id,
                info={"dialogue_label": dialogue.dialogue_label.json},
            )
            self.context.logger.debug(
                "[{}]: sending transaction to decision maker for signing. tx_msg={}".format(
                    self.context.agent_name, tx_msg
                )
            )
            self.context.decision_maker_message_queue.put_nowait(tx_msg)
        else:
            self.context.logger.info(
                "[{}]: received invalid PROPOSE from sender={}: proposal={}".format(
                    self.context.agent_name, msg.counterparty[-5:], data
                )
            )


class OEFSearchHandler(Handler):
    """This class implements an OEF search handler."""

    SUPPORTED_PROTOCOL = OefSearchMessage.protocol_id  # type: Optional[ProtocolId]

    def setup(self) -> None:
        """Call to setup the handler."""
        pass

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.

        :param message: the message
        :return: None
        """
        # convenience representations
        oef_msg = cast(OefSearchMessage, message)
        if oef_msg.performative is OefSearchMessage.Performative.SEARCH_RESULT:
            agents = oef_msg.agents
            self._handle_search(agents)

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass

    def _handle_search(self, agents: Tuple[str, ...]) -> None:
        """
        Handle the search response.

        :param agents: the agents returned by the search
        :return: None
        """
        if len(agents) > 0:
            self.context.logger.info(
                "[{}]: found agents={}, stopping search.".format(
                    self.context.agent_name, list(map(lambda x: x[-5:], agents))
                )
            )
            strategy = cast(Strategy, self.context.strategy)
            # stopping search
            strategy.is_searching = False
            # pick first agent found
            opponent_addr = agents[0]
            dialogues = cast(Dialogues, self.context.dialogues)
            query = strategy.get_service_query()
            cfp_msg = FipaMessage(
                message_id=Dialogue.STARTING_MESSAGE_ID,
                dialogue_reference=dialogues.new_self_initiated_dialogue_reference(),
                performative=FipaMessage.Performative.CFP,
                target=Dialogue.STARTING_TARGET,
                query=query,
            )
            cfp_msg.counterparty = opponent_addr
            dialogues.update(cfp_msg)
            self.context.logger.info(
                "[{}]: sending CFP to agent={}".format(
                    self.context.agent_name, opponent_addr[-5:]
                )
            )
            self.context.outbox.put_message(message=cfp_msg)
        else:
            self.context.logger.info(
                "[{}]: found no agents, continue searching.".format(
                    self.context.agent_name
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
        if (
            tx_msg_response.performative
            == TransactionMessage.Performative.SUCCESSFUL_SIGNING
            and (
                tx_msg_response.tx_id
                == ERC1155Contract.Performative.CONTRACT_SIGN_HASH_SINGLE.value
            )
        ):
            tx_signature = tx_msg_response.signed_payload.get("tx_signature")
            dialogue_label = DialogueLabel.from_json(
                cast(Dict[str, str], tx_msg_response.info.get("dialogue_label"))
            )
            dialogues = cast(Dialogues, self.context.dialogues)
            dialogue = dialogues.dialogues[dialogue_label]
            fipa_msg = cast(FipaMessage, dialogue.last_incoming_message)
            new_message_id = fipa_msg.message_id + 1
            new_target = fipa_msg.message_id
            counterparty_addr = dialogue.dialogue_label.dialogue_opponent_addr
            inform_msg = FipaMessage(
                message_id=new_message_id,
                dialogue_reference=dialogue.dialogue_label.dialogue_reference,
                target=new_target,
                performative=FipaMessage.Performative.ACCEPT_W_INFORM,
                info={"tx_signature": tx_signature},
            )
            inform_msg.counterparty = counterparty_addr
            self.context.logger.info(
                "[{}]: sending ACCEPT_W_INFORM to agent={}: tx_signature={}".format(
                    self.context.agent_name, counterparty_addr[-5:], tx_signature
                )
            )
            self.context.outbox.put_message(message=inform_msg)
        else:
            self.context.logger.info(
                "[{}]: signing failed: tx_msg_response={}".format(
                    self.context.agent_name, tx_msg_response
                )
            )

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass
