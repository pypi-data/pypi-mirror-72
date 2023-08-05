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

"""This package contains the dataModel for the weather agent."""

from aea.helpers.search.models import Attribute, DataModel

SCHEME = {"country": "UK", "city": "Cambridge"}


class Thermometer_Datamodel(DataModel):
    """Data model for the thermo Agent."""

    def __init__(self):
        """Initialise the dataModel."""
        self.attribute_country = Attribute("country", str, True)
        self.attribute_city = Attribute("city", str, True)

        super().__init__(
            "thermometer_datamodel", [self.attribute_country, self.attribute_city]
        )
