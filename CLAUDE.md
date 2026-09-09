**Date:** 2026-09-08
**Status:** CURRENT
**Scope:** this repository only. The wider working rules are in `~/Documents/CLAUDE.md`.

# kodamatrade.com

This repo is the public Kodama website, served by GitHub Pages at kodamatrade.com via the
`CNAME` file. Pushing to `main` deploys. There is no staging environment, so a bad push is
live within a minute or two.

## READ FIRST: THIS SESSION MAY BE HOLDING A STALE CLONE

Until 2026-09-08 this site was edited through the GitHub web upload page by a Cowork session,
because the Linux VM that session reaches has no route to GitHub (DNS does not resolve, HTTPS
returns 403 from the proxy) and no SSH key. Seven commits went in that way. If your clone
predates them, pull before you touch anything.

## THE TWO KINDS OF PAGE

**Assembled pages.** `strategy.html`, `subscriptions.html` and `our-story.html` are BUILD
OUTPUT. Never edit them directly; the next build silently reverts you. Edit the fragments in
`_src/sources/` and rebuild:

    python3 _src/build.py

Standard library only, so it runs on SCOUT's bare python3 without the automation venv.

**Hand-edited pages.** `index.html` and `members.html` are whole files with no fragments. The
copy in this repo is their only home. Edit them directly.

## THE BUILD, AND WHY EVERY ASSERTION IS THERE

`_src/build.py` concatenates `<page>.head.html + <page>.body.html`, substitutes two tokens, and
writes to the repo root. It writes to a temp file and `os.replace`s, because
`open(path,'w').write(transform(open(path).read()))` truncates the target before it evaluates
the argument, and that emptied a body file to zero bytes on 2026-09-05.

Nothing is written unless every page passes every check. The checks are not style preferences.
Each one is a thing that went wrong:

- `__LOGO__` appears exactly once. The logo has ONE home, `kodama_mark_2026-09-06.png` at the
  repo root, and the data URI is derived from it at build time. Its sha256 is pinned in
  `build.py`; if the file changes the build stops. Never paste a data URI into a fragment.
- CSS braces balance. A stray brace kills every rule after it and the page still renders,
  just wrongly.
- The file ends with `</html>`.
- `strategy.html` and `subscriptions.html` each carry exactly **12 disclosure clauses**.
  Clauses 3 and 4 are deliberately held out for John to edit; two more are bracketed pending
  counsel. The disclosure text lives once, in `_src/snippets/disclosure.html`, and is
  substituted for `__DISCLOSURE__`. It used to be duplicated inline in both pages, which is
  exactly how legal text drifts apart.
- The word **"signal" does not appear** in subscriber-facing copy on those two pages. John's
  ruling of 2026-09-08: the research and trade desks receive signals from the model, Kodama
  publishes **trade alerts**. In public copy, "signal" reads as advice. What fires inside the
  model is called a **trigger** (Nebari the entry trigger, Hasami the exit trigger).
  `our-story.html` is exempt because it carries John's verbatim copy about Mike.
- No retired vocabulary: Bonsai Breakout, Tanuki, Elite 50, Active 83, Golden 18, Golden ETFs,
  Canon, replica, Raymond James. Raymond James is entirely separate from Redwood, Bonsai and
  Kodama and must never appear or be implied.
- No parameter leaks. The IP rule is that subscribers see outputs, never settings. The moving
  averages, pullback threshold, lookback, tier scoring formula, pruning mechanics and funding
  waterfall are never published.
- "Kodama Mori" appears only as the full legal entity name `Kodama Mori Trading Inc.`, which is
  permitted in the copyright line and the disclosure clause that identifies the publisher. The
  brand in all writing is **Kodama**, one word, or **Kodama Trade**, two words.

If an assertion fires, the page is wrong. Do not weaken the assertion to make the build pass.

## WHY `_src` STARTS WITH AN UNDERSCORE

GitHub Pages runs Jekyll on this repo, and Jekyll excludes underscore-prefixed directories from
the published site. That keeps the fragments out of kodamatrade.com. Nothing in `_src/` is
secret, since it is the same text as the built pages, so this is tidiness rather than security.
If anyone adds a `.nojekyll` file the exclusion stops and the sources become publicly served.
Worth knowing, not worth panicking about.

## DEPLOYING

    python3 _src/build.py
    git add -A && git commit && git push

Then **verify the deploy rather than assuming it**. Two separate failure modes have bitten this
site:

1. Under the old browser-upload workflow, GitHub's Commit button moves down about 17 pixels when
   the ProTip line appears after you type a message. Five commits were silently swallowed across
   two sessions before anyone noticed. `git push` removes that failure mode entirely, which is
   the main reason this repo should now be driven from Claude Code rather than a browser.
2. The Pages CDN serves the old file for up to a couple of minutes. Confirm the live page, not
   just the push.

One trap when you check: `fetch(...).then(r => r.text()).length` counts CHARACTERS, while the
GitHub API reports BYTES. `subscriptions.html` contains 132 bytes of multibyte UTF-8, so the two
differ by 132 and it looks like a stale CDN copy when nothing is wrong. Compare bytes to bytes:

    curl -s https://kodamatrade.com/subscriptions.html | wc -c

## PERFORMANCE FIGURES

Every number on `strategy.html` is hard-coded, and **nothing links the page to its source**. It
will go stale silently. This is the most likely way the site becomes wrong.

The one home for every figure is the Model Portfolio store on SCOUT, read via
`modelportfolio_stats.py` in the automation venv. Never type a figure from memory, from a
document, or from an earlier message, and never carry one forward from this file. Regenerate
before changing any of them. Bare `python3` on SCOUT lacks numpy and pandas, so run the stats
module with the automation venv even though `build.py` itself does not need it.

Figures currently on the page are as of the **2026-09-04 close** and are labelled "based on
backtested results", which they must remain. The claim of 19 calendar years beating SPY is 18
complete years plus 2026 to date, and the page says so; do not shorten that to "19 years".

Two methodology points that were wrong in draft and are now right. Trade statistics aggregate at
the **position** level, one position from entry to final exit, with partial sales folded in
(65.2% win rate, 3.51 profit factor). Counting final-exit legs only gives 58.4% and 1.72, which
understates the model because a trim removes profit from a winner before its final exit. And the
model's drawdown was **deeper** than SPY's in three of the five tested declines; the honest story
is the recovery and the capture ratios, not a claim that it falls less.

Building a check that reads the store and fails when a page figure no longer matches it is
registered work and is not done. It is the single highest-value thing to add here.

## COMPLIANCE STATUS OF THESE PAGES

None of `strategy.html`, `subscriptions.html` or `our-story.html` has been through the
pre-client review gate. Item 8 of that gate, internal review completed and logged, is not
satisfied for any of them. They are public on John's stated basis that nobody can subscribe yet,
so the exposure is presentational rather than transactional. That basis expires the moment a
payment link works.

The publisher versus adviser classification is unresolved and is the legal critical path.

## OPEN ITEMS AGAINST THIS SITE

- `strategy.html` claims results were reproduced on "multiple separate professional investment
  platforms". Nothing documents this. Name the platforms and record it, or soften the sentence.
- `subscriptions.html` cites a $25,000 capital floor in a study line and $35,000 in the table.
  One of them is wrong.
- The four Stripe Payment Links do not exist, so the Subscribe buttons are disabled.
- `members.html` still carries the old unlinked footer.
- The daily email is still titled "Kodama Daily Signals" and becomes "Daily Alerts". That is not
  a site change; it touches the renderer subject line, the wrapper's delivery audit which
  inspects subject prefixes, the operations manual and the instruction blocks, and it goes
  through `CHECKLIST_Email_Template_Change_2026-08-09.md`.
- `charts/` was created by a separate conversation for the newsletters. Leave it alone.
- `.git/index.lock.stale_2026-09-08` is a zero-byte leftover from a failed checkout in a session
  that could not delete files. Harmless. `rm` it whenever convenient.

## WHERE THINGS ARE WRITTEN DOWN

The Claude project document store is retired to read-only history as of 2026-09-08. Disk is the
single home, so a pointer written anywhere as `claude/<name>.md` means a filesystem path.

- Filing rules, the paste block for any session: `Redwood_Central/07_Shared_Memory/SAVE_HERE_2026-09-08.md`
- Session history and decisions: `Redwood_Central/07_Shared_Memory/`
- This site's build and deploy record: `07_Shared_Memory/sessions/RECORD_Session_2026-09-08_Strategy_Page_and_Disclaimer.md`
- The alerts-not-signals ruling: `07_Shared_Memory/decisions/DECISION_Trade_Alerts_Not_Signals_2026-09-08.md`
- Open items across everything: `Documents/Claude outputs/AGENDA_Open_Items.md`
- Dated snapshots of the built site: `Documents/KodamaTradeBackup/`

Every document opens with a date and one of four statuses in its first five lines: CURRENT,
SUPERSEDED by <filename>, FROZEN (record), or DRAFT. When you supersede something, edit the old
one so its status names the successor. Prefer editing an existing document over creating a new
one, and point at a fact's home rather than copying the value.

## HOUSE STYLE FOR COPY ON THIS SITE

No em dashes. The research desk is framed as a chef on television: we show every step we take
and let people watch, and we never show the recipe. So the trades are shown in full, the work is
not. "Shows the receipts", never "shows its work". Do not write anything implying the rules,
thresholds or logic will be shared. Push back with data rather than softening.
