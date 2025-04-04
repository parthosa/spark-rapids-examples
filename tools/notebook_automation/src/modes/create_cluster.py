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

from datetime import datetime

from databricks.cluster import DatabricksClusterManager
from utils.state_manager import StateManager


def create_cluster(config, logger):
    """
    Creates a new Databricks cluster and saves its ID to state.

    Args:
        config: Configuration dictionary
        logger: Logger instance

    Returns:
        str: The ID of the created cluster
    """
    cluster_manager = DatabricksClusterManager(config, logger)
    cluster_name = f"{config['cluster']['name_prefix']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    cluster_id = cluster_manager.create_cluster(cluster_name)
    logger.info(f"Created cluster with ID: {cluster_id}")

    # Save cluster ID to state
    state_manager = StateManager()
    state_manager.save_cluster_id(cluster_id)

    return cluster_id
