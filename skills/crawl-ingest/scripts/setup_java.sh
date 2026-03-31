#!/bin/bash
set -euo pipefail

echo "=== Setting up Java/Gradle crawl-ingest project ==="

mkdir -p crawl-project && cd crawl-project

# Initialize Gradle project
gradle init --type java-application --dsl groovy --project-name crawl-project

# Create directory structure
mkdir -p src/main/java/com/example/{crawler,extract,storage}
mkdir -p src/main/resources
mkdir -p data

echo "=== Java/Gradle setup complete ==="
echo "Add dependencies to build.gradle (see java/gradle-setup.md)"
echo "Run: gradle run"
