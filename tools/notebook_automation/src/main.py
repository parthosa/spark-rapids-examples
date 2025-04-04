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
import sys
from enum import Enum

from core.config import ConfigLoader
from modes import create_cluster, delete_cluster, run_notebook
from utils.logger import setup_logging


class Mode(Enum):
    CREATE_CLUSTER = "create_cluster"
    RUN_NOTEBOOK = "run_notebook"
    DELETE_CLUSTER = "delete_cluster"


def main(user_config_path: str, mode: str, platform: str = "databricks") -> None:
    """
    Main entry point for the notebook automation tool.

    Args:
        user_config_path: Path to the user configuration file
        mode: Operation mode (create_cluster, run_notebook, or delete_cluster)
        platform: Platform to use (currently only databricks is supported)
    """
    logger = setup_logging()

    try:
        # Load configuration
        config = ConfigLoader.load_config(user_config_path, platform)
        if mode == Mode.CREATE_CLUSTER.value:
            create_cluster(config, logger)
        elif mode == Mode.RUN_NOTEBOOK.value:
            run_notebook(config, logger)
        elif mode == Mode.DELETE_CLUSTER.value:
            delete_cluster(config, logger)
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be one of {[m.value for m in Mode]}")

    except Exception as e:
        logger.error(f"Error in notebook execution: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <path_to_user_config> <mode>")
        print(f"Available modes: {[m.value for m in Mode]}")
        sys.exit(1)

    user_config_path = sys.argv[1]
    mode = sys.argv[2]

    if not os.path.exists(user_config_path):
        print(f"Configuration file not found: {user_config_path}")
        sys.exit(1)

    if not user_config_path.endswith(".yaml"):
        print("Configuration file must be a YAML file")
        sys.exit(1)

    main(user_config_path, mode)
