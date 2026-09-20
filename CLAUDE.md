**Date:** 2026-09-20
**Status:** CURRENT

# kodamatrade.com

This repository is **public**. It serves five pages at kodamatrade.com through GitHub Pages via
`CNAME`. Pushing to `main` deploys, and there is no staging.

**The working rules for this apartment are not in this repository, deliberately.** They live
beside it on SCOUT, outside the published tree, at `_ops/CLAUDE.md`. If you are reading this
without access to that file, you do not have what you need to change this site safely: stop, and
ask the owner.

Two things worth knowing before you touch anything, because getting either wrong is silent:

- **`strategy.html`, `subscriptions.html`, `our-story.html` and `disclosures.html` are build
  output.** Editing them directly works until the next build overwrites you without a word. Edit
  the fragments in `_src/sources/` instead. `index.html` and `members.html` are hand-edited whole
  files and this repository is their only home.
- **The builder is not in this repository.** It is run from `_ops/build/` on SCOUT and refuses to
  run without its configuration.

Nothing operational, internal or self-critical belongs in this repository. If a file is in this
apartment and not in `_ops/`, assume the world can read it.
