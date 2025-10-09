#!/bin/bash

DEST_DIR="${1:-notes}"
NUM_FILES="${2:-1}"

for ((i=1; i<=NUM_FILES; i++)); do
    NEW_FILE=$(forester new forest.toml --dest="trees/$DEST_DIR/" --prefix=dhsorens)
    if [ -n "$NEW_FILE" ]; then
        cursor "$NEW_FILE"
    fi
done