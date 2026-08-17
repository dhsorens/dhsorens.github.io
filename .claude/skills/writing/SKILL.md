---
name: writing
description: Standards for the technical prose in this forest. Consult before drafting any note, blurb, or section, and again as a revision pass before committing. Use when writing or editing .tree content, or when the user invokes /writing to review a draft. Targets academic, technical, concise prose - and names the specific habits that make generated writing bad.
---

# Writing standards for this forest

The prose here should read like a careful researcher thinking on paper: precise,
unhurried, and short. Academic and technical in register, but plain — clarity is the
goal, and jargon is a cost paid only when a term does real work.

Apply this twice. Once before drafting, to set the target. Once after, as a revision
pass — the second is where most of the value is.

## Principles

**Lead with the claim.** State the point, then support it. Do not build up to it.

**One idea per paragraph.** If a paragraph has two, it is two paragraphs.

**Concrete beats abstract.** Name the thing. `the Dexter2 specification omits fee
dynamics` is worth more than `certain specifications may lack economic detail`.

**Commit.** If the evidence supports a conclusion, state it. If it does not, say what
is missing. Symmetric both-sides framing that reaches no view is the most common way
technical writing wastes a reader's time.

**Earn every sentence.** Delete any sentence whose removal costs the reader nothing.
Do this literally, sentence by sentence, on the final pass.

## Sentence level

- Active voice with a real subject. `Buterin proposed` not `it was proposed that`.
- Verbs, not nominalizations: `analyze`, not `perform an analysis of`; `assume`, not
  `make the assumption that`.
- Vary length. A short sentence after two long ones lands. Uniform rhythm reads as
  machine output.
- Hedge once or not at all. `may potentially suggest` hedges three times and asserts
  nothing. Pick the accurate level of confidence and use it once.
- Cut intensifiers. `very`, `extremely`, `incredibly`, `truly`, `quite`, `really`.
  If a claim needs `very`, the noun or verb is wrong.
- Define a technical term on first use, or do not use it. Never use two terms for one
  concept.

## Structure

- No signposting paragraphs. `First we examine X, then we turn to Y` tells the reader
  nothing they will not learn by reading.
- No summary paragraph restating what was just said. In this forest, a section's job
  is to make its point and stop.
- No restating the question before answering it.
- Transclusion carries structure. If a section needs three paragraphs of scaffolding
  to connect to its parent, the split is wrong.

## Habits to cut

These are the specific failure modes of generated prose. Check for each by name.

**Throat-clearing.** `It is important to note that`, `It is worth considering`,
`In the world of formal methods`, `Let us now turn to`. Delete and start at the claim.

> ✗ It is important to note that specifications can be incorrect even when proofs succeed.
> ✓ A specification can be wrong even when every proof of it succeeds.

**Triads.** Three adjectives or three clauses where one is accurate. `robust, scalable,
and maintainable` usually means the writer had no specific property in mind.

**The "not just X, but Y" frame.** Rarely earns its length.

> ✗ This is not just a technical problem, but a fundamentally social one.
> ✓ The problem is social, not technical.

**Vague abstraction where a name exists.** `certain approaches`, `various factors`,
`a number of considerations`. Name them or cut the sentence.

**Padding verbs.** `serves to illustrate` → `illustrates`. `plays a role in
determining` → `determines`.

**Suspect vocabulary.** Each is a symptom; check whether a plainer word is exact:
`delve`, `leverage`, `robust`, `seamless`, `landscape`, `realm`, `crucial`, `pivotal`,
`myriad`, `nuanced`, `underscore`, `showcase`, `tapestry`, `intricate`,
`it's worth noting`, `at its core`, `fundamentally`.

**Faux profundity.** Sentences that sound weighty and assert nothing:
`This raises deep questions about the nature of correctness.` Either say which
questions, or cut it.

## Technical content

- **Separate the layers.** What a source establishes, what follows from it, and what
  you conclude are three different things. Keep them distinguishable in the prose.
- **Attribute contested claims.** `Buterin argued`, not `it is understood that`.
- **State uncertainty in the sentence**, not in a hedge. `I have not verified whether
  this holds for non-constant fees` beats `this may possibly hold in some cases`.
- **Quantify when you can.** `three of the four formalizations` beats `most`.
- **Give the assumption.** A technical claim without its assumptions is not a claim.
- Math is `#{inline}` and `##{display}`. Define every symbol at first use.

## Voice in this forest

These are Derek's notes, so first person is correct and so is thinking visibly on the
page — `my thoughts on this are still developing` is a legitimate sentence. Discursive
is fine; loose is not. The register to match is
`trees/notes/dhsorens-0025.tree` and `trees/notes/dhsorens-001N.tree`: a researcher
working something out, in complete and disciplined sentences.

Being someone's notebook is not a licence for filler. It is a reason to be exact,
because the reader most likely to be confused by a vague sentence is Derek in six
months.

## Revision pass

Before committing any prose, go through this:

1. Delete the first sentence of each section. Does it still work? Usually yes — it was
   throat-clearing.
2. Search the draft for every word in the suspect vocabulary list. Justify or replace.
3. Find every hedge. Keep at most one per claim.
4. Find every sentence over ~40 words. Split or cut.
5. Check each paragraph has exactly one idea.
6. Cut the concluding summary paragraph if one appeared.
7. Read for rhythm — if every sentence is the same length, vary it.
8. **Cut 10% by word count.** There is always 10%.

A note is finished when nothing else can come out without losing something the reader
needed.
