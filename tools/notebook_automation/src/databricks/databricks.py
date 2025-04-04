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
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .api import DatabricksAPIEndpoints


class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"


@dataclass
class DatabricksPlatform:
    """Manages Databricks cluster operations"""

    config: dict[str, Any] = field(default_factory=dict, init=True)
    logger: logging.Logger = field(default=None, init=True)
    api: DatabricksAPIEndpoints = field(default=None, init=False)
    headers: dict[str, str] = field(default_factory=dict, init=False)
    csp: CloudProvider = field(default=None, init=False)

    def __post_init__(self):
        workspace_url = self.config["databricks"]["workspace_url"]
        self.api = DatabricksAPIEndpoints(workspace_url)
        self.csp = self._determine_csp(workspace_url)
        self.headers = {
            "Authorization": f"Bearer {self.config['databricks']['token']}",
            "Content-Type": "application/json",
        }

    def _determine_csp(self, workspace_url: str) -> CloudProvider:
        """Determine the cloud service provider based on workspace URL"""
        if "azuredatabricks.net" in workspace_url:
            return CloudProvider.AZURE
        elif "databricks.com" in workspace_url:
            return CloudProvider.AWS
        else:
            raise ValueError(f"Could not determine CSP from workspace URL: {workspace_url}")
