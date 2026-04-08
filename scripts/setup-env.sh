#!/bin/bash
set -euo pipefail

# SessionStart hook: load .env into CLAUDE_ENV_FILE so all
# subsequent Bash commands have access to project secrets.
#
# Configured in .claude/settings.json under hooks.SessionStart.
# The .env file is gitignored — secrets never enter version control.

if [ -z "${CLAUDE_ENV_FILE:-}" ]; then
    exit 0
fi

ENV_FILE="${CLAUDE_PROJECT_DIR:-.}/.env"

if [ -f "$ENV_FILE" ]; then
    # Strip comments and blank lines, export each var
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
        echo "export $line" >> "$CLAUDE_ENV_FILE"
    done < "$ENV_FILE"
fi
