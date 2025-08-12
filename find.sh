#!/bin/bash

# Check if input is provided
if [ -z "$1" ]; then
    echo "Please provide an input number"
    exit 1
fi

# Search for the file in trees directory
file_path=$(find trees -name "dhsorens-$1.tree")

# Check if file exists
if [ -n "$file_path" ]; then
    cursor "$file_path"
else
    echo "No file found matching dhsorens-$1.tree"
    exit 1
fi
