#!/usr/bin/env python3
"""Assemble the one-file demo: inline the Ergon and Basel faces as data URIs.

Kept as a builder rather than a hand-edited file so the fonts can be dropped
back out in one line if the demo ever has to go somewhere the licence does not
follow it — see the note in the README.
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).parent
FONTS = HERE.parent / 'riffle-header' / 'fonts'
# Two faces, not five. The demo sets everything in Basel; Ergon Regular is
# carried only so the one-line swap on .winner works without a rebuild. The
# Thin, Light and Medium cuts are for the weight fade across a riffled deck,
# which nothing here uses — they were 78KB of file for nothing.
# All four Ergon cuts are back: the weight fade across a riffled deck steps
# through the family, and with only Regular embedded every copy came out the
# same weight — which is most of why the type riffle did not look like the
# studio's.
FACES = [
    ('Ergon', 250, 'Ergon-Thin.woff2'),
    ('Ergon', 300, 'Ergon-Light.woff2'),
    ('Ergon', 400, 'Ergon-Regular.woff2'),
    ('Ergon', 500, 'Ergon-Medium.woff2'),
    ('Basel Classic Book', 400, 'BaselClassic-Book.woff2'),
]

embed = '--fonts-embedded' not in sys.argv[1:] or True
if '--no-fonts' in sys.argv[1:]:
    css = ('/* Fonts left out of this build. Ergon and Basel Classic are\n'
           '   commercial faces; the page falls back to the system sans. */\n')
else:
    out = ['/* Ergon and Basel Classic, embedded so this is one file.\n'
           '   Both are commercial faces licensed for this project — see the\n'
           '   README before sending this file outside it. */']
    for fam, wt, name in FACES:
        p = FONTS / name
        if not p.exists():
            raise SystemExit('missing font: ' + str(p))
        b64 = base64.b64encode(p.read_bytes()).decode('ascii')
        out.append(
            '@font-face{font-family:"%s";font-weight:%d;font-style:normal;'
            'font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}'
            % (fam, wt, b64))
    css = '\n'.join(out)

src = (HERE / 'riffle-demo.src.html').read_text()
if '/*@FONTS@*/' not in src:
    raise SystemExit('no /*@FONTS@*/ placeholder in the source')
dst = HERE / 'riffle-demo.html'
dst.write_text(src.replace('/*@FONTS@*/', css))
print('built %s  (%.0f KB)' % (dst, dst.stat().st_size / 1024))
