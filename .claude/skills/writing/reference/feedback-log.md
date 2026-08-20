# Writing feedback log

Derek's writing and style feedback, dated, newest first. Each entry quotes what he said and
states the rule it produces.

**Read this before drafting.** Append to it whenever new feedback arrives — in a PR review,
a comment, or conversation — as part of doing the work, without being asked. An entry here
has already cost him one round of review; repeating the mistake is the worst available
failure.

---

## 2026-08-20 — follow-up on PR #36

### Why this workflow is textbook-voice, and where personal notes still live

> "there will still be personal notes with 'my read on this' in other places, but the purpose
> of this current workflow is to flesh out what is already known in the wild (mostly for my
> understanding) and so we should have a textbook quality to them and not personal writing
> quality"

**Rule.** The distinction is one of *purpose*, not merely of directory. Where a page exists to
set down what is already established in the literature — which is what the `zk` corpus and
the research workflows are for — it is exposition and takes the textbook voice. Where a page
exists to record Derek's own thinking, the personal register is correct and wanted. When
unsure which a page is, ask what the page is *for*: explaining the known, or working
something out.

### Ask when an instruction contradicts something else

> "please ask me questions if I ask for something contradictory"

**Rule.** Standing instruction. Where a new request conflicts with a recorded convention, an
earlier instruction, or itself, raise it before writing rather than picking a reading
silently. The register question above was exactly this case and asking resolved it in one
round.

### Paper pages take a fixed format

> "I would like the paper pages to have a standard format, with headers if possible, of
> context, contributions, and impact ; context should be historical and technical"

**Rule.** Fixed three-part structure, in this order, with run-in headers: **Context** (both
historical *and* technical — what the state of the art was, what was open, and the technical
setting the result lives in), **Contributions**, **Impact**. Recorded in `/add-content`.

---

## 2026-08-20 — review of PR #36 (the Fiat–Shamir section)

Verdict: *"This is a nice start, but your writing really needs to improve. All of the notes
in this website are meant to be textbook-quality, technical notes and I don't think that is
the case with the text you're producing in this PR yet."*

### Textbook quality is the standard

> "all writing here should be textbook quality, meaning that it is clear, readable, thorough
> without being wordy, and self-contained"

> "all the writing on this repository should be textbook-quality, and therefore mostly
> self-contained, precise, and extremely well-organised"

**Rule.** The target is a good graduate textbook, not a blog post or a research diary. Four
properties, all required: clear, self-contained, thorough without wordy, organised.

### Introduce concepts the way a textbook does

> "One of the things lacking is an effective way of introducing concepts that is both simple
> and salient, and which takes into account their history, relationship to other
> definitions, and their relevance. (Textbooks do this very well without being too wordy.)"

**Rule.** Open by answering four questions compactly: what it is, where it came from, how it
relates to neighbouring definitions, why it matters. Four questions is not four paragraphs.
Do not open with an aphorism about the subject's significance and never plainly say what the
subject is.

### Formal definitions, with prose around them

> "I would like something formal, mathematical, technical. My brain works like that of a
> formal mathematician's, so I want the content to read like that, as well as having good
> prose along with it."

> "Where appropriate, formal definitions should be introduced in a way commensurate with a
> high-quality mathematical textbook, and be prefaced or explained afterwards in a slightly
> more intuitive way."

**Rule.** Three-part treatment: intuition, then the definition stated formally with every
symbol introduced and assumptions named, then an unpacking of what the definition is doing.
Both the mathematics and the prose — not either.

### Define before you critique

> "I should get to the end of that introductory section with a strong sense, theoretically
> and technically, for exactly what Fiat-Shamir is before you go telling me what can go
> wrong with it."

> "Remember, this page is for someone who has never heard of Fiat Shamir"

**Rule.** The formal definition of a construction comes first, on the page that critiques it,
however briefly — even when the fuller treatment lives elsewhere and is linked. Write the
introduction for a reader who has never heard of the subject.

### No authorial opinion on a technical page

> "No offence, but I don't care what 'your reading' of anything is. This is supposed to be a
> textbook-like piece of writing, so we don't care much for your, or my, opinion phrased like
> this."

**Rule.** On technical pages, cut `my reading is`, `the part I would keep`, `I would not`, `I
have not checked`. State open questions as properties of the subject, not confessions about
the author. Attribution to other people stays and is required. The notebook register (first
person, visible thinking) survives only on logs and reflective or biographical notes — see
the register table in `SKILL.md`.

*Scope confirmed 2026-08-20: textbook voice governs `trees/zk/**` and technical notes;
`trees/logs/**` and reflective notes such as `dhsorens-0025` and `001N` keep the notebook
register.*

### Cite live, and give every paper its own page

> "For each of these sources, (and in general moving forward when we cite a paper), please
> (1) link it live into the text when you reference it, and (2) have a page for each paper,
> with a new taxonomy `paper` that explains: (1) the historical context, (2) the
> contributions, and (3) the impact of each paper."

**Rule.** No citation appears only in a trailing `Sources:` list. Every cited paper gets a
`\taxon{Paper}` page covering historical context, contributions, and impact, and in-text
citations link to it. Convention recorded in `/add-content`.

### Concepts get their own pages, and get linked

> "is there anywhere in this repo a page for a Sigma protocol? If not, could you please make
> one and /relate it appropriately?"

> "Might be nice to link 'transcripts' here to some of the existing work on soundness … it
> might be worth creating a stub for transcripts to link in both places"

**Rule.** A named technical concept used across several pages gets its own page and is linked
at each use, rather than re-explained inline. When a page leans on a concept that has no
page, mint one and `/relate` it.

### Comparisons to implementations belong on their own pages

> "I wonder if all the comparisons to Arklib should have their own, comparison page, with a
> taxonomy `in the wild` or something like that which can be used for any time a concept
> we're introducing exists in the wild"

**Rule.** ArkLib-style "here is how this concept appears in a real codebase" material goes on
its own `\taxon{In the Wild}` page, transcluded into the concept page, so it can be tracked
and updated as the codebase moves. Convention recorded in `/add-content`.

### Keep this log

> "Please make add to your skills that you listen for my writing feedback and add it to your
> writing skill, in general. Keep notes so that you improve in writing and style over time
> and we can just focus on the material."

**Rule.** This file. Append on every piece of feedback, unprompted.
