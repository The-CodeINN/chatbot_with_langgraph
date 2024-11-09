#!/bin/bash
set -e

# Check if OPENAI_API_KEY is set
if [ -z "${OPENAI_API_KEY}" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set"
    exit 1
fi

# Execute the command (defaults to running main.py)
exec uv run python main.py "$@"