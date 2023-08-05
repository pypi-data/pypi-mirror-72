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
from unittest.mock import patch

from .test_base import create_app


@patch("aea.cli_gui.cli_add_item")
@patch("aea.cli_gui.try_to_load_agent_config")
def test_add_item(*mocks):
    """Test remove a skill/connection/protocol.

    Actually we just do connection as code coverage is the same.
    """
    app = create_app()

    agent_name = "test_agent_id"
    connection_id = "author/test_connection:0.1.0"

    # Ensure there is now one agent
    response_remove = app.post(
        "api/agent/" + agent_name + "/connection",
        content_type="application/json",
        data=json.dumps(connection_id),
    )
    assert response_remove.status_code == 201
    data = json.loads(response_remove.get_data(as_text=True))
    assert data == agent_name


def test_delete_agent_fail():
    """Test remove a skill/connection/protocol when it fails.

    Actually we just do connection as code coverage is the same.
    """
    app = create_app()

    agent_name = "test_agent_id"
    connection_id = "author/test_connection:0.1.0"

    def _dummy_call_aea(param_list, dir):
        assert param_list[0] == sys.executable
        assert param_list[1] == "-m"
        assert param_list[2] == "aea.cli"
        assert param_list[3] == "add"
        assert param_list[4] == "--local"
        assert param_list[5] == "connection"
        assert param_list[6] == connection_id
        assert agent_name in dir
        return 1

    with patch("aea.cli_gui._call_aea", _dummy_call_aea):
        # Ensure there is now one agent
        response_remove = app.post(
            "api/agent/" + agent_name + "/connection",
            content_type="application/json",
            data=json.dumps(connection_id),
        )
    assert response_remove.status_code == 400
    data = json.loads(response_remove.get_data(as_text=True))
    assert data["detail"] == "Failed to add connection {} to agent {}".format(
        connection_id, agent_name
    )
