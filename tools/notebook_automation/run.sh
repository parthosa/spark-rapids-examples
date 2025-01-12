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
    echo "Usage: $0 <path_to_config_file>"
    exit 1
fi

CONFIG_FILE="$1"

if [[ ! -f $CONFIG_FILE ]]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found."
    exit 1
fi

echo "Running notebook automation with configuration file: $CONFIG_FILE"
python src/main.py "$CONFIG_FILE"

if [[ $? -eq 0 ]]; then
    echo "Notebook automation completed successfully."
else
    echo "Notebook automation encountered an error."
    exit 1
fi
