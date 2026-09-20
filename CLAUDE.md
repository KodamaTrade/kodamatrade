**Date:** 2026-09-20
**Status:** CURRENT

# kodamatrade.com

This repository is **public**. It serves the pages at kodamatrade.com through GitHub Pages via
`CNAME`. Pushing to `main` deploys, and there is no staging.

**The working rules for this site are not in this repository, deliberately.** They live outside it,
on the machine that builds the site. If you are reading this without access to them, you do not
have what you need to change this site safely: stop, and ask the owner.

Two things worth knowing before you touch anything, because getting either wrong is silent:

- **`strategy.html`, `subscriptions.html` and `our-story.html` are build output.** Editing them
  directly works until the next build overwrites you without a word. Edit the fragments in
  `_src/sources/` instead. `index.html` and `members.html` are hand-edited whole files and this
  repository is their only home.
- **The builder is not in this repository either.** It runs from outside the published tree and
  refuses to run without its configuration.

If a file is in this repository, assume the world can read it.
