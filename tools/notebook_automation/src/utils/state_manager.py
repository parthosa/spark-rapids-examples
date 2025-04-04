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
import logging
import os


class StateManager:
    """Manages state between different stages of the notebook automation process."""

    def __init__(self, state_file: str = "cluster_state.json"):
        """
        Initialize the state manager.

        Args:
            state_file: Path to the state file
        """
        self.state_file = state_file
        self.logger = logging.getLogger("NotebookAutomation")

    def save_cluster_id(self, cluster_id: str) -> None:
        """
        Save the cluster ID to the state file.

        Args:
            cluster_id: The cluster ID to save
        """
        state = {"cluster_id": cluster_id}
        with open(self.state_file, "w") as f:
            json.dump(state, f)
        self.logger.info(f"Saved cluster ID {cluster_id} to state file")

    def get_cluster_id(self) -> str | None:
        """
        Retrieve the cluster ID from the state file.

        Returns:
            Optional[str]: The cluster ID if found, None otherwise
        """
        if not os.path.exists(self.state_file):
            return None

        try:
            with open(self.state_file) as f:
                state = json.load(f)
                return state.get("cluster_id")
        except Exception as e:
            self.logger.error(f"Error reading state file: {str(e)}")
            return None

    def clear_state(self) -> None:
        """Clear the state file."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
            self.logger.info("Cleared state file")
