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

DOMAIN="https://adb-2222222222222222.azuredatabricks.net"
TOKEN="dapi22222222222222222222"
IMPORT_PATH="/Workspace/new/path/to/user/home/"
NODE_TYPE_ID="Standard_DS3_v2"
TOOLS_VERSION="25.0.0"
EVENTLOG_PATH="dbfs:/new/path/to/eventlog"


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
  --arg domain "$DOMAIN" \
  --arg token "$TOKEN" \
  --arg import_path "$IMPORT_PATH" \
  --arg node_type_id "$NODE_TYPE_ID" \
  --arg tools_version "$TOOLS_VERSION" \
  --arg eventlog_path "$EVENTLOG_PATH" \
  '
  .databricks.domain = $domain |
  .databricks.token = $token |
  .workspace.import_path = $import_path |
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
