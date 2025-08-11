#!/bin/bash

# Check if a commit message was provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a commit message"
    echo "Usage: $0 commit message"
    exit 1
fi

# Store the commit message
commit_message="$1"

# Execute git commands
git add trees/
git commit -m "$commit_message"
git push
