---
name: maintain
description: Health-check and update this forester-built website. Checks the installed forester version against the repo pin and against upstream releases, watches for the forester 6.0 release and the browser XSLT removal deadline, verifies the build and the live site, and applies updates when things are out of date. Use when asked to maintain, update, or health-check the site.
---

# Site maintenance for derekhsorensen.com

This repo is a personal website built with **forester** (Jon Sterling's OCaml forest tool), currently pinned to **5.0**. GitHub Pages serves the committed `docs/` directory; `output/` is the gitignored build directory. The domain `derekhsorensen.com` sits behind Cloudflare.

This skill is for site health and upgrades; for adding notes/logs/talks/papers, use the `/add-content` skill instead.

Run the checks below in order. Fix what's broken or outdated; report anything that needs a human decision (major version migration, breaking upstream changes) with a concrete recommendation instead of silently doing it.

## 1. Version check

- `forester --version` must report the version pinned in the guard at the top of `build.sh` (also guarded in `new.sh` and `log.sh`). If forester isn't installed: `opam install forester.5.0` (requires OCaml ≥ 5.3.0).
- Find the newest upstream release (do NOT trust the GitHub mirror — it's stale; development is on sourcehut):
  ```bash
  git ls-remote --tags https://git.sr.ht/~jonsterling/ocaml-forester | awk -F/ '{print $NF}' | sort -V | tail -3
  ```
  Cross-check https://ocaml.org/p/forester/latest/versions for what's actually on opam (tags can precede opam release).
- **If a 5.x point release exists**: upgrade the opam package, bump the version-guard greps in `build.sh`/`new.sh`/`log.sh` and the version in `README.md`, refresh the theme (section 4), rebuild, verify (section 5), publish.
- **If 6.0 (or later) is released**: do not auto-migrate — this is a breaking architectural change. See "Forester 6.0 migration" below, present a plan, and get confirmation.

## 2. XSLT-removal deadline (the "XML doomsday")

The site renders via client-side XSLT (`<?xml-stylesheet?>`), which browsers are removing:

- **Chrome 158 disables XSLT on 2026-11-17** (https://developer.chrome.com/docs/web-platform/deprecating-xslt). Firefox and WebKit/Safari have signaled the same.
- After that date, XML+XSLT sites render as raw text in affected browsers.

Each run: check how close this deadline is and whether forester 6.0 (which replaces XSLT with a built-in HTML renderer) has been released. If the deadline is near (< ~2 months) and 6.0 is out, escalate the migration to top priority. If the deadline is near and 6.0 is NOT out, flag it prominently — building 6.0 from the dev branch or another mitigation may need discussing.

## 3. Build & repo invariants

Run `./build.sh` and confirm it exits 0 with "Success!" and no diagnostics. The build script encodes three hard-won quirks of forester 5.0 — keep them intact:

1. **Assets are content-addressed**: 5.0 only emits `bafkr….pdf`-style copies. `build.sh` also copies `assets/` verbatim into `output/` so PDFs etc. keep stable URLs (`/docs/paper.pdf`). This also serves directory assets (e.g. `assets/slides/verso/zkproofs8/`) that content-addressing cannot.
2. **Asset links in trees must be absolute** (`/docs/…`, `/slides/…`, `/media/…`, `/img/…`). Pages live at `/<addr>/index.xml`, one directory deep, so relative links break. Lint for regressions:
   ```bash
   grep -rnE '\]\((docs|img|media|slides)/' trees --include="*.tree"   # should be empty
   ```
3. **Redirect stubs**: forester 4.x served each tree at `/<addr>.xml`; 5.0 moved them to `/<addr>/`. `build.sh` writes an XHTML meta-refresh file at each old `/<addr>.xml` path (browsers render XHTML-namespaced XML and honor the refresh, and GitHub Pages serves `.xml` as `application/xml`, so this works as a purely static redirect). Keep these — external links to the old URLs exist.

Also verify: `CNAME` exists at repo root (build copies it into output; `docs/` is regenerated wholesale on publish, so it must not be the only copy), `output/` is gitignored, and `theme/` customizations are limited to the six favicon files (see section 4).

Publishing = `./commit.sh "message"` (builds, replaces `docs/` wholesale, commits). Deploy is just merging to `main` — GitHub Pages serves `docs/`.

## 4. Theme freshness

`theme/` is a vendored copy of the upstream base theme with **zero local XSL/CSS/JS changes**. The only local files are the favicons: `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `apple-touch-icon.png`, `android-chrome-192x192.png`, `android-chrome-512x512.png`. When updating the theme (on any forester version bump), replace everything else wholesale from the matching upstream version and preserve those six files. Sources for the 5.x theme: `bin/forester/theme/` inside the ocaml-forester tag, or `https://git.sr.ht/~jonsterling/forester-base-theme` at the matching tag.

## 5. Live-site verification

After any publish (and as a periodic health check), verify locally first — `./view.sh`, then `xsltproc` is the fastest non-interactive render check:

```bash
xsltproc output/default.xsl output/index/index.xml > /dev/null && echo render OK
```

Then spot-check the live site:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://derekhsorensen.com/            # 200
curl -s https://derekhsorensen.com/index/index.xml | head -2                    # new-namespace XML
curl -s -o /dev/null -w "%{http_code}\n" https://derekhsorensen.com/default.xsl # 200
curl -s https://derekhsorensen.com/dhsorens-0004.xml | grep -c refresh          # 1 (redirect stub)
curl -s -o /dev/null -w "%{http_code}\n" https://derekhsorensen.com/docs/sorensen-research-statement.pdf  # 200
```

**Known post-deploy gotcha — the blank page**: Cloudflare edge-caches responses (`cache-control: max-age=600`), so for up to ~10 minutes after a deploy the site can serve a *mix* of old and new files. In particular, an old cached `default.xsl` (namespace `http://www.jonmsterling.com/jms-005P.xml`) applied to new XML (namespace `http://www.forester-notes.org`) matches nothing and renders a **blank page**. Diagnosis: compare the `xmlns` in live `/default.xsl` against live `/index/index.xml` — if they differ, it's the cache. Fix: wait 10 minutes or purge the Cloudflare cache. Not a code bug.

Also expected, not a bug: the browser address bar ends at `/<addr>/index.xml` — `/` redirects to `/index/`, and each tree directory's `index.html` forwards to its `index.xml`. That is forester 5.0's designed URL flow.

## Forester 6.0 migration (when released)

6.0's headline change is a **built-in HTML renderer** replacing the XML+XSLT pipeline, with theme resources bundled into the forester binary (announced goal: kill the theme-submodule/vendored-theme upgrade dance). When it ships, plan roughly:

1. Read the upstream release notes / migration guide first (forester-notes.org and the sourcehut repo); the notes below are educated expectations, not verified facts about 6.0.
2. The vendored `theme/` likely becomes obsolete — but port the six custom favicons into whatever customization mechanism 6.0 offers.
3. URLs will change again if output becomes `/<addr>/index.html`. Update the redirect story: the existing `/<addr>.xml` stubs must point at the new canonical URLs, and new redirects may be needed from `/<addr>/index.xml`. `/` + `/index/` behavior should be re-verified.
4. `build.sh` needs re-checking end to end: whether the CLI (`forester build forest.toml`) and `forest.toml` schema changed, whether assets are still content-addressed only (if 6.0 serves original paths, the verbatim `cp -R assets/. output/` may become unnecessary — but the absolute `/docs/…` links in trees still require the originals to exist), and the version guards need bumping.
5. The legacy XML renderer reportedly remains available in 6.0 — a fallback if the HTML renderer has issues, but it doesn't dodge the browser XSLT removal, so don't stay on it.
6. Rebuild, run all of section 5, and remember the Cloudflare cache gotcha when validating the deployed result.

## Report format

End with a short status summary: forester version (installed / pinned / latest upstream), 6.0 status, days until the Chrome XSLT cutoff, build result, live-site check results, and any actions taken or recommended.
