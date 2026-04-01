#!/bin/bash
set -euo pipefail

# Install Python dependencies using uv with Python 3.12
# The cloud image defaults to Python 3.11 but the project requires >=3.12
if [ ! -d "$CLAUDE_PROJECT_DIR/.venv" ]; then
  uv sync --python python3.12 --project "$CLAUDE_PROJECT_DIR"
else
  # Re-sync only if lockfile is newer than venv
  if [ "$CLAUDE_PROJECT_DIR/uv.lock" -nt "$CLAUDE_PROJECT_DIR/.venv" ]; then
    uv sync --python python3.12 --project "$CLAUDE_PROJECT_DIR"
  fi
fi
