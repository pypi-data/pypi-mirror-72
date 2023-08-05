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

"""This module contains the base message and serialization definition."""

import logging
from copy import copy
from typing import Any, Dict, Optional

from aea.configurations.base import PublicId

logger = logging.getLogger(__name__)


class InternalMessage:
    """This class implements a message."""

    protocol_id = PublicId("fetchai", "internal", "0.1.0")

    def __init__(self, body: Optional[Dict] = None, **kwargs):
        """
        Initialize a Message object.

        :param body: the dictionary of values to hold.
        :param kwargs: any additional value to add to the body. It will overwrite the body values.
        """
        self._body = copy(body) if body else {}  # type: Dict[str, Any]
        self._body.update(kwargs)
        try:
            self._is_consistent()
        except Exception as e:  # pylint: disable=broad-except
            logger.error(e)

    @property
    def body(self) -> Dict:
        """
        Get the body of the message (in dictionary form).

        :return: the body
        """
        return self._body

    @body.setter
    def body(self, body: Dict) -> None:
        """
        Set the body of hte message.

        :param body: the body.
        :return: None
        """
        self._body = body

    def set(self, key: str, value: Any) -> None:
        """
        Set key and value pair.

        :param key: the key.
        :param value: the value.
        :return: None
        """
        self._body[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Get value for key."""
        return self._body.get(key, None)

    def unset(self, key: str) -> None:
        """
        Unset value for key.

        :param key: the key to unset the value of
        """
        self._body.pop(key, None)

    def is_set(self, key: str) -> bool:
        """
        Check value is set for key.

        :param key: the key to check
        """
        return key in self._body

    def _is_consistent(self) -> bool:
        """Check that the data is consistent."""
        return True

    def __eq__(self, other):
        """Compare with another object."""
        return isinstance(other, InternalMessage) and self.body == other.body

    def __str__(self):
        """Get the string representation of the message."""
        return (
            "InternalMessage("
            + " ".join(
                map(
                    lambda key_value: str(key_value[0]) + "=" + str(key_value[1]),
                    self.body.items(),
                )
            )
            + ")"
        )
