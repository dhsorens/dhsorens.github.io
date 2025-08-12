#!/bin/bash

DEST_DIR="${1:-notes}"
NUM_FILES="${2:-1}"

for ((i=1; i<=NUM_FILES; i++)); do
    forester new forest.toml --dest="trees/$DEST_DIR/" --prefix=dhsorens
done