#!/usr/bin/env bash
set -euo pipefail

# neon-team-setup.sh — Provision per-developer Neon branches for 3-person team.
#
# For each developer in DEVELOPERS:
#   1. Create a Neon branch dev-{name}
#   2. Create a database role dev_{name} on that branch
#   3. Fetch the connection string
#   4. Apply ontology/schema.sql
#   5. Apply all ontology/migrations/*.sql in order
#
# Usage:
#   NEON_PROJECT_ID=calm-paper-82059121 ./scripts/neon-team-setup.sh
#
# Requires: neonctl (https://neon.tech/docs/reference/neonctl), psql

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Default to the project's known Neon project ID; override via env.
NEON_PROJECT_ID="${NEON_PROJECT_ID:-calm-paper-82059121}"

DEVELOPERS=(sebastian alex jake)

echo "=== Neon team setup for project: $NEON_PROJECT_ID ==="
echo ""

for dev in "${DEVELOPERS[@]}"; do
    branch_name="dev-$dev"
    role_name="dev_$dev"

    echo "--- Developer: $dev ---"

    # 1. Create the branch (idempotent: ignore "already exists" errors).
    echo "  Creating branch '$branch_name'..."
    if ! neonctl branches create \
            --name "$branch_name" \
            --project-id "$NEON_PROJECT_ID" 2>&1; then
        echo "  Branch '$branch_name' may already exist — continuing."
    fi

    # 2. Create the database role on the branch.
    echo "  Creating role '$role_name' on branch '$branch_name'..."
    if ! neonctl roles create \
            --name "$role_name" \
            --project-id "$NEON_PROJECT_ID" \
            --branch "$branch_name" 2>&1; then
        echo "  Role '$role_name' may already exist — continuing."
    fi

    # 3. Fetch the connection string for this branch.
    echo "  Fetching connection string..."
    CONN_STR="$(neonctl connection-string "$branch_name" \
        --project-id "$NEON_PROJECT_ID")"

    # 4. Apply schema.
    echo "  Applying schema (ontology/schema.sql)..."
    psql "$CONN_STR" -f "$PROJECT_DIR/ontology/schema.sql"

    # 5. Apply migrations in lexicographic order.
    shopt -s nullglob
    migrations=("$PROJECT_DIR/ontology/migrations/"*.sql)
    shopt -u nullglob

    if [ "${#migrations[@]}" -gt 0 ]; then
        for migration in "${migrations[@]}"; do
            echo "  Applying migration: $(basename "$migration")..."
            psql "$CONN_STR" -f "$migration"
        done
    else
        echo "  No migrations found — skipping."
    fi

    # 6. Summary for this developer.
    echo ""
    echo "  Developer   : $dev"
    echo "  Branch      : $branch_name"
    echo "  Role        : $role_name"
    echo "  Connection  : $CONN_STR"
    echo ""
done

echo "=== Team setup complete ==="
