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

"""This module contains the handler for the 'ml_train' skill."""

import pickle  # nosec
import uuid
from typing import Optional, Tuple, cast

from aea.configurations.base import ProtocolId
from aea.decision_maker.messages.transaction import TransactionMessage
from aea.helpers.search.models import Description
from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.fetchai.protocols.ml_trade.message import MlTradeMessage
from packages.fetchai.protocols.oef_search.message import OefSearchMessage
from packages.fetchai.skills.ml_train.strategy import Strategy


DUMMY_DIGEST = "dummy_digest"


class TrainHandler(Handler):
    """Train handler."""

    SUPPORTED_PROTOCOL = MlTradeMessage.protocol_id

    def setup(self) -> None:
        """
        Set up the handler.

        :return: None
        """
        self.context.logger.debug("Train handler: setup method called.")

    def handle(self, message: Message) -> None:
        """
        Handle messages.

        :param message: the message
        :return: None
        """
        ml_msg = cast(MlTradeMessage, message)
        if ml_msg.performative == MlTradeMessage.Performative.TERMS:
            self._handle_terms(ml_msg)
        elif ml_msg.performative == MlTradeMessage.Performative.DATA:
            self._handle_data(ml_msg)

    def _handle_terms(self, ml_trade_msg: MlTradeMessage) -> None:
        """
        Handle the terms of the request.

        :param ml_trade_msg: the ml trade message
        :return: None
        """
        terms = ml_trade_msg.terms
        self.context.logger.info(
            "Received terms message from {}: terms={}".format(
                ml_trade_msg.counterparty[-5:], terms.values
            )
        )

        strategy = cast(Strategy, self.context.strategy)
        acceptable = strategy.is_acceptable_terms(terms)
        affordable = strategy.is_affordable_terms(terms)
        if not acceptable and affordable:
            self.context.logger.info(
                "[{}]: rejecting, terms are not acceptable and/or affordable".format(
                    self.context.agent_name
                )
            )
            return

        if strategy.is_ledger_tx:
            # propose the transaction to the decision maker for settlement on the ledger
            tx_msg = TransactionMessage(
                performative=TransactionMessage.Performative.PROPOSE_FOR_SETTLEMENT,
                skill_callback_ids=[self.context.skill_id],
                tx_id=strategy.get_next_transition_id(),
                tx_sender_addr=self.context.agent_addresses[terms.values["ledger_id"]],
                tx_counterparty_addr=terms.values["address"],
                tx_amount_by_currency_id={
                    terms.values["currency_id"]: -terms.values["price"]
                },
                tx_sender_fee=terms.values["buyer_tx_fee"],
                tx_counterparty_fee=terms.values["seller_tx_fee"],
                tx_quantities_by_good_id={},
                ledger_id=terms.values["ledger_id"],
                info={"terms": terms, "counterparty_addr": ml_trade_msg.counterparty},
                tx_nonce=uuid.uuid4().hex,
            )  # this is used to send the terms later - because the seller is stateless and must know what terms have been accepted
            self.context.decision_maker_message_queue.put_nowait(tx_msg)
            self.context.logger.info(
                "[{}]: proposing the transaction to the decision maker. Waiting for confirmation ...".format(
                    self.context.agent_name
                )
            )
        else:
            # accept directly with a dummy transaction digest, no settlement
            ml_accept = MlTradeMessage(
                performative=MlTradeMessage.Performative.ACCEPT,
                tx_digest=DUMMY_DIGEST,
                terms=terms,
            )
            ml_accept.counterparty = ml_trade_msg.counterparty
            self.context.outbox.put_message(message=ml_accept)
            self.context.logger.info(
                "[{}]: sending dummy transaction digest ...".format(
                    self.context.agent_name
                )
            )

    def _handle_data(self, ml_trade_msg: MlTradeMessage) -> None:
        """
        Handle the data.

        :param ml_trade_msg: the ml trade message
        :return: None
        """
        terms = ml_trade_msg.terms
        payload = ml_trade_msg.payload
        data = pickle.loads(payload)  # nosec
        if data is None:
            self.context.logger.info(
                "Received data message with no data from {}".format(
                    ml_trade_msg.counterparty[-5:]
                )
            )
        else:
            self.context.logger.info(
                "Received data message from {}: data shape={}, terms={}".format(
                    ml_trade_msg.counterparty[-5:], data[0].shape, terms.values
                )
            )
            # training_task = MLTrainTask(data, self.context.ml_model)
            # self.context.task_manager.enqueue_task(training_task)
            self.context.ml_model.update(data[0], data[1], 5)
            self.context.strategy.is_searching = True

    def teardown(self) -> None:
        """
        Teardown the handler.

        :return: None
        """
        self.context.logger.debug("Train handler: teardown method called.")


class OEFSearchHandler(Handler):
    """The OEF search handler."""

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
        if len(agents) == 0:
            self.context.logger.info(
                "[{}]: found no agents, continue searching.".format(
                    self.context.agent_name
                )
            )
            return

        self.context.logger.info(
            "[{}]: found agents={}, stopping search.".format(
                self.context.agent_name, list(map(lambda x: x[-5:], agents))
            )
        )
        strategy = cast(Strategy, self.context.strategy)
        strategy.is_searching = False
        query = strategy.get_service_query()
        for opponent_address in agents:
            self.context.logger.info(
                "[{}]: sending CFT to agent={}".format(
                    self.context.agent_name, opponent_address[-5:]
                )
            )
            cft_msg = MlTradeMessage(
                performative=MlTradeMessage.Performative.CFP, query=query
            )
            cft_msg.counterparty = opponent_address
            self.context.outbox.put_message(message=cft_msg)


class MyTransactionHandler(Handler):
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
            == TransactionMessage.Performative.SUCCESSFUL_SETTLEMENT
        ):
            self.context.logger.info(
                "[{}]: transaction was successful.".format(self.context.agent_name)
            )
            info = tx_msg_response.info
            terms = cast(Description, info.get("terms"))
            ml_accept = MlTradeMessage(
                performative=MlTradeMessage.Performative.ACCEPT,
                tx_digest=tx_msg_response.tx_digest,
                terms=terms,
            )
            ml_accept.counterparty = tx_msg_response.tx_counterparty_addr
            self.context.outbox.put_message(message=ml_accept)
            self.context.logger.info(
                "[{}]: Sending accept to counterparty={} with transaction digest={} and terms={}.".format(
                    self.context.agent_name,
                    tx_msg_response.tx_counterparty_addr[-5:],
                    tx_msg_response.tx_digest,
                    terms.values,
                )
            )
        else:
            self.context.logger.info(
                "[{}]: transaction was not successful.".format(self.context.agent_name)
            )

    def teardown(self) -> None:
        """
        Implement the handler teardown.

        :return: None
        """
        pass
