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

from typing import Dict
from dataclasses import dataclass, field

@dataclass
class DatabricksAPIEndpoints:
    """Manages all Databricks API endpoints"""
    domain: str = field(default=None, init=True)

    def __post_init__(self):
        self.domain = self.domain.rstrip('/')
        
    @property
    def clusters(self) -> Dict[str, str]:
        return {
            'create': f"{self.domain}/api/2.0/clusters/create",
            'get': f"{self.domain}/api/2.0/clusters/get",
            'delete': f"{self.domain}/api/2.0/clusters/delete"
        }
    
    @property
    def jobs(self) -> Dict[str, str]:
        return {
            'submit_run': f"{self.domain}/api/2.0/jobs/runs/submit",
            'get_run': f"{self.domain}/api/2.0/jobs/runs/get",
            'get_output': f"{self.domain}/api/2.0/jobs/runs/get-output"
        }
    
    @property
    def workspace(self) -> Dict[str, str]:
        return {
            'import': f"{self.domain}/api/2.0/workspace/import",
            'get_status': f"{self.domain}/api/2.0/workspace/get-status",
            'delete': f"{self.domain}/api/2.0/workspace/delete"
        }
