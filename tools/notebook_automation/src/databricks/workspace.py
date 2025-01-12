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

import base64
import requests
from dataclasses import dataclass

from .databricks import DatabricksPlatform

@dataclass
class DatabricksWorkspaceManager(DatabricksPlatform):
    """Manages Databricks workspace operations"""

    def import_notebook(self, content: bytes, workspace_path: str) -> str:
        """Import notebook content into Databricks workspace"""
        import_payload = {
            "content": base64.b64encode(content).decode('utf-8'),
            "path": workspace_path,
            "format": "JUPYTER",
            "overwrite": self.config['workspace']['overwrite']
        }
        
        self.logger.info(f"Importing notebook to {workspace_path}")
        response = requests.post(
            self.api.workspace['import'],
            headers=self.headers,
            json=import_payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to import notebook: {response.text}")
            
        return workspace_path
