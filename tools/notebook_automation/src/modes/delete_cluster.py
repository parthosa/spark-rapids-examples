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


from databricks.cluster import DatabricksClusterManager
from utils.state_manager import StateManager


def delete_cluster(config, logger):
    """
    Terminates an existing Databricks cluster and cleans up state.

    Args:
        config: Configuration dictionary
        logger: Logger instance
    """
    # Get cluster ID from state
    state_manager = StateManager()
    cluster_id = state_manager.get_cluster_id()

    if not cluster_id:
        raise ValueError("No cluster ID found in state. Please run create_cluster mode first.")

    logger.info(f"Using cluster ID: {cluster_id}")

    cluster_manager = DatabricksClusterManager(config, logger)
    logger.info(f"Terminating cluster {cluster_id}...")
    cluster_manager.terminate_cluster(cluster_id)
    logger.info("Cluster terminated successfully")

    # Clear state after successful deletion
    state_manager.clear_state()
