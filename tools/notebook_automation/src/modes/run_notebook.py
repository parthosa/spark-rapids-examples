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

import json

from core.notebook import NotebookOrchestrator
from databricks.runner import DatabricksNotebookRunner
from databricks.workspace import DatabricksWorkspaceManager
from utils.state_manager import StateManager


def run_notebook(config, logger):
    """
    Runs a notebook on an existing Databricks cluster.

    Args:
        config: Configuration dictionary
        logger: Logger instance

    Returns:
        dict: The result of the notebook execution
    """
    # Get cluster ID from state
    state_manager = StateManager()
    cluster_id = state_manager.get_cluster_id()

    if not cluster_id:
        raise ValueError("No cluster ID found in state. Please run create_cluster mode first.")

    logger.info(f"Using cluster ID: {cluster_id}")

    workspace_manager = DatabricksWorkspaceManager(config, logger)
    orchestrator = NotebookOrchestrator(config, logger, workspace_manager)
    notebook_runner = DatabricksNotebookRunner(config, logger)

    # Import notebook from GitHub
    logger.info("Preparing notebook from GitHub...")
    workspace_path = orchestrator.prepare_notebook()

    # Run notebook
    logger.info("Running notebook...")
    result = notebook_runner.run_notebook(cluster_id=cluster_id, notebook_path=workspace_path)

    logger.info("Run completed successfully!")
    logger.info(f"Run Output: {json.dumps(result['output'], indent=2)}")
    return result
