# /link reference — placement, matching, stubs

## Placement

Entity pages are named, durable, and not Notes-feed items. Directory is
organizational only; the address is the filename basename.

| Kind | Directory | Taxon | Address |
|---|---|---|---|
| Person | `trees/people/` | `Person` | Ask for the slug. Those URLs are durable; `avsm` has no `dhsorens-` prefix. Default otherwise: `dhsorens-<lastname>`. |
| Institution | `trees/institutions/` | `Institution` | `dhsorens-<slug>` |
| Tool | `trees/tools/` | `Tool` | `dhsorens-<slug>` |
| Place | `trees/places/` | `Place` | `dhsorens-<slug>` |
| Organization | `trees/orgs/` | `Organization` | `dhsorens-<slug>` |
| Protocol / chain | `trees/protocols/` | `Protocol` | `dhsorens-<full-name>` — `dhsorens-bitcoin`, `dhsorens-ethereum`, never `dhsorens-eth` (collides in the mind with `dhsorens-ef`) |
| Concept | — | — | Do not stub. Search notes harder; if none, ask. |

`forest.toml` already scans all of `trees/`, so a new subdirectory needs no
config change. The first Protocol page creates `trees/protocols/`.

Never put an entity stub in `notes/`. Never transclude one into
`dhsorens-notes`. Never bump the Latest Deep-Dive for a stub.

## Matching

Index every tree: address, title, taxon, directory. For link text `T`:

1. Exact title match, case-insensitive.
2. Title `The T`.
3. Prefer an entity taxon (`Protocol`, `Institution`, `Tool`, `Person`,
   `Place`, `Organization`) over a Blog/Deep-Dive/Talk whose title contains `T`.
4. Reject substring hits. `T` matching a strictly longer title is a false
   friend unless the extra words are only an article.

If several candidates still look right, ask.

### False friends

These are the ones that have already come up. The spirit is: the TODO names
the entity, not a note, talk, or institution about it.

| Link text | Not this | Why |
|---|---|---|
| Ethereum | `dhsorens-ef` Ethereum Foundation | Different entity. |
| Ethereum | `dhsorens-0046` The Ethereum Setting | A zk-corpus page about deployment constraints. |
| Ethereum | `dhsorens-0020` Protocol Snarkification | A note about snarkifying the protocol. |
| Ethereum | `dhsorens-0022` / `dhsorens-0028` Safely Snarkifying the Ethereum Protocol | A talk. |
| Bitcoin | (none yet) | No existing tree is titled Bitcoin. |

## Stub template

Match `trees/tools/dhsorens-lean.tree` and `trees/institutions/dhsorens-ef.tree`:

```
\title{<Name>}
\taxon{<Kind>}
\author{dhsorens}
\date{<today, YYYY-MM-DD>}

[https://<canonical>](https://<canonical>)
```

Add **at most one** `\p{}` when disambiguation or a pointer into the forest is
actually useful. Load the `writing` skill before that sentence. No provenance
line.

`\meta{toc}{true}` is for trees that transclude children. A stub does not.

Do not use `./new.sh` or `.claude/scripts/next-tree-id.sh` for these. Sequential
addresses are for notes; entity pages are mnemonic, created as
`trees/<dir>/dhsorens-<slug>.tree`.

## Worked example: `/link 004D`

`trees/notes/dhsorens-004D.tree` has `[Bitcoin](TODO)` and `[Ethereum](TODO)`.

- **Bitcoin** — no title match. Proper-noun protocol. Create
  `trees/protocols/dhsorens-bitcoin.tree`, `\taxon{Protocol}`, canonical
  `https://bitcoin.org`. Replace every `[Bitcoin](TODO)` with
  `[Bitcoin](dhsorens-bitcoin)`. Then `/relate dhsorens-bitcoin`.
- **Ethereum** — no exact title match. `dhsorens-ef`, `dhsorens-0046`,
  `dhsorens-0020` are false friends. Create
  `trees/protocols/dhsorens-ethereum.tree`, `\taxon{Protocol}`, canonical
  `https://ethereum.org`. The one `\p{}` is worth it here: distinct from the
  [Ethereum Foundation](dhsorens-ef), and a pointer at the hash-functions note
  that prompted the stub. Replace `[Ethereum](TODO)` with
  `[Ethereum](dhsorens-ethereum)`. Then `/relate dhsorens-ethereum`.

Neither stub goes on the Notes page. One PR, both pages, both relate passes.
