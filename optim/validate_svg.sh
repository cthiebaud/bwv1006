#!/bin/bash

# Validate all SVG files in a directory
# Usage: ./validate_all_svgs.sh <directory>

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    echo "Example: $0 svgo_incremental_20250525_153244"
    exit 1
fi

DIRECTORY="$1"

if [ ! -d "$DIRECTORY" ]; then
    echo "❌ Directory not found: $DIRECTORY"
    exit 1
fi

echo "🔍 Validating all SVG files in: $DIRECTORY"
echo

# Find all .svg files and run validator on each
find "$DIRECTORY" -name "*.svg" -type f | sort | while read -r svg_file; do
    echo "Testing: $(basename "$svg_file")"
    python3 optim/svg_validator.py "$svg_file"
    echo
done