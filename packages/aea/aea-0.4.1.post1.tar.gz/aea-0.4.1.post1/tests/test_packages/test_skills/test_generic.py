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
"""This test module contains the integration test for the generic buyer and seller skills."""
import pytest

from aea.test_tools.test_cases import AEATestCaseMany, UseOef

from ...conftest import FUNDED_FET_PRIVATE_KEY_1, MAX_FLAKY_RERUNS


class TestGenericSkills(AEATestCaseMany, UseOef):
    """Test that generic skills work."""

    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)  # cause possible network issues
    def test_generic(self, pytestconfig):
        """Run the generic skills sequence."""
        seller_aea_name = "my_generic_seller"
        buyer_aea_name = "my_generic_buyer"
        self.create_agents(seller_aea_name, buyer_aea_name)

        # prepare seller agent
        self.set_agent_context(seller_aea_name)
        self.add_item("connection", "fetchai/oef:0.4.0")
        self.set_config("agent.default_connection", "fetchai/oef:0.4.0")
        self.add_item("skill", "fetchai/generic_seller:0.5.0")
        setting_path = (
            "vendor.fetchai.skills.generic_seller.models.strategy.args.is_ledger_tx"
        )
        self.set_config(setting_path, False, "bool")
        self.run_install()

        # prepare buyer agent
        self.set_agent_context(buyer_aea_name)
        self.add_item("connection", "fetchai/oef:0.4.0")
        self.set_config("agent.default_connection", "fetchai/oef:0.4.0")
        self.add_item("skill", "fetchai/generic_buyer:0.4.0")
        setting_path = (
            "vendor.fetchai.skills.generic_buyer.models.strategy.args.is_ledger_tx"
        )
        self.set_config(setting_path, False, "bool")
        self.run_install()

        # run AEAs
        self.set_agent_context(seller_aea_name)
        seller_aea_process = self.run_agent("--connections", "fetchai/oef:0.4.0")

        self.set_agent_context(buyer_aea_name)
        buyer_aea_process = self.run_agent("--connections", "fetchai/oef:0.4.0")

        check_strings = (
            "updating generic seller services on OEF service directory.",
            "unregistering generic seller services from OEF service directory.",
            "received CFP from sender=",
            "sending a PROPOSE with proposal=",
            "received ACCEPT from sender=",
            "sending MATCH_ACCEPT_W_INFORM to sender=",
            "received INFORM from sender=",
        )
        missing_strings = self.missing_from_output(
            seller_aea_process, check_strings, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in seller_aea output.".format(missing_strings)

        check_strings = (
            "found agents=",
            "sending CFP to agent=",
            "received proposal=",
            "accepting the proposal from sender=",
            "informing counterparty=",
            "received INFORM from sender=",
            "received the following data=",
        )
        missing_strings = self.missing_from_output(
            buyer_aea_process, check_strings, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in buyer_aea output.".format(missing_strings)

        self.terminate_agents(seller_aea_process, buyer_aea_process)
        assert (
            self.is_successfully_terminated()
        ), "Agents weren't successfully terminated."


class TestGenericSkillsFetchaiLedger(AEATestCaseMany, UseOef):
    """Test that generic skills work."""

    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS)  # cause possible network issues
    def test_generic(self, pytestconfig):
        """Run the generic skills sequence."""
        seller_aea_name = "my_generic_seller"
        buyer_aea_name = "my_generic_buyer"
        self.create_agents(seller_aea_name, buyer_aea_name)

        ledger_apis = {"fetchai": {"network": "testnet"}}

        # prepare seller agent
        self.set_agent_context(seller_aea_name)
        self.force_set_config("agent.ledger_apis", ledger_apis)
        self.add_item("connection", "fetchai/oef:0.4.0")
        self.set_config("agent.default_connection", "fetchai/oef:0.4.0")
        self.add_item("skill", "fetchai/generic_seller:0.5.0")
        self.run_install()

        diff = self.difference_to_fetched_agent(
            "fetchai/generic_seller:0.2.0", seller_aea_name
        )
        assert (
            diff == []
        ), "Difference between created and fetched project for files={}".format(diff)

        # prepare buyer agent
        self.set_agent_context(buyer_aea_name)
        self.force_set_config("agent.ledger_apis", ledger_apis)
        self.add_item("connection", "fetchai/oef:0.4.0")
        self.set_config("agent.default_connection", "fetchai/oef:0.4.0")
        self.add_item("skill", "fetchai/generic_buyer:0.4.0")
        self.run_install()

        diff = self.difference_to_fetched_agent(
            "fetchai/generic_buyer:0.2.0", buyer_aea_name
        )
        assert (
            diff == []
        ), "Difference between created and fetched project for files={}".format(diff)

        self.generate_private_key("fetchai")
        self.add_private_key("fetchai", "fet_private_key.txt")
        self.replace_private_key_in_file(
            FUNDED_FET_PRIVATE_KEY_1, "fet_private_key.txt"
        )

        # run AEAs
        self.set_agent_context(seller_aea_name)
        seller_aea_process = self.run_agent("--connections", "fetchai/oef:0.4.0")

        self.set_agent_context(buyer_aea_name)
        buyer_aea_process = self.run_agent("--connections", "fetchai/oef:0.4.0")

        # TODO: finish test once testnet is reliable
        check_strings = (
            "updating generic seller services on OEF service directory.",
            "unregistering generic seller services from OEF service directory.",
            "received CFP from sender=",
            "sending a PROPOSE with proposal=",
            "received ACCEPT from sender=",
            "sending MATCH_ACCEPT_W_INFORM to sender=",
            "received INFORM from sender=",
            "checking whether transaction=",
            "Sending data to sender=",
        )
        missing_strings = self.missing_from_output(
            seller_aea_process, check_strings, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in seller_aea output.".format(missing_strings)

        check_strings = (
            "found agents=",
            "sending CFP to agent=",
            "received proposal=",
            "accepting the proposal from sender=",
            "received MATCH_ACCEPT_W_INFORM from sender=",
            "proposing the transaction to the decision maker. Waiting for confirmation ...",
            "Settling transaction on chain!",
            "transaction was successful.",
            "informing counterparty=",
            "received INFORM from sender=",
            "received the following data=",
        )
        missing_strings = self.missing_from_output(
            buyer_aea_process, check_strings, is_terminating=False
        )
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in buyer_aea output.".format(missing_strings)

        self.terminate_agents(seller_aea_process, buyer_aea_process)
        assert (
            self.is_successfully_terminated()
        ), "Agents weren't successfully terminated."
