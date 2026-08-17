# derekhsorensen.com

Personal website of Derek Sorensen, built with [forester](https://sr.ht/~jonsterling/forester/) **5.0** (version pinned by the guard in `build.sh`). GitHub Pages serves the committed `docs/` directory from `main`; the domain sits behind Cloudflare.

## Repo map

| Path | What it is |
| --- | --- |
| `trees/` | Content source (`.tree` files). Subdirs: `notes/`, `logs/`, `research/`, `institutions/`, `tools/`, `places/`, `people/`, `orgs/`. Top-level trees are section indexes (`index.tree` = homepage, `dhsorens-notes.tree`, `dhsorens-logs.tree`, `dhsorens-talks.tree`, …). |
| `assets/` | Static files: `docs/` (paper/CV PDFs), `slides/`, `media/` (images), `img/`. Published at those same absolute paths. |
| `theme/` | Vendored upstream forester theme. **Do not edit** XSL/CSS/JS — only the six favicon files (`favicon*`, `apple-touch-icon.png`, `android-chrome-*`) are local and must survive theme updates. |
| `docs/` | **Generated** build output, committed for GitHub Pages. Never hand-edit; `commit.sh` regenerates it wholesale. |
| `output/` | Gitignored build directory (`forester` writes here). |
| `forest.toml` | Forester config (trees, assets, site URL). |
| `cmds.md` | Markup cheatsheet for `.tree` files. |

## Scripts

| Script | Purpose |
| --- | --- |
| `build.sh` | The clean build: version guard, wipes `output/`, `forester build`, copies `assets/` verbatim into `output/` (forester 5.0 only emits content-addressed copies), copies `CNAME`, writes redirect stubs at the old 4.x `/<addr>.xml` URLs. |
| `view.sh` | Build + serve locally at `localhost:1313`. |
| `commit.sh "msg"` | Build, replace `docs/` wholesale with the output, commit everything. |
| `new.sh [dir] [n]` | Mint new tree(s) in `trees/<dir>/` (default `notes`) with the next sequential address; prints the path when non-interactive. |
| `log.sh` | Same as `new.sh` but defaults to `trees/logs/`. |
| `find.sh XXXX` | Locate `trees/**/dhsorens-XXXX.tree`. |
| `commit-trees.sh "msg"` | Commit and push only `trees/` (no build). |

## Hard rules

- Asset links in trees must be **absolute** (`/docs/…`, `/slides/…`, `/media/…`, `/img/…`) — pages live at `/<addr>/`, so relative links break.
- Never hand-edit `docs/` or `output/`.
- Every paragraph needs `\p{…}`; see `cmds.md` for the markup reference.
- Publishing flow: work on a branch, `./commit.sh "msg"`, push, PR to `main`. Deploy happens on merge; allow ~10 minutes for the Cloudflare cache after merging.

## Workflows

- **Add notes/logs/talks/papers/slides**: use the `/add-content` skill.
- **Health check / forester upgrades / broken-site diagnosis**: use the `/maintain` skill.
