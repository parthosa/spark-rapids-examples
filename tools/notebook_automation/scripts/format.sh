#!/bin/bash

# Exit on error
set -e

# Get the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Get the project root directory (parent of scripts directory)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "Running code formatters and linters..."

# Change to project root
cd "$PROJECT_ROOT"

# Run isort to sort imports
echo "Running isort..."
isort .

# Run black for code formatting
echo "Running black..."
black .

# Run ruff for linting and auto-fixing
echo "Running ruff..."
ruff check . --fix

echo "All done! 🎉" 