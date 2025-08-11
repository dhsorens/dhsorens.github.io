#!/bin/bash

forester build forest.toml

echo -e "\033]8;;http://localhost:1313/index.xml\033\\Click here: http://localhost:1313/index.xml\033]8;;\033\\"

python3 -m http.server 1313 -d output
