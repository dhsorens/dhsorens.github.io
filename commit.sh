#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"commit message\""
    exit 1
fi

forester build forest.toml

cp output/fukkr-favicon/android-chrome-192x192.png output/android-chrome-192x192.png
cp output/fukkr-favicon/android-chrome-512x512.png output/android-chrome-512x512.png
cp output/fukkr-favicon/apple-touch-icon.png output/apple-touch-icon.png

# Rename output to docs
mv output docs

# Add all changes
git add .

# Commit with provided message
git commit -m "$1"

# Rename docs back to output
mv docs output
