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
"""This test module contains the tests for the `aea gui` sub-commands."""
import json
import sys
import unittest.mock

from aea.test_tools.test_cases import UseOef

from tests.common.utils import wait_for_condition

from .test_base import DummyPID, create_app
from ..common.mocks import ctx_mock_Popen


class TestCreateWithOEF(UseOef):
    """Use OEF to test create."""

    def test_create_and_run_oef(self):
        """Test for running oef, reading TTY and errors."""
        app = create_app()

        pid = DummyPID(None, "A thing of beauty is a joy forever\n", "Testing Error\n")

        def _dummy_call_aea_async(param_list, dir_arg):
            assert param_list[0] == sys.executable
            assert "launch.py" in param_list[1]
            return pid

        with ctx_mock_Popen():
            with unittest.mock.patch(
                "aea.cli_gui._call_aea_async", _dummy_call_aea_async
            ):
                response_start = app.post(
                    "api/oef", data=None, content_type="application/json",
                )
        assert response_start.status_code == 200

        def wait_oef_ready_condition():
            response_status = app.get(
                "api/oef", data=None, content_type="application/json",
            )
            if response_status.status_code != 200:
                return False

            data = json.loads(response_status.get_data(as_text=True))

            if "RUNNING" not in data["status"]:
                return False

            if (
                "A thing of beauty is a joy forever" in data["tty"]
                and "Testing Error" in data["error"]
            ):
                return True

            return False

        wait_for_condition(
            wait_oef_ready_condition,
            timeout=20,
            error_msg="OEF not ready but we waited for it!",
        )

        # get the status if failed
        pid.return_code = 1
        with unittest.mock.patch("aea.cli_gui._call_aea_async", _dummy_call_aea_async):
            response_status = app.get(
                "api/oef", data=None, content_type="application/json",
            )
        assert response_status.status_code == 200
        data = json.loads(response_status.get_data(as_text=True))
        assert "FAILED" in data["status"]

        # get the status if finished
        pid.return_code = 0
        with unittest.mock.patch("aea.cli_gui._call_aea_async", _dummy_call_aea_async):
            response_status = app.get(
                "api/oef", data=None, content_type="application/json",
            )
        assert response_status.status_code == 200
        data = json.loads(response_status.get_data(as_text=True))
        assert "FINISHED" in data["status"]

        # Stop the OEF Node
        with ctx_mock_Popen():
            response_stop = app.delete(
                "api/oef", data=None, content_type="application/json",
            )
        assert response_stop.status_code == 200

        # get the status
        pid.return_code = 0
        with unittest.mock.patch("aea.cli_gui._call_aea_async", _dummy_call_aea_async):
            response_status = app.get(
                "api/oef", data=None, content_type="application/json",
            )
        assert response_status.status_code == 200
        data = json.loads(response_status.get_data(as_text=True))
        assert "NOT_STARTED" in data["status"]

    def test_create_and_run_oef_fail(self):
        """Test for running oef, reading TTY and errors."""
        app = create_app()

        def _dummy_call_aea_async(param_list, dir_arg):
            assert param_list[0] == sys.executable
            assert "launch.py" in param_list[1]
            return None

        with ctx_mock_Popen():
            with unittest.mock.patch(
                "aea.cli_gui._call_aea_async", _dummy_call_aea_async
            ):
                response_start = app.post(
                    "api/oef", data=None, content_type="application/json",
                )
        assert response_start.status_code == 400
