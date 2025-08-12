#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"commit message\""
    exit 1
fi

# Rename output to docs
if [ -d output ]; then
    mv output docs
else
    echo "Directory 'output' does not exist."
    exit 1
fi

# Add all changes
git add .

# Commit with provided message
git commit -m "$1"

# Rename docs back to output
mv docs output
