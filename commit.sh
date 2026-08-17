#!/bin/bash
set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"commit message\""
    exit 1
fi

./build.sh

# Publish the build into docs/ (what GitHub Pages serves), replacing it
# wholesale so stale files from previous builds don't linger
rm -rf docs
cp -R output docs

# Add all changes
git add .

# Commit with provided message
git commit -m "$1"
