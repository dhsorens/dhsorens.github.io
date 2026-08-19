---
name: relate
description: Weave a note into the rest of the forest by adding interconnecting links in both directions. Use when the user invokes /relate with a tree address - e.g. "/relate dhsorens-0029". Finds conceptually related notes, links the target out to them, edits those notes to link back, and opens a pull request.
---

# /relate — connect a note to everything around it

Forester has no tags, no queries, and no automatic backlinks. Relatedness in this
forest exists only as inline prose links and the transclusion hierarchy. So the web of
ideas is built by hand — this skill does that building.

The goal is a corpus you can wander through: land on any note, and the concepts it
mentions are live links to the other notes where those concepts were thought about.

**Read `../notes/reference/forester-syntax.md` before editing any `.tree` file.**

If the target still has `[…](TODO)` stubs, run `/link` on it first — those are
unresolved entity links, and relating around them just cements the holes.

## 1. Read the target

`/relate dhsorens-0029` refers to a tree address. Find the file — the address is the
filename basename, and it may be in any subdirectory of `trees/`:

```bash
find trees -name "dhsorens-0029.tree"
```

Read it, and read any children it transcludes. You are relating the whole note, not
just the parent page.

## 2. Index the forest

Build a picture of what else exists. For each tree under `trees/`: its address, title,
date, and the addresses it already links to or transcludes. Reading every file is fine
— there are only ~100 and they are small. Use an `Explore` agent if it is faster.

You need the existing link graph so you do not add a link that is already there.

## 3. Find genuine relationships

Look for notes that are conceptually connected to the target:

- **Shared subject** — both are about specification correctness.
- **Instance of** — one is a case study of what the other argues in general
  (`dhsorens-001N` Dexter2 is an instance of `dhsorens-001J` smart contract
  specification).
- **Precursor / successor** — the target develops an idea an older note raised, or
  supersedes something the older note left open.
- **Shared tooling** — both concern Lean, Rocq, proof assistants.
- **Tension** — the target complicates or contradicts something said earlier. These are
  the most valuable links in a research notebook. Say so explicitly when you find one.

Reject superficial keyword overlap. Two notes both containing the word "formal" are not
related. If you cannot say in one sentence *why* a reader following the link would be
glad they did, do not add the link.

## 4. Add outbound links

In the target note, link the concepts that already have homes in the forest.

## 5. Add inbound links

Edit the related notes so they point back at the target. This is what makes the corpus
navigable from both ends rather than a pile of one-way references.

## The editing rule

Derek has written and edited this prose. Protect it.

**Strongly prefer wrapping an existing phrase in a link**, changing zero words:

```
before:   the nuance of smart contract specification is
after:    the nuance of [smart contract specification](dhsorens-001J) is
```

Only when no natural anchor phrase exists, add one new sentence in the existing voice —
usually at the end of a paragraph, in the forest's established idiom
("I also keep some [preprints](dhsorens-preprints)", "for more on this see …").

**Load the `writing` skill before adding any sentence.** You are writing into prose
Derek has already edited, so an added sentence has to be at least as disciplined as
what surrounds it. One sentence, no throat-clearing, no signposting. If you cannot say
it in one clean sentence, the link probably is not worth adding.

Never:

- rewrite, reword, or reflow existing prose
- delete anything, including commented-out lines (`%` comments are how this forest
  parks material it may want back)
- add a "See also" or "Related notes" heading — the forest has no such convention and
  introducing one would look foreign
- link the same target twice in one paragraph, or link a phrase to the tree it is
  already inside

Aim for a handful of high-value links per note, not maximal density. A note where every
other phrase is blue is worse than one with four good links.

## 6. Report and ship

Report every edit as a table: file, the phrase you linked, the address you linked it
to, and the one-sentence reason. Derek reviews inbound edits more carefully than
generated notes, so make the diff easy to read.

```bash
git checkout -b claude/relate-<address>
git add trees/
git commit -m "relate: connect <address> to the corpus"
git push -u origin claude/relate-<address>
```

Open a PR with `mcp__github__create_pull_request` containing that table. Do not merge.
Do not run `./commit.sh` — CI does the building (see `CLAUDE.md`).

If you found no relationships worth adding, say so and change nothing. An honest empty
result is better than padding the graph with weak links.
