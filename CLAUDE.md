# derekhsorensen.com

Personal website of Derek Sorensen, built with [forester](https://sr.ht/~jonsterling/forester/) **5.0** (version pinned by the guard in `build.sh` — bump it together with the pins in `.github/workflows/*.yml`). GitHub Pages serves the committed `docs/` directory from `main`; the domain sits behind Cloudflare.

**Publishing model: CI is the single writer to `docs/`.** Sessions commit *sources only* (`trees/`, `assets/`, scripts, skills); on every push to `main`, `publish.yml` rebuilds the site and commits the fresh `docs/`. Merging a content PR is what publishes it. Never hand-edit `docs/`, and don't commit locally-built `docs/` unless CI is broken (`./commit.sh` remains as that manual fallback).

**Cloud sessions (claude.ai) have no forester and can't install it.** They can write `.tree` sources, allocate addresses with `.claude/scripts/next-tree-id.sh <n>`, and open PRs; `build-check.yml` on the PR is their build verification. Never attempt `./build.sh`, `./view.sh`, or `./commit.sh` from a cloud session.

## Repo map

| Path | What it is |
| --- | --- |
| `trees/` | Content source (`.tree` files). Subdirs: `notes/`, `logs/`, `zk/`, `research/`, `institutions/`, `tools/`, `places/`, `people/`, `orgs/`. Top-level trees are section indexes (`index.tree` = homepage, `dhsorens-notes.tree`, `dhsorens-logs.tree`, `dhsorens-talks.tree`, …). `zk/` is a multi-page corpus rather than a pile of notes — see below. |
| `assets/` | Static files: `docs/` (paper/CV PDFs), `slides/`, `media/` (images), `img/`. Published at those same absolute paths. |
| `theme/` | Vendored upstream forester theme. **Do not edit** XSL/CSS/JS — only the six favicon files (`favicon*`, `apple-touch-icon.png`, `android-chrome-*`) are local and must survive theme updates. |
| `docs/` | **Generated** build output, committed for GitHub Pages. Never hand-edit; `commit.sh` regenerates it wholesale. |
| `output/` | Gitignored build directory (`forester` writes here). |
| `forest.toml` | Forester config (trees, assets, site URL). |
| `cmds.md` | Markup cheatsheet for `.tree` files; `.claude/skills/notes/reference/forester-syntax.md` documents the markup as this forest actually uses it. |
| `.claude/scripts/next-tree-id.sh` | Allocates the next sequential `dhsorens-XXXX` addresses (works without forester). |
| `.github/workflows/` | `build-check.yml` (build + render + lint on every PR), `publish.yml` (rebuild and commit `docs/` on push to `main`). |

## Scripts

| Script | Purpose |
| --- | --- |
| `build.sh` | The clean build: version guard, wipes `output/`, `forester build`, copies `assets/` verbatim into `output/` (forester 5.0 only emits content-addressed copies), copies `CNAME`, writes redirect stubs at the old 4.x `/<addr>.xml` URLs. |
| `view.sh` | Build + serve locally at `localhost:1313`. |
| `commit.sh "msg"` | Build, replace `docs/` wholesale, commit everything. **Manual fallback only** — CI normally writes `docs/`. |
| `new.sh [dir] [n]` | Mint new tree(s) in `trees/<dir>/` (default `notes`) with the next sequential address; prints the path when non-interactive. |
| `log.sh` | Same as `new.sh` but defaults to `trees/logs/`. |
| `find.sh XXXX` | Locate `trees/**/dhsorens-XXXX.tree`. |
| `commit-trees.sh "msg"` | Commit and push only `trees/` (no build). |

## Hard rules

- Asset links in trees must be **absolute** (`/docs/…`, `/slides/…`, `/media/…`, `/img/…`) — pages live at `/<addr>/`, so relative links break. CI lints this.
- Never hand-edit `docs/` or `output/`.
- Every paragraph needs `\p{…}`; see `cmds.md` for the markup reference.
- Publishing flow: work on a branch, commit **sources only** (`./commit-trees.sh` or plain git), push, PR to `main`. CI publishes on merge; allow ~10 minutes for the Cloudflare cache after merging.
- `trees/notes/dhsorens-001S.tree` is the **Latest Deep-Dive** blurb transcluded at the top of the front page. Its address is load-bearing — rewrite its body, never its address.
- `trees/dhsorens-notes.tree` is an **index, not a container**: one `\li{}` entry per item, newest first, linking out. Never transclude a note into it — a note is read on its own page, and the index has to stay legible as the forest grows. `dhsorens-talks.tree` and `dhsorens-slides.tree` follow the same pattern.
- A **corpus** (currently `trees/zk/`, rooted at `dhsorens-002C`) is one item on that index however many trees it contains. Its internal structure is transclusion — root transcludes hubs, hubs transclude leaves — so the whole thing reads as one page at its own address. Adding a page inside a corpus does not touch the Notes index.

## Workflows

- **Add notes/logs/talks/papers/slides by hand**: use the `/add-content` skill.
- **Research a topic into the forest**: `/notes <topic> with resources A, B. Focus on …` — researches, writes a parent tree + child sections under `trees/notes/`, indexes it, updates the Latest Deep-Dive, opens a PR. `/deep-research <topic>` (or `/notes --deep`) is the heavy multi-agent version with adversarial verification.
- **Weave a note into the corpus**: `/relate <address>` adds interconnecting links in both directions.
- **Prose quality**: `/writing` is the prose standard; the research skills load it before drafting and run its revision pass before committing.
- **Health check / forester upgrades / broken-site diagnosis**: use the `/maintain` skill.

Generated notes carry a visible `\em{AI-drafted <date>; not yet reviewed.}` first paragraph and `\taxon{Deep-Dive}`. Delete that paragraph after reviewing and editing the note.
