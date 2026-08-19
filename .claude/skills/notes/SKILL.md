---
name: notes
description: Research a topic and write it into the forest as a new deep-dive note. Use when the user invokes /notes with a topic, optional source resources, and optional focus instructions - e.g. "/notes make a new note on lattice-based commitments with resources A, B, C. Focus on the soundness argument." Produces a parent tree plus child sub-trees under trees/notes/, indexes it in dhsorens-notes, updates the Latest Deep-Dive blurb, and opens a pull request.
---

# /notes — write a researched deep-dive into the forest

Turn a research request into a permanent, linked note in Derek's Forester site.
The point is that the site records what he has been thinking about *while* the
thinking happens, so the corpus grows into a large interconnected body he (and
anyone else) can get lost in.

**Read `reference/forester-syntax.md` before writing any `.tree` file.** The markup
is narrow and unforgiving, and a bad directive fails the CI build.

## 1. Parse the request

Pull three things out of the invocation:

- **Topic** — what the note is about.
- **Resources** — URLs, papers, repo paths, file paths the user supplied. These are
  the spine of the note; every one of them must actually be read and used.
- **Focus** — the angle the user asked for ("focus on the soundness argument",
  "compare it to what we said about metaspecifications"). This shapes what the note
  argues, not just what it covers.

If the topic is genuinely ambiguous, ask *one* clarifying question with
`AskUserQuestion`. Otherwise proceed — a note is cheap to revise and lives on a branch.

## 2. Research

Default mode: read every supplied resource with `WebFetch` (or `Read` for local
paths), then use `WebSearch` to fill gaps, follow citations, and check claims that
the supplied sources assert but do not establish.

**Going deeper**: if the invocation contains `--deep`, or the user asks to "go really
deep", hand off to the `deep-research` skill and follow that instead — it runs a
multi-agent sweep with adversarial verification and writes a more structured note.
Do not use the `Workflow` tool from this skill.

Ground rules for the writing that follows:

- Every non-obvious factual claim carries a source link. If you could not verify
  something, say so in the note rather than asserting it.
- Distinguish what sources establish from what Derek might conclude. This is his
  notebook — it can speculate, but it must be visible when it is speculating.
- Prefer primary sources. Where a claim is contested, say that it is contested.

## 3. Allocate addresses

```bash
./.claude/scripts/next-tree-id.sh <N>
```

where `N` is 1 (blurb, see step 5) + 1 (parent) + one per section + 1 (session log, see
step 7). The script prints addresses like `dhsorens-0029`. Use them in the order printed:
first for the blurb, next for the parent, then the children, and the last for the log. Never invent an address by hand, and never reuse one.

## 4. Write the trees

**Parent** at `trees/notes/dhsorens-<parent>.tree`:

```
\title{<Title in Title Case>}
\taxon{Deep-Dive}
\author{dhsorens}
\date{<today, YYYY-MM-DD>}
\meta{toc}{true}

\p{
    \em{AI-drafted <today>; not yet reviewed.}
}

\p{
    <One or two paragraphs orienting the reader: what this is about, why it came
    up, and what the note argues. Link out to existing trees wherever a concept
    already has a home in the forest.>
}

\transclude{dhsorens-<child1>} % <short label>
\transclude{dhsorens-<child2>} % <short label>

\p{
    Sources: [<name>](<url>), [<name>](<url>).
}
```

The provenance line is deliberately the first thing on the page and deliberately
trivial to delete — Derek removes that one `\p{}` block when he has read and edited
the note. Do not bury it, do not make it decorative, and never omit it.

**Children** at `trees/notes/dhsorens-<childN>.tree`, one per section:

```
\title{<Section Title>}
\author{dhsorens}
\date{<today>}

\p{
    <prose>
}
```

Children are ordinary note trees — no taxon, no provenance line (the parent carries
it), and they only need `\meta{toc}{true}` if they in turn transclude something.

Writing standards:

- **Load the `writing` skill before drafting a single sentence, and run its revision
  pass before you commit.** It is not optional and it is not advisory. The prose here
  should be concise, academic, and plain; the skill names the specific habits that make
  generated writing bad, and the revision pass is where most of the quality comes from.
- Match the voice of the existing notes: first person, discursive, willing to say
  "my thoughts on this are still developing". Read `trees/notes/dhsorens-0025.tree`
  for the register. Discursive is fine; loose is not.
- Link into the existing forest constantly. Before writing, grep `trees/` for the
  concepts you are about to mention — if `[Lean](dhsorens-lean)` or
  `[smart contract specification](dhsorens-001J)` already exists, link it.
- Sections should be substantial. If a section is one paragraph, it belongs in the
  parent, not in its own tree.

## 5. Index it in Notes

Prepend a transclude line to the block at the bottom of `trees/dhsorens-notes.tree`,
newest first:

```
\transclude{dhsorens-<parent>} % <Title>
```

Notes are **transcluded, not listed**. Each entry renders in place with its own title and
date, in the standard forester page format — not as a bulleted list of links. Read the
existing order before inserting; thematic notes are sometimes grouped with their topic
rather than placed strictly by date.

**What you transclude is a blurb, not the note.** Anything this workflow produces is a
parent plus several sections; transcluding it whole would put a few thousand words on the
page and bury every other entry. So write one more tree, in ordinary note format:

```
\title{A Note on <Topic>}
\author{dhsorens}
\date{<today>}

\p{
    <One paragraph: what [<Title>](dhsorens-<parent>) covers, and what it concludes.>
}

\p{
    The sections:
    \ul{
        \li{[<Section title>](dhsorens-<childN>) — <half a line on what is in it>.}
    }
}
```

The blurb is the feed item; the note is read at its own address. Working examples:
`dhsorens-004C` (for the zk corpus) and `dhsorens-004I` (for the hash-functions note).

Only a short standalone note with no sections goes in directly, as the older entries on
that page do. If in doubt, write the blurb — it is one small tree and it keeps the page
readable as the forest grows.

## 6. Update the Latest Deep-Dive

Rewrite the body of `trees/notes/dhsorens-001S.tree` and bump its `\date` to today:

```
\title{Latest Deep-Dive}
\author{dhsorens}
\date{<today>}
\meta{toc}{true}

\p{
    <One or two sentences on what the latest note is about and why it was
    interesting> — see [<Title>](dhsorens-<parent>).
}
```

Keep the address `dhsorens-001S`. It is transcluded by `trees/index.tree` and its
page is already published at `/dhsorens-001S/`; changing it would break the front page.

Write the blurb for Derek first — its main job is to remind him what the most recent
thing was — but keep it readable to a stranger landing on the front page.

## 7. Log the session

Mint one more tree — a short `\taxon{Log}` entry in `trees/logs/` recording that this
note was written, what it covers, and what it left open — and prepend
`\transclude{dhsorens-XXXX} % <date label>` to `trees/dhsorens-logs.tree`. Allocate its
address alongside the others in step 2. This is a hard rule for every session that
touches `trees/`; see **Session records** in `CLAUDE.md`. Keep it to a paragraph or two,
in the register of the existing entries — it is a record of the work, not a second
abstract of the note.

## 8. Ship it

```bash
git checkout -b claude/note-<short-slug>
git add trees/
git commit -m "notes: <title>"
git push -u origin claude/note-<short-slug>
```

Then open a PR (use `gh pr create` locally, or the GitHub MCP tools from a cloud
session). The body should give Derek what he needs to review without opening every
file:

- what the note argues, in three or four sentences
- the sources used, as links
- every tree created, with its address and title
- anything you were unsure about or could not verify

Do not merge it — merging to `main` is what publishes (CI rebuilds `docs/` via
`publish.yml`). Do not run `./commit.sh`; commit sources only. In a local session
you can preview first: `./build.sh` must pass, and
`xsltproc output/default.xsl output/dhsorens-<parent>/index.xml > /dev/null` proves
the new page renders. Cloud sessions have no forester — CI's build-check on the PR
is the preview there.

## Afterwards

Suggest `/relate dhsorens-<parent>` as the natural next step, which weaves the new
note into the rest of the corpus.
