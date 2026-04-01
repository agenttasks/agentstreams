#!/bin/bash

# Only run in remote (cloud) environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

# Install Python dependencies using uv with Python 3.12
# The cloud image defaults to Python 3.11 but the project requires >=3.12
cd "$CLAUDE_PROJECT_DIR"
uv sync --python python3.12 || true

exit 0
