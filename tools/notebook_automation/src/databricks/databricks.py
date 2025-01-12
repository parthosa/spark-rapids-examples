# Copyright (c) 2025, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Dict, Any
from dataclasses import dataclass, field

from .api import DatabricksAPIEndpoints

@dataclass
class DatabricksPlatform:
    """ Manages Databricks cluster operations """
    config: Dict[str, Any] = field(default_factory=dict, init=True)
    logger: logging.Logger = field(default=None, init=True)
    api: DatabricksAPIEndpoints = field(default=None, init=False)
    headers: Dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.api = DatabricksAPIEndpoints(self.config['databricks']['domain'])
        self.headers = {
            'Authorization': f"Bearer {self.config['databricks']['token']}",
            'Content-Type': 'application/json'
        }
