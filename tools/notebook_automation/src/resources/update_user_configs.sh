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

# Initialize variables
INPUT_FILE=""
OUTPUT_FILE=""

# Parse named arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--input)
            INPUT_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 -i|--input <input_template_file> -o|--output <output_file>"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$INPUT_FILE" || -z "$OUTPUT_FILE" ]]; then
    echo "Error: Both input and output files must be specified"
    echo "Usage: $0 -i|--input <input_template_file> -o|--output <output_file>"
    exit 1
fi

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

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file $INPUT_FILE not found"
    exit 1
fi

if ! command -v yq &> /dev/null; then
    echo "Error: yq is not installed. Please install yq to run this script."
    echo "You can install it using:"
    echo "  brew install yq     # On macOS"
    echo "  apt install yq      # On Ubuntu/Debian"
    echo "  or visit https://github.com/mikefarah/yq for other options"
    exit 1
fi

temp_file=$(mktemp)

# Copy input file to temp file, preserving header comments
cp "$INPUT_FILE" "$temp_file"

# Update YAML values using yq
yq -i eval "
  .databricks.workspace_url = \"$WORKSPACE_URL\" |
  .databricks.token = \"$DATABRICKS_TOKEN\" |
  .github.repo_url = \"$REPO_URL\" |
  .github.branch = \"$BRANCH\" |
  .github.notebook_path = \"$NOTEBOOK_PATH\" |
  .workspace.import_path = \"$IMPORT_PATH\" |
  .cluster.default_config.spark_version = \"$SPARK_VERSION\" |
  .cluster.default_config.node_type_id = \"$NODE_TYPE_ID\" |
  .notebook.parameters.[\"Tools Version\"] = \"$TOOLS_VERSION\" |
  .notebook.parameters.[\"Eventlog Path\"] = \"$EVENTLOG_PATH\"
" "$temp_file"

# Check if yq command was successful
if [ $? -eq 0 ]; then
    mv "$temp_file" "$OUTPUT_FILE"
    echo "Configuration updated successfully and saved to $OUTPUT_FILE"
else
    rm "$temp_file"
    echo "Error: Failed to update configuration"
    exit 1
fi
