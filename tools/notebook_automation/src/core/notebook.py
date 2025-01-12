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

import os
import logging
from typing import Dict, Any
from dataclasses import dataclass, field

from github.notebook_fetcher import GitHubNotebookFetcher
from databricks.workspace import DatabricksWorkspaceManager

@dataclass
class NotebookOrchestrator:
    """Orchestrates the notebook import and execution process"""
    config: Dict[str, Any] = field(default_factory=dict, init=True)
    logger: logging.Logger = field(default=None, init=True)
    workspace_manager: DatabricksWorkspaceManager = field(default=None, init=True)
        
    def prepare_notebook(self) -> str:
        """Fetch notebook from GitHub and import to Databricks"""
        github_config = self.config['github']
        
        self.logger.info(f"Fetching notebook from GitHub: {github_config['notebook_path']}")
        content = GitHubNotebookFetcher.fetch_notebook_content(
            github_config['repo_url'],
            github_config['notebook_path'],
            github_config['branch']
        )
        
        notebook_name = os.path.basename(github_config['notebook_path'])
        workspace_path = os.path.join(
            self.config['workspace']['import_path'],
            notebook_name
        )
        
        return self.workspace_manager.import_notebook(content, workspace_path)
