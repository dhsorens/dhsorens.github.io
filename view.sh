#!/bin/bash
set -e

./build.sh

echo -e "\033]8;;http://localhost:1313/\033\\Click here: http://localhost:1313/\033]8;;\033\\"

python3 -m http.server 1313 -d output
