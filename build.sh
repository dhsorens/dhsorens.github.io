#!/bin/bash
set -e

# This site is built against forester 5.0 (https://ocaml.org/p/forester/5.0)
if ! forester --version 2>/dev/null | grep -q '^5\.0'; then
    echo "error: forester 5.0 is required (found: $(forester --version 2>/dev/null || echo 'not installed'))" >&2
    echo "install it with: opam install forester.5.0" >&2
    exit 1
fi

# forester does not clean output/ between builds, so removed trees would
# linger (and get published by commit.sh) without this
rm -rf output

forester build forest.toml

# forester 5.0 only emits content-addressed copies of assets (bafkr....pdf);
# also publish them under their original paths so /docs/*.pdf etc. keep
# stable, human-readable URLs
cp -R assets/. output/

# custom domain for GitHub Pages
cp CNAME output/

# forester 5.0 moved each tree from /<addr>.xml to /<addr>/; write an XHTML
# redirect at each old .xml path so existing links keep working
for dir in output/*/; do
    addr=$(basename "$dir")
    [ -f "$dir/index.xml" ] || continue
    cat > "output/$addr.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="refresh" content="0;url=/$addr/"/><title>Redirecting</title></head><body><a href="/$addr/">This page has moved to /$addr/</a></body></html>
EOF
done
