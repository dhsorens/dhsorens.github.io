#!/usr/bin/env python3
"""Check — and with --fix, reflow — the line length of forester tree sources.

Prose in trees/ is written one paragraph per \\p{...} block. Left alone, a
paragraph becomes a single enormous line, which makes diffs unreadable: a
one-word edit shows up as a rewritten paragraph. So every line is kept to
MAX_WIDTH characters.

--fix reflows: it joins each paragraph back into one stream of words and
refills it to the limit. Write and edit however you like — a sentence added
in the middle, a clause deleted — then run --fix and the paragraph is packed
neatly again. Only the limit is enforced, though; a paragraph left ragged is
never an error, so nothing fails CI for want of a reflow.

A line break in forester markup is whitespace, so both breaking and joining
are invisible in the rendered page — but only where a break really is
whitespace, and only where a newline really was a break. Hence the two halves
of the reflow:

Wrapping never splits:

  * inline and display maths, #{...} and ##{...}
  * \\code{...}
  * a link target, ](...), together with the ] that introduces it

Link text, [like this], is ordinary inline content and may be wrapped.

Joining never merges across a blank line or a structural one — an opener
(\\p{), a closer (}), or a block macro (\\li{...}, \\transclude{...}, the rest of
BLOCK_MACROS, and anything the file \\lets). So a list stays a list and a
paragraph stays a paragraph; only the lines within one of them are repacked.
An \\em{...} heading keeps its own line because the blank lines around it are
boundaries, which is also why a reflow cannot dissolve one: it never produces
a blank line, so it can never take one away. A comment is reflowed within
itself, each continuation commented out too, so that a reflow can never
promote prose into content or bury content in a comment.

Some lines cannot be brought under the limit at all: a link target longer than
the limit has nowhere to break. So the rule enforced is not "no line exceeds
MAX_WIDTH" but the strongest rule that is actually satisfiable —

    a line fails if reflowing would make its paragraph's longest line shorter.

An over-long line with no break point in it is reported as a note and does not
fail; shortening it means editing the content, which is an author's decision,
not a formatter's. --fix applies exactly the reflow the check asks for, so the
two agree by construction and the check is stable under repeated fixing.

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

# Macros that introduce a line of their own: structure, frontmatter, list
# items. A line starting with one of these is never joined onto the line
# above. Inline macros (\em, \strong, \code, and all of maths) are absent on
# purpose — they turn up at the head of a continuation line all the time.
BLOCK_MACROS = frozenset(
    """
    p ul ol li
    title subtitle author authors contributor date taxon tag meta number
    transclude import export def let scope put get query
    tex texify
    """.split()
)

MACRO_RE = re.compile(r"\\([a-zA-Z]+)")
LET_RE = re.compile(r"\\let\\([a-zA-Z]+)")


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


def _brace_balance(text: str) -> int:
    """Unescaped { minus unescaped } — how much this text leaves open."""
    depth = 0
    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return depth


class Line:
    """One source line, classified for reflow.

    `prefix` is what every line of this line's paragraph is written behind:
    indentation, and for a comment the % that keeps it a comment. `body` is
    the content after it. `verbatim` marks a line to be copied out untouched.
    """

    __slots__ = ("raw", "prefix", "body", "verbatim", "comment", "opens", "closes")

    def __init__(self, raw: str, lets: frozenset[str]) -> None:
        self.raw = raw
        indent = raw[: len(raw) - len(raw.lstrip())]
        rest = raw[len(indent) :]

        self.comment = False
        self.verbatim = False

        at = _comment_start(rest)
        if at == 0:
            # A whole-line comment: reflowable behind a % of its own.
            self.comment = True
            tail = rest[1:]
            inner = tail[: len(tail) - len(tail.lstrip())]
            self.prefix = indent + "%" + (inner if inner else " ")
            self.body = tail.strip()
        elif at > 0:
            # Content, then a comment. Splitting this needs the comment lifted
            # out of the middle, which is a judgement call, not a reflow.
            self.prefix = indent
            self.body = rest.rstrip()
            self.verbatim = True
        else:
            self.prefix = indent
            self.body = rest.rstrip()

        body = self.body
        macro = MACRO_RE.match(body)
        name = macro.group(1) if macro else None
        block = name is not None and (name in BLOCK_MACROS or name in lets)

        # An opener (\p{) or a closer (}) is structure, not prose: it is left
        # on its own line, and nothing is packed onto it from either side.
        alone = bool(body) and (body.endswith("{") or set(body) == {"}"})

        # A } at the head of a line closes a group the line above opened, even
        # where something follows it — packing it onto that line would bury the
        # brace mid-paragraph and re-indent what comes after it.
        self.opens = alone or block or self.verbatim or not body or body.startswith("}")
        # A block macro that closed everything it opened is a complete item —
        # \transclude{x}, \li{x} — so the next line belongs to whatever
        # encloses it, not to this. One left open, \li{x — continues, absorbs.
        self.closes = (
            alone
            or self.verbatim
            or not body
            or (block and _brace_balance(body) <= 0)
            or _brace_balance(body) < 0
        )

def paragraphs(lines: list[Line]) -> list[list[Line]]:
    """Group lines into the runs that get filled together."""
    groups: list[list[Line]] = []
    for line in lines:
        last = groups[-1][-1] if groups else None
        starts = (
            last is None
            or line.opens
            or last.closes
            or line.comment != last.comment
            # Indentation is normalised to the first line of the paragraph, but
            # a comment's % is part of its prefix and has to match.
            or (line.comment and line.prefix != last.prefix)
        )
        if starts:
            groups.append([line])
        else:
            groups[-1].append(line)
    return groups


def refill(group: list[Line], width: int) -> list[str]:
    """The lines this paragraph becomes."""
    if group[0].verbatim or not group[0].body:
        return [line.raw for line in group]
    atoms: list[str] = []
    for line in group:
        atoms.extend(atomize(line.body))
    if not atoms:
        return [line.raw for line in group]
    return wrap(group[0].prefix, atoms, width)


def reflow_groups(text: str, width: int) -> list[tuple[int, list[Line], list[str]]]:
    """(first line number, source lines, refilled lines) per paragraph."""
    lets = frozenset(LET_RE.findall(text))
    lines = [Line(raw, lets) for raw in text.split("\n")]

    out: list[tuple[int, list[Line], list[str]]] = []
    number = 1
    for group in paragraphs(lines):
        out.append((number, group, refill(group, width)))
        number += len(group)
    return out


def reflow(text: str, width: int) -> str:
    """The file, with every paragraph refilled to `width`."""
    return "\n".join(
        line for _, _, filled in reflow_groups(text, width) for line in filled
    )


def check_file(path: Path, width: int, fix: bool) -> tuple[list[tuple[int, int, bool]], bool]:
    """Return ((line, length, fixable) per offender, whether the file changed).

    A line over the limit is an error when the reflow would make its
    paragraph's longest line shorter than it — that is, when there is
    something to gain. When there is not, the line has no break point left in
    it, and it is reported as a note rather than a failure.
    """
    original = path.read_text(encoding="utf-8")
    groups = reflow_groups(original, width)
    fixed = "\n".join(line for _, _, filled in groups for line in filled)

    offenders: list[tuple[int, int, bool]] = []
    if fix:
        # The reflow has had its go, so whatever is still over the limit is
        # irreducible by construction. Report it against the file as written.
        for number, line in enumerate(fixed.split("\n"), start=1):
            if len(line) > width:
                offenders.append((number, len(line), False))
    else:
        for start, group, filled in groups:
            longest = max(len(line) for line in filled)
            for offset, line in enumerate(group):
                if len(line.raw) > width:
                    offenders.append((start + offset, len(line.raw), longest < len(line.raw)))

    if not fix or fixed == original:
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
    parser.add_argument("--fix", action="store_true", help="reflow every paragraph in place")
    parser.add_argument("--max-width", type=int, default=MAX_WIDTH, metavar="N")
    args = parser.parse_args()

    width = args.max_width
    annotate = bool(os.environ.get("GITHUB_ACTIONS"))

    wrappable = 0
    stuck = 0
    touched = 0

    for path in collect(args.paths or ["trees"]):
        offenders, changed = check_file(path, width, args.fix)
        if changed:
            touched += 1
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
        print(f"reflowed {touched} file(s)")
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
