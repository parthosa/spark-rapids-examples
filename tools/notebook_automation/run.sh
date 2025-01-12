#!/bin/bash

# Check if a configuration file is provided as an argument
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <path_to_config_file>"
    exit 1
fi

CONFIG_FILE="$1"

# Check if the specified configuration file exists
if [[ ! -f $CONFIG_FILE ]]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found."
    exit 1
fi

# Run the Python script
echo "Running notebook automation with configuration file: $CONFIG_FILE"
python src/main.py "$CONFIG_FILE"

# Check if the command succeeded
if [[ $? -eq 0 ]]; then
    echo "Notebook automation completed successfully."
else
    echo "Notebook automation encountered an error."
    exit 1
fi
