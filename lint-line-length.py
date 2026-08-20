#!/usr/bin/env python3
"""Check — and with --fix, repair — the line length of forester tree sources.

Prose in trees/ is written one paragraph per \\p{...} block. Left alone, a
paragraph becomes a single enormous line, which makes diffs unreadable: a
one-word edit shows up as a rewritten paragraph. So every line is kept to
MAX_WIDTH characters, wrapped at whitespace.

A line break in forester markup is whitespace, so wrapping is invisible in the
rendered page — but only where a break really is whitespace. These constructs
are never broken:

  * inline and display maths, #{...} and ##{...}
  * \\code{...}
  * a link target, ](...), together with the ] that introduces it

Link text, [like this], is ordinary inline content and may be wrapped.

Some lines cannot be brought under the limit at all: a link target longer than
the limit has nowhere to break. So the rule enforced is not "no line exceeds
MAX_WIDTH" but the strongest rule that is actually satisfiable —

    a line fails if wrapping it would make its longest line shorter.

An over-long line with no break point in it is reported as a note and does not
fail; shortening it means editing the content, which is an author's decision,
not a formatter's. --fix applies exactly the wrapping the check asks for, so
the two agree by construction and the check is stable under repeated fixing.

Usage:
    ./lint-line-length.py [--fix] [--max-width N] [path ...]

Paths may be files or directories; directories are searched for *.tree.
Defaults to trees/. Exits non-zero if any line is over the limit and could be
wrapped shorter (in --fix mode, only if any such line survives the fix).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

MAX_WIDTH = 100

# Macros whose argument is typeset verbatim-ish, where a break would show.
PROTECTED_MACROS = ("code",)

MACRO_RE = re.compile(r"\\([a-zA-Z]+)")


def _match_group(text: str, start: int, opener: str, closer: str) -> int:
    """Index just past the group opening at `start`. len(text) if unbalanced."""
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == opener:
            depth += 1
        elif c == closer:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def atomize(text: str) -> list[str]:
    """Split into whitespace-separated atoms, keeping unbreakable spans whole."""
    atoms: list[str] = []
    cur: list[str] = []

    def flush() -> None:
        if cur:
            atoms.append("".join(cur))
            cur.clear()

    i = 0
    while i < len(text):
        c = text[i]

        if c == "\\":
            m = MACRO_RE.match(text, i)
            if m and m.group(1) in PROTECTED_MACROS and text[m.end() : m.end() + 1] == "{":
                end = _match_group(text, m.end(), "{", "}")
                cur.append(text[i:end])
                i = end
                continue
            # Any other escape: the backslash and the character it protects
            # travel together.
            cur.append(text[i : i + 2])
            i += 2
            continue

        if c == "#":
            j = i + 1
            if text[j : j + 1] == "#":
                j += 1
            if text[j : j + 1] == "{":
                end = _match_group(text, j, "{", "}")
                cur.append(text[i:end])
                i = end
                continue

        if c == "]" and text[i + 1 : i + 2] == "(":
            end = _match_group(text, i + 1, "(", ")")
            cur.append(text[i:end])
            i = end
            continue

        if c.isspace():
            flush()
            i += 1
            continue

        cur.append(c)
        i += 1

    flush()
    return atoms


def wrap(prefix: str, atoms: list[str], width: int) -> list[str]:
    """Greedily pack atoms into lines of at most `width`, each behind `prefix`.

    An atom longer than the budget gets a line of its own and overflows it;
    there is nowhere else for it to go.
    """
    lines: list[str] = []
    cur: str | None = None
    for atom in atoms:
        if cur is None:
            cur = prefix + atom
        elif len(cur) + 1 + len(atom) <= width:
            cur += " " + atom
        else:
            lines.append(cur)
            cur = prefix + atom
    if cur is not None:
        lines.append(cur)
    return lines


def _comment_start(text: str) -> int:
    """Offset of the % that starts a comment, or -1. \\% is not a comment."""
    i = 0
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "%":
            return i
        i += 1
    return -1


def rewrap(line: str, width: int) -> list[str] | None:
    """The line rewrapped, or None if this line must be left alone.

    A comment line is rewrapped with each continuation commented out too, so
    that wrapping cannot promote prose into content. A line with a comment
    *after* other content is left alone: splitting it would need the comment
    lifted out, which is a judgement call, not a reflow.
    """
    indent = line[: len(line) - len(line.lstrip())]
    body = line[len(indent) :]

    comment = _comment_start(body)
    if comment == 0:
        rest = body[1:]
        inner = rest[: len(rest) - len(rest.lstrip())]
        prefix = indent + "%" + (inner if inner else " ")
        body = rest.lstrip()
    elif comment > 0:
        return None
    else:
        prefix = indent

    atoms = atomize(body)
    if not atoms:
        return None
    return wrap(prefix, atoms, width)


def check_file(path: Path, width: int, fix: bool) -> tuple[list[tuple[int, int, bool]], bool]:
    """Return ((line, length, wrappable) per offender, whether the file changed)."""
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")

    offenders: list[tuple[int, int, bool]] = []
    out: list[str] = []
    for number, line in enumerate(lines, start=1):
        if len(line) <= width:
            out.append(line)
            continue

        wrapped = rewrap(line, width)
        if wrapped is None or max(len(w) for w in wrapped) >= len(line):
            # Nothing to gain: an unbreakable URL, or a line we do not touch.
            offenders.append((number, len(line), False))
            out.append(line)
            continue

        offenders.append((number, len(line), True))
        out.extend(wrapped if fix else [line])

    if not fix:
        return offenders, False

    fixed = "\n".join(out)
    if fixed == original:
        return offenders, False
    path.write_text(fixed, encoding="utf-8")
    return offenders, True


def collect(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            found.extend(sorted(p.rglob("*.tree")))
        elif p.is_file():
            found.append(p)
        else:
            sys.exit(f"lint-line-length: no such file or directory: {p}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", default=["trees"])
    parser.add_argument("--fix", action="store_true", help="rewrap offending lines in place")
    parser.add_argument("--max-width", type=int, default=MAX_WIDTH, metavar="N")
    args = parser.parse_args()

    width = args.max_width
    annotate = bool(os.environ.get("GITHUB_ACTIONS"))

    wrappable = 0
    stuck = 0
    fixed = 0
    touched = 0

    for path in collect(args.paths or ["trees"]):
        offenders, changed = check_file(path, width, args.fix)
        if changed:
            touched += 1
        if args.fix:
            fixed += sum(1 for _, _, ok in offenders if ok)
            # Re-read, so that we report only what is still over the limit.
            offenders = check_file(path, width, fix=False)[0]
        for number, length, ok in offenders:
            complaint = f"line is {length} characters (limit {width})"
            if ok:
                wrappable += 1
                print(f"{path}:{number}: error: {complaint}")
                if annotate:
                    print(f"::error file={path},line={number}::{complaint}")
            else:
                stuck += 1
                print(f"{path}:{number}: note: {complaint}, with no break point in it")

    if args.fix:
        print(f"rewrapped {fixed} line(s) across {touched} file(s)")
    if stuck:
        print(
            f"{stuck} line(s) are over {width} characters with nowhere to wrap "
            "(a link target, or a maths span). Shortening those means editing the "
            "content; they are not failures."
        )
    if wrappable:
        print(
            f"{wrappable} line(s) over {width} characters could be wrapped shorter; "
            "run ./lint-line-length.py --fix",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
