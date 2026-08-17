# Forester markup, as this forest actually uses it

Distilled from `cmds.md` plus the conventions observed across all ~104 trees.
When writing a tree, use only what is listed here. Anything else risks a build failure.

## Addresses

A tree's address **is its filename basename**. `trees/notes/dhsorens-0025.tree` has
address `dhsorens-0025`. There is no `\def`, no id directive, no front-matter field
for it.

The directory a tree lives in is organizational only and does not affect the address —
forester resolves addresses globally across `trees/`. (`dhsorens-0026.tree` is a
`\taxon{Log}` that lives in `notes/`.)

Two families of address are in use:

- **Generated**: `dhsorens-XXXX`, four base-36 characters, allocated sequentially.
  Use `.claude/scripts/next-tree-id.sh` to get the next ones.
- **Mnemonic**: hand-picked slugs for stable structural pages — `dhsorens-notes`,
  `dhsorens-lean`, `dhsorens-phd`, `dhsorens-ef`, `index`, `avsm`, and so on.
  Never invent a new mnemonic address for a note; those are the site's stable API.

## Front matter

Canonical order, the form used by most trees:

```
\title{...}
\author{dhsorens}
\date{YYYY-MM-DD}
\meta{toc}{true}
```

- `\title` is mandatory and always the first line.
- `\author` is always the literal `dhsorens`. Omitted on `\taxon{Publication}` trees.
- `\date` is ISO `YYYY-MM-DD` and nothing else.
- `\meta{toc}{true}` gives the tree a table of contents. Put it on any tree that
  transcludes children.
- `\taxon{...}` is optional and goes right after `\title`. Ordinary notes carry
  **no taxon**. The values in use are `Publication`, `Institution`, `Tool`, `Talk`,
  `Place`, `Person`, `Log`, `Organization`, and — introduced by the `/notes`
  workflow — `Deep-Dive`.
- `\meta{external}{URL}` makes the tree's title link out to a canonical source. Used on
  publications and people. It may be repeated.

## Body

| Syntax | Meaning |
|---|---|
| `\p{...}` | A paragraph. **Mandatory** — prose outside a `\p{}` is not a paragraph. |
| `\em{...}` | Italics |
| `\strong{...}` | Bold |
| `\code{...}` | Inline monospace |
| `\ul{...}` / `\ol{...}` | Unordered / ordered list |
| `\li{...}` | List item |
| `#{...}` | Inline math (KaTeX) |
| `##{...}` | Display math (KaTeX) |
| `[text](address)` | Link. If `address` is a tree address it becomes an internal link; otherwise it is treated as a URL. |
| `\transclude{address}` | Pull another tree in as a subsection |
| `%` | Comment, to end of line |
| `\let\name[x][y]{body}` | Define a local macro |

Lists may be nested inside a `\p{}`. Markup nests inside link text:
`[\em{metaspecifications}](dhsorens-000L)`.

Literal `%` in prose must be escaped as `\%` (see `#{0.3}\%` in `dhsorens-001N.tree`).

## Links

Markdown-style `[text](address)` is the *only* link form. There is no `\ref`, no
`[[wikilink]]`. Four flavors, all in use:

```
[financial smart contracts](dhsorens-000A)      % internal, generated address
[Lean](dhsorens-lean)                            % internal, mnemonic address
[Anil Madhavapeddy](avsm)                        % internal, no dhsorens- prefix
[GitHub](https://github.com/dhsorens)            % external URL
[CV](/docs/sorensen-cv.pdf)                      % absolute asset path
```

Asset paths must be **absolute** (`/docs/…`, `/slides/…`, `/media/…`, `/img/…`) —
pages are served at `/<addr>/`, one directory deep, so a relative asset link
resolves to the wrong place. CI's lint step fails the build on relative asset links.

Link text may span several source lines.

## Transclusion

House style is a trailing `%` comment naming what is being pulled in:

```
\transclude{dhsorens-0025} % Computable Specifications
\transclude{dhsorens-0020} % Protocol Snarkification
% \transclude{dhsorens-0017} % temporarily unlisted
```

Transcludes may be interleaved with `\p{}` blocks — they render as subsections in
document order, so you can write a paragraph, transclude a child, then write more.

Commenting out a transclude is the idiom for unlisting a child without deleting it.
A tree may be transcluded from more than one place.

## Directives that do NOT work here

`\parent`, `\tag`, `\def`, `\ref`, `\query`, `\subtree`, `\import`, `\scope`, `\put`,
`\get`. None appear anywhere in the forest. There is no tagging system, no query
mechanism, and **no automatic backlinks** — relatedness is expressed entirely through
inline prose links and the transclusion hierarchy. That is why `/relate` exists.

`\tex{preamble}{body}` exists in forester but is unused here, and would add a LaTeX
dependency to CI. Do not introduce it.

## House style

- Wrap prose in `\p{}` with four-space indentation.
- One idea per paragraph; the existing notes run long and discursive, first person.
- No "See also" or "Related" headed blocks — this forest has none. Cross-references
  are inline links inside ordinary sentences, or a closing sentence in the
  "I also keep some [preprints](dhsorens-preprints)" idiom.
- Em-dashes and curly quotes are written directly as Unicode.
