#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"commit message\""
    exit 1
fi

forester build forest.toml

# Rename output to docs
git mv output docs

# Add all changes
git add .

# Commit with provided message
git commit -m "$1"

# Rename docs back to output
git mv docs output
