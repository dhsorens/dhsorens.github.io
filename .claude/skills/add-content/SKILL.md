---
name: add-content
description: Add new content to this forester website — notes/blog posts, logs, talks, slides, publications/preprints, or homepage features — and publish it. Covers minting tree addresses, frontmatter and taxon conventions, wiring content into the right parent tree, asset placement, preview checks, and the branch + PR publish flow. Use when asked to add, write, or publish a note, log entry, talk, paper, or other site content.
---

# Adding content to derekhsorensen.com

Read `CLAUDE.md` for the repo map and hard rules, and `cmds.md` for the markup cheatsheet. Every content addition follows the same spine; the per-type sections below say where each kind of content lives and how it gets wired in.

## The spine

1. **Branch.** Never commit content directly on `main` (merging to `main` deploys). Create or switch to a working branch (the user historically uses `next` for content batches).

2. **Mint the tree.** Run `./new.sh <dir>` (default `notes`) or `./log.sh` (defaults to `logs`) — non-interactively they print the new file path, e.g. `trees/notes/dhsorens-002C.tree`, minting the next sequential base-36 address. Equivalent direct command: `forester new forest.toml --dest="trees/<dir>/" --prefix=dhsorens`. Trees with named addresses (e.g. `dhsorens-lean`) are created by hand as `trees/<dir>/dhsorens-<name>.tree`; use names only for durable concept/entity pages, sequential addresses for everything else.

3. **Write frontmatter + body.**
   ```
   \title{...}
   \author{dhsorens}
   \date{YYYY-MM-DD}
   \taxon{Blog}        % per type, see below
   ```
   Body rules: every paragraph in `\p{…}`; links are `[text](dhsorens-XXXX)` for trees and `[text](https://…)` for URLs; math `#{…}` inline, `##{…}` display; **asset links must be absolute** (`/docs/…`, `/slides/…`, `/media/…`, `/img/…`). Match the voice and density of neighboring trees — look at 2–3 recent siblings before writing.

4. **Wire it in** (per-type, below). A tree that isn't transcluded or linked from a parent is unreachable — that's a bug unless intentional.

5. **Assets.** Drop files into the matching `assets/` subdir (`docs/` for PDFs of papers/CV/thesis, `slides/` for talk decks, `media/` for photos/screenshots, `img/` for site imagery). They publish at the same absolute path (`assets/slides/x.pdf` → `/slides/x.pdf`).

6. **Preview.**
   ```bash
   ./build.sh                                                    # must exit 0, "Success!", no diagnostics
   xsltproc output/default.xsl output/<addr>/index.xml >/dev/null  # page renders
   xsltproc output/default.xsl output/<parent>/index.xml | grep -i "<new title>"  # wired in
   grep -rnE '\]\((docs|img|media|slides)/' trees                # must be EMPTY (no relative asset links)
   ```
   Offer `./view.sh` if the user wants to eyeball it at `localhost:1313`.

7. **Publish.** `./commit.sh "message"` on the branch (builds and regenerates `docs/` wholesale), push, `gh pr create` targeting `main`. Deploy happens when the PR merges; after merging, the live site can serve stale files for ~10 minutes (Cloudflare cache) — don't diagnose "breakage" inside that window (see `/maintain`).

## Per-type wiring

### Note / blog post
- File: `trees/notes/dhsorens-XXXX.tree`, `\taxon{Blog}` (or omit taxon for plain notes).
- Wire: add `\transclude{dhsorens-XXXX} % short label` to `trees/dhsorens-notes.tree`. Newest content goes near the top of the transclude list; thematic/evergreen notes are grouped with their topic block instead — read the existing order first.

### Log entry
- File: `trees/logs/dhsorens-XXXX.tree`, `\taxon{Log}`, `\date` required, usually short (one or two `\p`), often no `\author`.
- Wire: `\transclude{dhsorens-XXXX} % <date label>` at the **top** of the list in `trees/dhsorens-logs.tree` (newest first).

### Talk
- Add a `\li{…}` at the **top** of the list in `trees/dhsorens-talks.tree`: title (linked to a companion note if there is one), event link, date, place.
- Companion note (when there are slides/photos/abstract): a note tree with `\taxon{Talk}`, containing the abstract and a `Links:` list (event, `/slides/…` PDF, media). See `trees/notes/dhsorens-0023.tree` for the pattern.
- Slides deck: PDF → `assets/slides/`, plus a `\li{[Talk title](/slides/<file>.pdf)}` in `trees/dhsorens-slides.tree`.

### Publication / preprint
- PDF (if hosted here) → `assets/docs/`.
- Publication: add a `\paper{authors}{title}{venue}{year}{link}` row in `trees/research/dhsorens-pubs.tree`.
- Preprint: add a `\preprint{authors}{title}{venue}{year}{link}` row in `trees/dhsorens-preprints.tree`.
- The `link` argument is a URL or an absolute asset path like `/docs/paper.pdf`.

### Homepage feature
- `trees/index.tree` transcludes the homepage sections (featured article, education, publications, talks, work history). To feature something, add/move a `\transclude{…} % label` there; to retire one, comment it out with `%` (the existing style) rather than deleting.

### New section or entity page (institution, person, tool, …)
- Named tree in the matching subdir (`trees/institutions/dhsorens-<name>.tree`, `trees/people/<name>.tree`, …), then link to it from wherever it's mentioned. People trees are referenced by `\author{<addr>}`.

## Don'ts

- Don't edit `docs/` or `output/` by hand — `commit.sh` regenerates `docs/` wholesale.
- Don't use relative asset links, ever.
- Don't touch `theme/` for content work.
- Don't merge the PR without the user's go-ahead — merging deploys.

For site health checks, forester upgrades, or diagnosing a broken deploy, use the `/maintain` skill instead.
