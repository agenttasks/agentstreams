#!/usr/bin/env bash
set -euo pipefail

# Render Atlas PNG charts from Neon metric_values data.
# Usage: ./render-charts.sh [output-dir]
#
# Requires: Java 17+, Neon database with metric_values populated.
# Set NEON_JDBC_URL to override the default connection string.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="${1:-$SCRIPT_DIR/charts}"

cd "$SCRIPT_DIR"

echo "Building atlas-chart renderer..."
./gradlew -q compileScala

echo "Rendering charts to $OUTPUT_DIR..."
./gradlew -q run --args="$OUTPUT_DIR"

echo ""
echo "Charts:"
ls -1 "$OUTPUT_DIR"/*.png 2>/dev/null | while read -r f; do
  SIZE=$(du -h "$f" | cut -f1)
  echo "  $SIZE  $(basename "$f")"
done
