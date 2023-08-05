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

"""This test module contains the integration test for the gym skill."""

import os
import shutil

from aea.test_tools.test_cases import AEATestCaseEmpty

from ...conftest import ROOT_DIR, skip_test_windows


class TestGymSkill(AEATestCaseEmpty):
    """Test that gym skill works."""

    @skip_test_windows
    def test_gym(self):
        """Run the gym skill sequence."""
        self.add_item("skill", "fetchai/gym:0.3.0")
        self.add_item("connection", "fetchai/gym:0.2.0")
        self.run_install()

        # add gyms folder from examples
        gyms_src = os.path.join(ROOT_DIR, "examples", "gym_ex", "gyms")
        gyms_dst = os.path.join(self.agent_name, "gyms")
        shutil.copytree(gyms_src, gyms_dst)

        # change default connection
        setting_path = "agent.default_connection"
        self.set_config(setting_path, "fetchai/gym:0.2.0")

        # change connection config
        setting_path = "vendor.fetchai.connections.gym.config.env"
        self.set_config(setting_path, "gyms.env.BanditNArmedRandom")

        # change number of training steps
        setting_path = "vendor.fetchai.skills.gym.handlers.gym.args.nb_steps"
        self.set_config(setting_path, 20, "int")

        gym_aea_process = self.run_agent("--connections", "fetchai/gym:0.2.0")

        check_strings = (
            "Training starting ...",
            "Training finished. You can exit now via CTRL+C.",
        )
        missing_strings = self.missing_from_output(gym_aea_process, check_strings)
        assert (
            missing_strings == []
        ), "Strings {} didn't appear in agent output.".format(missing_strings)

        assert (
            self.is_successfully_terminated()
        ), "Gym agent wasn't successfully terminated."
