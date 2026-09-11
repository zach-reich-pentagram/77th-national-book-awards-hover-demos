# National Book Awards — interaction demos

`index.html` is the whole thing. Open it in a browser, or publish this repo
with GitHub Pages and send the link.

It exists so the interactions for the 77th Awards microsite can be **tried**
rather than described: three ways the header sub-navigation can open, two ways
"Get this book" can open, and the book riffle.

## Using it

The demo opens as the page alone, full screen. The **?** in the bottom-left
corner slides the control rail in over it; the same button, or Escape, puts it
away.

| Panel | What it changes |
| --- | --- |
| Header menu | **Row** — the categories arrive in a row under a dimmed top level. **Stack** — they stack under Honorees, left-aligned with it. **Replace** — they take the top level's place in the same band at the same height. |
| Get this book | **Hover** — the shops deal out beneath it and it fades back. **Click** — the shops replace it, with an arrow back. |
| Type, held open | The riffle on the category and the judges heading, which are always open. |
| Type, on hover | The riffle on whatever the cursor is on — the menu, the categories, the shop links. |
| The books | Hover a cover. Leaves, turn per leaf, gap, and the pivot. |
| Motion | Opening, closing, fading, the beat between items, and the curve. |

Everything starts on the studio's own settings. **Reset** puts them back.

## The riffle is ported, not approximated

Everything that decides how a deck looks is read out of the riffle studio's
`src/app.js`, so a setting means the same thing here as it does there:

| | |
| --- | --- |
| `cumulative()` | Σ spacing·cutoff^i — the studio's falloff, verbatim |
| tracking | thousandths of an em, which is what `TTF.layoutLine` is handed |
| weight fade | `heavy-centre`: heaviest at the middle out to Thin, `maxWeight` at Regular |
| the card | **every** copy sits on an opaque card, the centre one included |
| the gap | a **ring** — the studio cuts each copy against the copies in front of it, each outset by `gap`, so the space is on every shared edge |
| the pivot | centre + (pivot/100)·half, i.e. `50% + pivot/200` in `transform-origin` |
| scale | spacing **and** gap are pixels at the studio's own size and are scaled together: by `fontSize / 166` for type, by `coverWidth / 280` for a cover |

The books use the studio's **Page fan** preset — `count 10, spacing 14.5,
cutoff 0.91, gap 3, rotation 2.5°, pivot 30 / -11` — and the panel carries the
same sliders with the same names and ranges, so it can be dialled to match a
studio screenshot exactly.

## The type scale

Three sizes carry the page, set as variables at the top of the stylesheet:

| | |
| --- | --- |
| `--t-body` | 20px — body copy and the header nav |
| `--t-sub` | 36px — Winner, Finalists, Longlist |
| `--t-head` | 48px — the riffled Ergon headings |

A book title sits one step above body (`--t-title`, 28px; 24px in the grids) so
the hierarchy survives a body size that large. The riffle follows the type on
its own — spacing and gap are pixels at the studio's 166px and are scaled by
each element's own font-size — so a 48px heading riffles at the same proportion
a 40px one did.

## The lockup

The burgundy band under the nav holds the awards lockup. It is **not** sticky:
the nav stays at the top and the lockup scrolls away under it, which is what
makes the burgundy appear to shrink to the nav as you go down.

It looks for `logo.svg` beside the page. If that file is not there, the lockup
is set live in Ergon and riffled with the demo's own machinery — which is how
the artwork was made in the first place — and sized to fill the band. **Drop
the real `logo.svg` in next to `index.html` and it takes over with nothing else
to change.** The live-text stand-in has no book glyph.

Its size is solved rather than measured: a riffled box has a transition on its
width, so reading it back mid-change gives a number on its way somewhere. The
plain word is measured instead, and what the riffle adds is known —
`cumulative(count, spacing, cutoff)` each side, in pixels at the studio's 166px
type, so a fixed multiple of the font size.

## Two things that are not the site

- **"Winner" is set in the text face, not Ergon.** On the site every heading is
  Ergon in caps; in the mockup it is plainly the text face, low contrast and in
  sentence case. The mockup is what was asked for. One line in `.winner`
  switches it back.
- **The book covers and judges' portraits are grey plates**, as in the mockup.

## The lockup

The burgundy band under the nav holds the awards lockup. It is **not** sticky:
the nav stays at the top and the lockup scrolls away under it, which is what
makes the burgundy appear to shrink to the nav as you go down.

It looks for **`logo.svg` at the root of this repo, beside `index.html`**. Drop
the real artwork in and it takes over with nothing else to change. Until then
the lockup is set live in Ergon and riffled with the demo's own machinery —
which is how the artwork was made in the first place — and sized to fill the
band. The live-text stand-in has no book glyph.

## Rebuilding it

`index.html` is generated. Edit `src/riffle-demo.src.html`, then:

```sh
cd src
python3 build.py            # embeds the fonts, writes riffle-demo.html
python3 build.py --no-fonts # leaves them out, falls back to the system sans
```

`build.py` reads the `.woff2` files from the design repo
(`wordpress/riffle-header/fonts`); point `FONTS` at wherever they are on your
machine. Copy the result over `index.html`.

## On the fonts

Ergon and Basel Classic are commercial faces, embedded in `index.html` as data
URIs so the demo is genuinely one file. That is the same thing a PDF comp does,
but in a public repository it does mean the font data is downloadable by anyone
with the link. `python3 build.py --no-fonts` produces the version that carries
no font data, if this ever needs to go somewhere the licence does not follow.
