#!/usr/bin/env bash
set -euo pipefail

# End-to-end: generate time-series data → load into Neon → render Atlas charts.
#
# Requires:
#   NEON_JDBC_URL — JDBC connection string for atlas-chart renderer
#   NEON_PSQL_URL — psql connection string for data loading
#   Java 17+
#
# Usage: ./scripts/refresh-charts.sh [output-dir]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${1:-$PROJECT_DIR/atlas-chart/charts}"

: "${NEON_JDBC_URL:?Set NEON_JDBC_URL (jdbc:postgresql://...)}"
: "${NEON_PSQL_URL:?Set NEON_PSQL_URL (postgresql://...)}"

echo "=== Step 1: Generate time-series seed data ==="
python3 "$SCRIPT_DIR/generate-timeseries.py" > "$SCRIPT_DIR/timeseries-seed.sql"
ROWS=$(tail -3 "$SCRIPT_DIR/timeseries-seed.sql" | grep "Total rows" | grep -o '[0-9]*')
echo "  Generated $ROWS rows"

echo ""
echo "=== Step 2: Load into Neon ==="
psql "$NEON_PSQL_URL" -f "$SCRIPT_DIR/timeseries-seed.sql" > /dev/null 2>&1
COUNT=$(psql "$NEON_PSQL_URL" -t -c "SELECT count(*) FROM metric_values;")
echo "  Loaded ${COUNT// /} rows into metric_values"

echo ""
echo "=== Step 3: Render Atlas charts ==="
cd "$PROJECT_DIR/atlas-chart"
export NEON_JDBC_URL
./gradlew -q run --args="$OUTPUT_DIR"

echo ""
echo "=== Done ==="
ls -1 "$OUTPUT_DIR"/*.png 2>/dev/null | while read -r f; do
  SIZE=$(du -h "$f" | cut -f1)
  echo "  $SIZE  $(basename "$f")"
done
