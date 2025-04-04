#!/bin/bash

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

# Exit on error
set -e

# Function to clean up state file
cleanup() {
    echo "Cleaning up state file..."
    rm -f cluster_state.json
}

# Set up trap for cleanup on script exit
trap cleanup EXIT

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <config_file>"
    exit 1
fi

CONFIG_FILE="$1"

if [[ ! -f $CONFIG_FILE ]]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found."
    exit 1
fi

echo "Starting notebook automation workflow with configuration file: $CONFIG_FILE"

# Execute each stage of the notebook automation workflow sequentially
echo "Stage 1/3: Creating Databricks cluster..."
python src/main.py "$CONFIG_FILE" create_cluster || {
    echo "Error: Failed to create Databricks cluster"
    exit 1
}

echo "Stage 2/3: Running qualification notebook..."
python src/main.py "$CONFIG_FILE" run_notebook || {
    echo "Error: Failed to execute notebook on cluster"
}

echo "Stage 3/3: Cleaning up cluster resources..."
python src/main.py "$CONFIG_FILE" delete_cluster || {
    echo "Error: Failed to delete cluster"
    exit 1
}

echo "Workflow completed successfully."
