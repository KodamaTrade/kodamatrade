#!/usr/bin/env python3
"""
Rebuild the assembled kodamatrade.com pages from _src/.

Standard library only, so it runs on SCOUT's bare python3 without the
automation venv. Run from anywhere:  python3 _src/build.py

Writes strategy.html, subscriptions.html and our-story.html to the repo root.
index.html and members.html are NOT built: they are hand-edited whole files and
the copy at the repo root is their only home.

Every write is temp-file + os.replace, so a failed build never truncates a live
page. Every assertion below exists because something once went wrong; do not
weaken one to make a build pass. If an assertion fires, the page is wrong.
"""
import base64, hashlib, os, re, sys

SRC  = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)

# The logo has ONE home: the PNG at the repo root. The data URI is derived from
# it at build time. Never paste a data URI into a source fragment.
MARK     = 'kodama_mark_2026-09-06.png'
MARK_SHA = 'eb03b0a7721967dd76dbe913841337f6e1ad62411efa7085ff813104bf9c4379'

PAGES = [
    ('strategy.html',      'strategy.head.html',  'strategy.body.html',  12, True),
    ('subscriptions.html', 'subs.head.html',      'subs.body.html',      12, True),
    ('our-story.html',     'our-story.head.html', 'our-story.body.html', None, False),
]

# Retired vocabulary. Pre-client review gate, item 1.
RETIRED = ['Bonsai Breakout', 'Tanuki', 'Elite 50', 'Active 83', 'Active 82',
           'Golden 18', 'Golden ETF', 'replica', 'Raymond James', 'Canon']

# Locked production parameters. IP rule: results may be shown, settings may not.
PARAMS = ['20/50', '2/8 SMA', '15% pullback', '60-day lookback', '60 day lookback',
          'MIN_HOLD_BARS', 'LADDER_MIN_UNITS', 'PRUNE_FLOOR', 'MIN_PRUNE_UNITS']

problems = []

def check(cond, msg):
    if not cond:
        problems.append(msg)

def body_of(s):
    i = s.find('<body>')
    return s[i:] if i >= 0 else s

def logo_uri():
    p = os.path.join(ROOT, MARK)
    raw = open(p, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != MARK_SHA:
        sys.exit('FAIL: %s sha256 is %s, expected %s.\n'
                 'The 2026-09-06 mark is the only approved logo. If it really '
                 'changed, update MARK_SHA deliberately and say so in the commit.'
                 % (MARK, sha, MARK_SHA))
    return 'data:image/png;base64,' + base64.b64encode(raw).decode('ascii')

def build(out, head, body, clauses, no_signal, uri, disclosure):
    hp = os.path.join(SRC, 'sources', head)
    bp = os.path.join(SRC, 'sources', body)
    s = open(hp).read() + open(bp).read()

    check(s.count('__LOGO__') == 1,
          '%s: expected exactly one __LOGO__ token, found %d' % (out, s.count('__LOGO__')))
    n_disc = s.count('__DISCLOSURE__')
    check(n_disc <= 1, '%s: %d __DISCLOSURE__ tokens' % (out, n_disc))
    if clauses is not None:
        check(n_disc == 1, '%s: disclosure token missing' % out)

    # CSS brace balance. A stray brace silently kills every rule after it.
    try:
        css = s[s.index('<style>') + 7:s.index('</style>')]
        check(css.count('{') == css.count('}'),
              '%s: CSS brace imbalance, %d open %d close' % (out, css.count('{'), css.count('}')))
    except ValueError:
        problems.append('%s: no <style> block found' % out)

    check(s.rstrip().endswith('</html>'), '%s: does not end with </html>' % out)

    s = s.replace('__LOGO__', uri).replace('__DISCLOSURE__', disclosure)
    b = body_of(s)

    # Disclosure clause count. Twelve as deployed 2026-09-08. Clauses 3 and 4
    # are held out for John to edit; two more are bracketed pending counsel.
    if clauses is not None:
        i = b.index('class="discl-full"')
        j = b.index('</details>', i)
        got = len(re.findall(r'<li>', b[i:j]))
        check(got == clauses, '%s: %d disclosure clauses, expected %d' % (out, got, clauses))

    # John's ruling 2026-09-08: the desks receive signals, Kodama publishes
    # trade alerts. "Signal" implies advice in subscriber-facing copy.
    if no_signal:
        hits = len(re.findall(r'(?i)signal', b))
        check(hits == 0, '%s: "signal" appears %d times in subscriber-facing copy; '
                         'use "alert" for what we publish, "trigger" for what fires' % (out, hits))

    for term in RETIRED:
        pat = r'(?i)\b' + re.escape(term) + r'\b'
        check(not re.search(pat, b), '%s: retired vocabulary "%s"' % (out, term))

    for term in PARAMS:
        check(term not in b, '%s: parameter leak "%s"' % (out, term))

    # The registered name is permitted only as the full legal entity, in the
    # copyright line and the disclosure. Never as a brand.
    for m in re.finditer(r'Kodama Mori', b):
        check(b[m.start():m.start() + 24] == 'Kodama Mori Trading Inc.',
              '%s: "Kodama Mori" not written as the full legal entity name' % out)

    return out, s

def main():
    uri = logo_uri()
    disclosure = open(os.path.join(SRC, 'snippets', 'disclosure.html')).read()
    built = []
    for out, head, body, clauses, no_signal in PAGES:
        built.append(build(out, head, body, clauses, no_signal, uri, disclosure))

    if problems:
        print('BUILD FAILED, nothing written:', file=sys.stderr)
        for p in problems:
            print('  ' + p, file=sys.stderr)
        sys.exit(1)

    for out, s in built:
        path = os.path.join(ROOT, out)
        data = s.encode('utf-8')
        open(path + '.tmp', 'wb').write(data)
        os.replace(path + '.tmp', path)
        print('%-20s %7d bytes  %s' % (out, len(data), hashlib.sha256(data).hexdigest()[:16]))

if __name__ == '__main__':
    main()
