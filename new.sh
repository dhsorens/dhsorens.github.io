#!/bin/bash

DEST_DIR="${1:-notes}"
forester new forest.toml --dest="trees/$DEST_DIR/" --prefix=dhsorens