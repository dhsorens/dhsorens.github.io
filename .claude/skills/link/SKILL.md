---
name: link
description: Resolve `[text](TODO)` stubs in the forest by linking to an existing tree or minting a thin named entity page, then weave each new page in with /relate. Use when the user invokes /link — e.g. "/link 004D" or bare "/link" — or asks to fill TODO links or create missing entity pages for unresolved markdown links.
---

# /link — give a stub a home

Notes in this forest mark unresolved entity links as `[text](TODO)`. This skill
turns those into real addresses: reuse a page that already is that entity, or
mint a thin named stub in the right subdirectory, then run `/relate` on each
new page so the rest of the corpus can point at it.

**Read `../notes/reference/forester-syntax.md` before editing any `.tree` file.**
**Read `reference.md` before creating a page** — placement, matching, and the
stub template live there.

## 1. Parse the invocation

`/link 004D`, `/link dhsorens-004D`, and a path all mean the same tree. Find it:

```bash
find trees -name "dhsorens-004D.tree"
```

Bare `/link` uses the `.tree` in context (open, attached, or just discussed).
If there is none, scan all of `trees/`.

## 2. Collect TODOs

```bash
rg -n '\]\(TODO\)' trees
```

Restrict to the target tree when one was named. Record every `[text](TODO)`:
the link text, the file, the line. Deduplicate by link text — two
`[Bitcoin](TODO)`s share one destination.

If there are no TODOs, say so and stop.

## 3. Index the forest

For each tree under `trees/`: address, title, taxon, directory. You need this
to match, and `/relate` will need the link graph next. Reading every file is
fine; use an Explore agent if it is faster.

## 4. Resolve each unique link text

For link text `T`, in order:

1. **Reuse** an existing tree that *is* `T`, not a note about `T`. Exact title
   match (case-insensitive), then `The T`. Prefer an entity taxon over a
   Blog/Deep-Dive. Reject substring hits — `Ethereum` is not Ethereum Foundation.
   Matching rules and false friends: `reference.md`.
2. **Create** a thin named entity page when nothing matches and `T` is a
   proper-noun entity (protocol, person, institution, tool, place, org).
   Placement table: `reference.md`. Do not use `next-tree-id.sh` — these are
   mnemonic addresses, written by hand like `dhsorens-lean`.
3. **Ask** when `T` is a concept (`list decoding`, `soundness`) with no home.
   Do not auto-write a `/notes` deep-dive and do not mint a junk stub.

If several plausible targets remain, ask — do not guess. If you would create
more than about three pages, list them first and wait.

## 5. Write new stubs

Follow the template in `reference.md`. Load the `writing` skill before adding
any `\p{}`. No AI-drafted provenance line — these are not generated notes.

Do **not** transclude a new stub into `dhsorens-notes`. Do **not** bump
`dhsorens-001S`. Entity pages are reached by links, not the Notes feed.

## 6. Replace the stubs

In every file under `trees/` that has `[T](TODO)`, replace it with
`[T](<address>)`. Same text, new address, zero other edits.

## 7. Relate each new page

If every TODO resolved to an existing address, skip this step.

Otherwise **read `../relate/SKILL.md` and follow it** on each newly created
address: outbound links from the stub, inbound by wrapping existing phrases
elsewhere. Same editing rules — wrap, do not rewrite; no "See also". Stay on
the `/link` branch; do not open a second PR.

## 8. Report and ship

Report two tables:

- TODO text → address, reused or created, file the stub lived in
- every `/relate` edit (file, phrase, address, one-sentence reason)

```bash
git checkout -b claude/link-<source-or-slug>
git add trees/
git commit -m "link: resolve TODO stubs in <source>"
git push -u origin claude/link-<source-or-slug>
```

Open a PR containing those tables. Do not merge. Do not run `./commit.sh` —
CI does the building (see `CLAUDE.md`).
