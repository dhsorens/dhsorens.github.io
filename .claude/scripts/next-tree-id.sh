#!/bin/bash
# Allocate the next N tree addresses in this forest.
#
# Forester's own `forester new` does this, but forester is not installed in
# cloud sessions (see CLAUDE.md), so this replicates the allocation scheme:
# scan every trees/**/dhsorens-XXXX.tree, take the highest 4-character
# base-36 suffix, and emit the next N addresses after it.
#
# We take the maximum rather than filling gaps on purpose. 0016 and 001R are
# missing from trees/ but their stale .xml is still published in docs/, and
# reusing those addresses would collide with live URLs.
#
# Usage:  ./.claude/scripts/next-tree-id.sh [count]
# Output: one address per line, e.g.  dhsorens-0029

set -euo pipefail

COUNT="${1:-1}"
PREFIX="dhsorens"
DIGITS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
WIDTH=4

if ! [[ "$COUNT" =~ ^[0-9]+$ ]] || [ "$COUNT" -lt 1 ]; then
    echo "Usage: $0 [count]   (count must be a positive integer)" >&2
    exit 1
fi

# Run from the repo root regardless of where we were invoked.
cd "$(dirname "${BASH_SOURCE[0]}")/../.."

if [ ! -d trees ]; then
    echo "error: no trees/ directory here; run this from the forest repo" >&2
    exit 1
fi

from_base36() {
    local s="$1" n=0 i c d
    for ((i = 0; i < ${#s}; i++)); do
        c="${s:i:1}"
        d="${DIGITS%%"$c"*}"
        n=$((n * 36 + ${#d}))
    done
    printf '%s' "$n"
}

to_base36() {
    local n="$1" out=""
    while [ "$n" -gt 0 ]; do
        out="${DIGITS:$((n % 36)):1}$out"
        n=$((n / 36))
    done
    while [ "${#out}" -lt "$WIDTH" ]; do
        out="0$out"
    done
    printf '%s' "$out"
}

max=0
while IFS= read -r f; do
    suffix="$(basename "$f" .tree)"
    suffix="${suffix#"$PREFIX"-}"
    # Only 4-character all-base-36 suffixes are generated addresses; mnemonic
    # ones (notes, lean, phd, ...) are hand-picked and must not be counted.
    [[ "$suffix" =~ ^[0-9A-Z]{4}$ ]] || continue
    n="$(from_base36 "$suffix")"
    [ "$n" -gt "$max" ] && max="$n"
done < <(find trees -type f -name "$PREFIX-*.tree")

if [ "$max" -eq 0 ]; then
    echo "error: found no $PREFIX-XXXX.tree addresses under trees/" >&2
    exit 1
fi

for ((i = 1; i <= COUNT; i++)); do
    echo "$PREFIX-$(to_base36 $((max + i)))"
done
