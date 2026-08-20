#!/bin/bash
set -e

# Lints the tree sources. CI runs this same script (build-check.yml), so the
# checks cannot drift between a local run and a pull request.
#
# Needs nothing but bash and python3 — no forester — so it also runs in cloud
# sessions, which cannot build the forest.

cd "$(dirname "$0")"

status=0

# Asset links must be absolute. Pages live at /<addr>/, so a relative link to
# docs/foo.pdf resolves to /<addr>/docs/foo.pdf and 404s.
if grep -rnE '\]\((docs|img|media|slides)/' trees --include="*.tree"; then
    echo "error: relative asset link(s) in trees/ — use /docs/..., /slides/..., etc." >&2
    if [ -n "${GITHUB_ACTIONS:-}" ]; then
        echo "::error::relative asset link(s) in trees/"
    fi
    status=1
fi

# Prose is wrapped at 100 characters, so that editing a sentence produces a
# diff of a sentence rather than of a whole paragraph. ./lint-line-length.py
# --fix rewraps anything that is over.
./lint-line-length.py trees || status=1

if [ "$status" -eq 0 ]; then
    echo "lint: trees/ is clean"
fi
exit "$status"
