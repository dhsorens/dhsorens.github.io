#!/bin/bash

if ! forester --version 2>/dev/null | grep -q '^5\.0'; then
    echo "error: forester 5.0 is required (install with: opam install forester.5.0)" >&2
    exit 1
fi

DEST_DIR="${1:-logs}"
NUM_FILES="${2:-1}"

for ((i=1; i<=NUM_FILES; i++)); do
    NEW_FILE=$(forester new forest.toml --dest="trees/$DEST_DIR/" --prefix=dhsorens)
    if [ -n "$NEW_FILE" ]; then
        # open an editor when run interactively; otherwise just print the path
        if [ -t 1 ] && command -v cursor >/dev/null; then
            cursor "$NEW_FILE"
        else
            echo "$NEW_FILE"
        fi
    fi
done

