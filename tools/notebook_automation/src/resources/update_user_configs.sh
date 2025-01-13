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

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <path_to_user_config_file>"
    exit 1
fi

USER_CONFIG_FILE="$1"

# Configs for 'databricks' 
WORKSPACE_URL="${WORKSPACE_URL:-https://adb-2222222222222222.azuredatabricks.net}"
DATABRICKS_TOKEN="${DATABRICKS_TOKEN:-dapi22222222222222222222}"
# Configs for 'github'
REPO_URL="${REPO_URL:-https://github.com/NVIDIA/spark-rapids-examples}"
BRANCH="${BRANCH:-main}"
NOTEBOOK_PATH="${NOTEBOOK_PATH:-tools/databricks/[RAPIDS Accelerator for Apache Spark] Qualification Tool Notebook Template.ipynb}"
# Configs for 'workspace'
IMPORT_PATH="${IMPORT_PATH:-/Workspace/new/path/to/user/home/}"
# Configs for 'cluster'
SPARK_VERSION="${SPARK_VERSION:-13.3.x-scala2.12}"
NODE_TYPE_ID="${NODE_TYPE_ID:-Standard_DS3_v2}"
# Configs for 'notebook parameters'
TOOLS_VERSION="${TOOLS_VERSION:-24.12.0}"
EVENTLOG_PATH="${EVENTLOG_PATH:-dbfs:/new/path/to/eventlog}"


if [ ! -f "$USER_CONFIG_FILE" ]; then
    echo "Error: Input file $USER_CONFIG_FILE not found"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to run this script."
    exit 1
fi

temp_file=$(mktemp)

jq \
  --arg workspace_url "$WORKSPACE_URL" \
  --arg token "$DATABRICKS_TOKEN" \
  --arg repo_url "$REPO_URL" \
  --arg branch "$BRANCH" \
  --arg notebook_path "$NOTEBOOK_PATH" \
  --arg import_path "$IMPORT_PATH" \
  --arg spark_version "$SPARK_VERSION" \
  --arg node_type_id "$NODE_TYPE_ID" \
  --arg tools_version "$TOOLS_VERSION" \
  --arg eventlog_path "$EVENTLOG_PATH" \
  '
  .databricks.workspace_url = $workspace_url |
  .databricks.token = $token |
  .github.repo_url = $repo_url |
  .github.branch = $branch |
  .github.notebook_path = $notebook_path |
  .workspace.import_path = $import_path |
  .cluster.default_config.spark_version = $spark_version |
  .cluster.default_config.node_type_id = $node_type_id |
  .notebook.parameters["Tools Version"] = $tools_version |
  .notebook.parameters["Eventlog Path"] = $eventlog_path
  ' "$USER_CONFIG_FILE" > "$temp_file"

# Check if jq command was successful
if [ $? -eq 0 ]; then
    mv "$temp_file" "$USER_CONFIG_FILE"
    echo "Configuration updated successfully"
else
    rm "$temp_file"
    echo "Error: Failed to update configuration"
    exit 1
fi
