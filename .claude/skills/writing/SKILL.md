---
name: writing
description: Standards for the technical prose in this forest. Consult before drafting any note, blurb, or section, and again as a revision pass before committing. Use when writing or editing .tree content, or when the user invokes /writing to review a draft. Targets textbook-quality technical exposition - formal definitions properly introduced, concepts placed in their history, and the specific habits that make generated writing bad.
---

# Writing standards for this forest

**The target is a good graduate textbook.** Not a blog post, not a literature review, not
a research diary. A reader who has never heard of the subject should be able to arrive at
a page cold, read it start to finish, and leave knowing what the thing *is* — formally —
where it came from, what it relates to, and why anyone cares.

Apply this three times: **before** drafting, to set the target; **while** drafting, for the
definition pattern below; **after**, as a revision pass. The third is where most of the
value is.

## Read the feedback log first

`reference/feedback-log.md` accumulates Derek's writing feedback, dated, each entry paired
with the rule derived from it. Read it before drafting. It is the record of what has
already been corrected once, and repeating a mistake that is written down there is the
worst failure mode available.

When Derek gives writing or style feedback — in a PR review, a comment, or conversation —
**append it to that log** as part of doing the work, before or alongside the fix. Quote his
words, then state the rule in a form that applies to the next page. Do not wait to be
asked. The point is that the standard accumulates and he stops having to repeat himself.

## The standard

Four properties, all required:

- **Clear.** A first reading suffices. If a sentence needs re-reading to parse, rewrite it.
- **Self-contained.** The page defines what it uses, or links to the page that does. A
  reader should not have to already know the answer to follow the exposition.
- **Thorough without being wordy.** Cover the subject completely; say each thing once.
  Length comes from material, never from restatement or hedging.
- **Organised.** The order is: what it is → where it came from → how it relates → why it
  matters → what goes wrong. Never critique before defining.

## Two registers, and which page gets which

| Register | Where | Voice |
|---|---|---|
| **Textbook** | `trees/zk/**`, and any note carrying definitions, theorems, or protocol detail | Impersonal. Third person. No authorial opinion. |
| **Notebook** | `trees/logs/**`, reflective and biographical notes (`dhsorens-0025`, `001N`, `0005`, education and work-history pages) | First person. Thinking visibly on the page is legitimate. |

On a **textbook** page, cut authorial framing entirely. It reads as opinion where the
reader wants exposition:

> ✗ My reading is that the random oracle model is not the problem and adaptivity is.
> ✓ The binding constraint is adaptivity rather than the random oracle model.

> ✗ Their negative result is the part I would keep.
> ✓ The negative result is the load-bearing one.

> ✗ I have not checked which.
> ✓ How the bound scales in the round count is open.

An open question is still stated — completeness demands it — but as a property of the
subject, not as a confession about the author. Attribution to *other* people stays and is
required: `Canetti et al. proved`, not `it is known that`.

On a **notebook** page the older guidance holds: first person is correct, and `my thoughts
on this are still developing` is a legitimate sentence. Being someone's notebook is not a
licence for filler; it is a reason to be exact, because the reader most likely to be
confused by a vague sentence is Derek in six months.

## Introducing a concept

This is the thing most often done badly. A textbook introduces a concept by answering four
questions in its first two paragraphs, compactly:

1. **What it is** — the idea in one or two sentences, before any formalism.
2. **Where it came from** — who introduced it, when, and what problem they were solving.
   A definition invented to make a specific proof work should say so.
3. **How it relates** — to the neighbouring definitions the reader may already have. Which
   it strengthens, which it implies, which it replaces.
4. **Why it matters** — what it buys, and what depends on it.

Compactly. Four questions is not four paragraphs, and none of them is a signposting
sentence. The failure to avoid is a page that opens with a sharp aphorism about the
subject's significance and never says plainly what the subject is.

## Formal definitions

Derek reads as a formal mathematician: he wants the mathematics stated properly, with good
prose around it. Both, not either.

Every substantial concept gets the three-part treatment:

1. **Intuition first** — a sentence or two saying what the definition is going to capture,
   in words, so the reader knows what they are looking at.
2. **The definition, stated formally** — set out as a definition, with quantifiers in the
   right order, every symbol introduced, and the assumptions named. Display maths (`##{}`)
   for anything that does not read cleanly inline.
3. **Unpacking afterwards** — what the quantifier order is doing, which clause is
   load-bearing, what breaks if a hypothesis is dropped, and the degenerate case.

A technical claim without its assumptions is not a claim. A definition whose symbols are
undefined is not a definition.

Where a page is a critique of a construction, the formal definition of that construction
comes **first, on that page**, however briefly — even when a fuller treatment lives
elsewhere and is linked. Do not tell the reader what goes wrong with a thing before they
know precisely what the thing is.

## Citations

Cite live, in the text, at the point of the claim — never only in a trailing sources list.
Every cited paper gets its own `\taxon{Paper}` page (historical context, contributions,
impact) and the in-text citation links to it; see the `/add-content` skill for the
convention. A trailing `Sources:` paragraph is a supplement to live links, not a substitute.

Attribute contested claims to whoever made them. Keep three things distinguishable in the
prose: what a source establishes, what follows from it, and what is being concluded here.

## Sentence level

- Active voice with a real subject. `Buterin proposed`, not `it was proposed that`.
- Verbs, not nominalizations: `analyze`, not `perform an analysis of`.
- Vary length. A short sentence after two long ones lands. Uniform rhythm reads as machine
  output.
- Hedge once or not at all. `may potentially suggest` hedges three times and asserts
  nothing.
- Cut intensifiers: `very`, `extremely`, `incredibly`, `truly`, `quite`, `really`.
- Define a technical term on first use, or do not use it. Never two terms for one concept.
- Quantify when you can. `three of the four formalizations` beats `most`.
- Maths is `#{inline}` and `##{display}`. Define every symbol at first use.

## Habits to cut

The specific failure modes of generated prose. Check for each by name.

**Throat-clearing.** `It is important to note that`, `It is worth considering`, `Let us now
turn to`. Delete and start at the claim.

**Authorial opinion on a technical page.** `my reading is`, `the part I would keep`, `I
would not`, `what should worry an implementer`. See the register table above.

**The knowing aside.** A sentence whose work is to signal that the author finds something
amusing or embarrassing — `the catalogue is embarrassing`, `this is the part that makes it
awkward`, `which is itself informative`. It is editorial, and a textbook does not do it.

**Triads.** Three adjectives or three clauses where one is accurate.

**The "not just X, but Y" frame.** Rarely earns its length.

**Vague abstraction where a name exists.** `certain approaches`, `various factors`. Name
them or cut the sentence.

**Padding verbs.** `serves to illustrate` → `illustrates`.

**Suspect vocabulary.** Each is a symptom; check whether a plainer word is exact: `delve`,
`leverage`, `robust`, `seamless`, `landscape`, `realm`, `crucial`, `pivotal`, `myriad`,
`nuanced`, `underscore`, `showcase`, `tapestry`, `intricate`, `it's worth noting`, `at its
core`, `fundamentally`.

**Faux profundity.** Sentences that sound weighty and assert nothing. Either say which
questions, or cut it.

**No signposting paragraphs**, no summary paragraph restating what was just said, no
restating the question before answering it, no `See also` blocks — cross-references are
inline links inside ordinary sentences.

## Revision pass

Before committing any prose:

1. Does the page define its subject formally before criticising it? If not, fix that first.
2. Can a reader who has never heard of the subject follow it? Read it as that reader.
3. Delete the first sentence of each section. Does it still work? Usually yes.
4. Search for every word in the suspect vocabulary list. Justify or replace.
5. Search for `I `, `my `, `we ` on a technical page. Each one is a defect.
6. Find every hedge. Keep at most one per claim.
7. Find every sentence over ~40 words. Split or cut.
8. Check each paragraph has exactly one idea.
9. Check every cited paper is linked live at the point of the claim.
10. Read for rhythm — if every sentence is the same length, vary it.
11. **Cut 10% by word count.** There is always 10%.

A page is finished when nothing else can come out without losing something the reader
needed.
