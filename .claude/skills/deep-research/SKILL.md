---
name: deep-research
description: Run an exhaustive multi-agent research investigation on a topic and record it in the forest as a substantial deep-dive note. Use when the user invokes /deep-research with a topic - e.g. "/deep-research the soundness of FRI in the list-decoding regime" - or asks to "go really deep" on something. Fans out parallel researchers across distinct search modalities, adversarially verifies every substantive claim, then writes a multi-level note under trees/notes/ and opens a pull request.
---

# /deep-research — go all the way in, and write it down

`/notes` is for recording a topic you've mostly already got a handle on.
This is for the ones you don't: fan out hard, read the primary sources, try to break
the conclusions, and leave behind a note that is genuinely worth returning to.

Invoking this skill **is** the user's opt-in to multi-agent orchestration. Use the
`Workflow` tool. Expect it to cost real tokens and take real time — that is the point,
and the user asked for it.

**Read `../notes/reference/forester-syntax.md` before writing any `.tree` file.**

## 1. Scope it first, inline

Before spawning anything, do a little reconnaissance yourself so the fan-out is aimed
rather than speculative:

- Read any resources the user supplied.
- Grep `trees/` for what the forest already says about this topic. A deep-dive that
  ignores Derek's own prior thinking is a worse note than a shallow one that engages it.
- Decompose the topic into 4–8 concrete research questions. These become the work-list.

If the topic is ambiguous in a way that would send the whole investigation in the wrong
direction, ask **one** question with `AskUserQuestion` before spending the budget.

## 2. Fan out

Author a `Workflow` script over the questions from step 1. The shape that works here:

```js
export const meta = {
  name: 'deep-research',
  description: 'Exhaustive research sweep on a topic, verified and synthesized',
  phases: [
    { title: 'Sweep',     detail: 'parallel researchers, distinct modalities' },
    { title: 'Verify',    detail: 'adversarial check of each substantive claim' },
    { title: 'Critique',  detail: 'what is still missing' },
  ],
}
```

**Sweep — use genuinely different modalities, not the same search five times.**
One agent per lens, each blind to what the others find:

- primary literature (papers, specs, RFCs — the actual sources, not summaries)
- implementations (real code, repos, how it is actually done)
- criticism and limitations (who says this is wrong, and why)
- adjacent and prior formalisms (what this is a special case of, what it generalizes)
- historical development (how the current understanding was arrived at)

Pipeline rather than barrier: a claim from the literature agent should start verifying
while the implementation agent is still reading. Use `pipeline()` unless a stage
genuinely needs every prior result at once (deduplicating claims does; nothing else here
usually does).

**Verify — adversarially.** Every substantive claim gets independent skeptics prompted
to *refute* it, not to confirm it. Where a claim can fail in more than one way, give
each verifier a different lens (is it true / is it load-bearing / does the source
actually say this). Majority-refuted claims get dropped, or kept and explicitly marked
as contested. Prefer perspective-diverse verifiers over three identical ones.

**Critique — one final agent asks what is missing.** An unread primary source, a
modality not run, a question from step 1 that never got answered. If it finds something
substantial, that is another round, not a footnote.

Scale to the topic. A focused technical question might be 8–10 agents; a broad survey
more. If the user gave a token budget, use `budget.remaining()` to drive a
loop-until-dry rather than a fixed count.

## 3. Write it up

Allocate addresses — one blurb (for the Notes page, see step 4), one parent, one per
section, plus any sub-sections, plus one for the session log:

```bash
./.claude/scripts/next-tree-id.sh <N>
```

A deep-dive earns more structure than a `/notes` note. Nesting is fine and idiomatic:
a child tree may itself transclude grandchildren (`dhsorens-000U` does exactly this).

**Parent** at `trees/notes/dhsorens-<parent>.tree`:

```
\title{<Title>}
\taxon{Deep-Dive}
\author{dhsorens}
\date{<today>}
\meta{toc}{true}

\p{
    \em{AI-drafted <today> by deep research; not yet reviewed.}
}

\p{
    <What this is about, why it came up, and what the investigation concluded.
    Link into the existing forest wherever a concept already has a home.>
}

\transclude{dhsorens-<child1>} % <label>
\transclude{dhsorens-<child2>} % <label>

\p{
    Sources: [<name>](<url>), [<name>](<url>).
}
```

**Two sections that make a deep-dive worth returning to.** Do not skip them:

- **Open questions** — what the investigation could not settle, and what would settle
  it. This is the most valuable page in a research notebook and the usual reason to
  come back to a note months later.
- **Contested claims** — anything the verification pass could not confirm, or where
  sources genuinely disagree. Say who claims what. Never smooth a real disagreement
  into a confident sentence.

Standards for the prose:

- **Load the `writing` skill before drafting and run its revision pass before you
  commit.** Mandatory. Depth is not length: a long investigation is exactly the case
  where padding creeps in, so the cut-10% pass matters more here, not less.
- Every non-obvious claim carries a source link. A claim you could not verify is
  written *as* unverified, in the sentence, not quietly asserted.
- Distinguish what the sources establish from what follows from them from what Derek
  might conclude. Depth without that distinction is just confident noise.
- Match the register of the existing notes — first person, discursive, willing to say
  "my thoughts on this are still developing". `trees/notes/dhsorens-0025.tree` is the
  model.
- Length should follow the material. A deep-dive that found three real things says
  three real things; it does not pad to look thorough.

## 4. Index, feature, ship

Same as `/notes`:

1. Write a blurb tree for the deep-dive and prepend
   `\transclude{dhsorens-<blurb>} % <label>` to the block at the bottom of
   `trees/dhsorens-notes.tree`. Never transclude the deep-dive itself — it is far too
   long for that page. See `/notes` step 5 for the blurb's shape, and allocate its
   address alongside the others.
2. Rewrite the blurb in `trees/notes/dhsorens-001S.tree` and bump its `\date`. Keep
   the address — the front page transcludes it.
3. Mint a short `\taxon{Log}` entry in `trees/logs/` recording the session — what was
   investigated, what it concluded, what it left open — and prepend its `\transclude`
   to `trees/dhsorens-logs.tree`. See `/notes` step 7 and **Session records** in
   `CLAUDE.md`; allocate its address alongside the others.
4. Branch, commit, push, open a PR:

```bash
git checkout -b claude/deep-<short-slug>
git add trees/
git commit -m "deep-research: <title>"
git push -u origin claude/deep-<short-slug>
```

The PR body should record **how the research was done**, not just what it found:
the questions investigated, the modalities swept, how many claims were verified and how
many were dropped or marked contested, every tree created, and what remains open. Derek
is reviewing an investigation, not just prose.

Do not merge. Do not run `./commit.sh` — CI builds (see `CLAUDE.md`).

## Afterwards

Suggest `/relate dhsorens-<parent>`. A deep-dive is exactly the kind of note that
should be wired into everything around it.
