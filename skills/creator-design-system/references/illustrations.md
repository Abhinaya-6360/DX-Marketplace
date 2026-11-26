# Illustrations (Figma: Guides · Imagery › 06 · Illustrations)

Flat, geometric drawings in CDS colours, for ideas a screenshot or photo can't show: a process
(order to cash, approvals, onboarding), a connection (integrations, extending a legacy system), a
result (growth), a view (dashboards), a team, an industry. Claude draws them in this style whenever
someone asks for an illustration or a picture for a post, email, slide or web draft.

**Draw for the content.** The six references are examples of the style, not a fixed set. Read what
the piece is about, pick the two or three things that tell that story (the objects, the flow
between them, the result), and draw a new illustration from the same parts. Use a reference as it
is only when it already tells that exact story.

## Which picture to use (in this order)

1. **A real product screenshot** from the marketer — best proof, always first for product claims.
2. **A CDS illustration**, drawn by Claude in this style — when the idea is a process or concept.
3. **A stock illustration** the marketer supplies — fine when it's flat 2D, licensed, and
   recoloured to CDS (people are best done this way).
4. **The CDS 3D tile** (social, YouTube, email only) with one icon.
5. **No picture** — the statement versions of the templates.

Offer these as options; draw the illustration when it fits, and never generate photos or
real-looking product screens.

## The style

- Canvas 800 × 600, flat 2D. A soft ground shadow (`ground()`); the Creator diamond behind the
  picture is **optional** — only when it needs grounding.
- **Colour:** CDS only. Blues (blue/100 main, blue/130 for strong lines, blue/70 connectors,
  blue/40–20 light fills) and greys carry the picture. Other CDS colours are allowed as **small
  accents, under 8% of the picture** (`illustration.py check` measures it), each with a meaning:
  - yellow (yellow/90, yellow/60, yellow/40): highlights, money, the current step;
  - green (green/90, green/40, green/20): done, approved, success;
  - red (red/90, red/20): only a stop, an error or a rejected step;
  - violet (violet/100, violet/20): only on AI pieces, with the ai-sparkle icon.
  Never colours outside CDS.
- **Shapes:** rounded rectangles from the radius scale, circles, flat offset shadows (blue/40
  under white, blue/30 under colour). No gradients, no blur, no outlines except 6–10 px lines.
- **Lines and arrows:** round ends, 45° bends; an arrow head sits on a 45° last segment.
  Lines run around shapes, never through them.
- **Icons:** CDS icons only, inside tiles (`tile()`), white on blue or blue on white.
- **Documents and screens:** grey bars instead of words (`lines()`); app windows are clearly
  schematic.
- **Never:** people drawn in code, the Creator or Zoho logo (don't rebuild it), real words or
  numbers, other brands' logos, a real-looking Creator screen, 3D or photo-real effects.
- One illustration per piece, in the template's picture slot; never behind text.

## Compose it like a design lead

- **Fill the space.** In a post the illustration is the second thing people see after the headline.
  render_social crops it to the drawing and scales it to fill the picture zone (the full width
  between the text margins, clear of the logos), so draw for that shape: a wide band of about
  3 : 1 for Feature, Story and carousel slides; about 3 : 2 beside text (Landscape, X).
- **Give it weight.** Two or three main objects of similar size (cards about 230–250 wide and
  300 tall on the 800 × 600 grid), evenly spaced, with short connectors between them. No tiny
  pieces floating in empty space.
- **Add the detail that tells the story**, not decoration: a header bar with an icon on each card,
  form fields, a checklist with ticks, an avatar on a profile card, one accent badge on the result.
- **One focal point:** the result (the last card, the coin, the approved badge) gets the accent.
- **Align the text to it:** with the illustration centred below, the tag, headline and supporting
  text are centred above it (Feature switches to its Illustration layout; other templates are
  centred by the renderer). Beside text, the text stays left-aligned.
- **Look at it in place** (render the post, not just the SVG) and fix anything small, crowded or
  unbalanced before handing over.

## The six references (`assets/illustrations/style/`)

| File | Shows |
| --- | --- |
| `01-order-to-cash` | an order becomes an invoice, then cash |
| `02-integrations` | Creator in the middle, connected to systems around it |
| `03-approvals` | a request moves through review to approved |
| `04-growth` | results rising over time |
| `05-dashboard` | a schematic app window with charts |
| `06-extend-legacy` | Creator apps plug into an existing ERP or old system |

Use one as it is only when it tells exactly the right story; otherwise draw a new one for the
content from the same parts (for example, customer onboarding: a sign-up form, a checklist with
green ticks, a team tile with a green done badge).

## How to draw and place one

```python
import sys; sys.path.insert(0, "scripts")
from illustration import *
b = ground()
b += tile(80, 260, 130, "shopping-cart")                  # icon names: python scripts/icon.py find <word>
b += card(320, 170, 170, 230) + lines(342, 245, 4, 126)
b += path("M210 325 L255 325 L285 295 L320 295")
b += coin(660, 320)
save("order-to-cash.svg", b)                               # marked data-cds-illustration="new"
```

1. `python scripts/illustration.py check order-to-cash.svg` — fix everything it lists.
2. `python scripts/illustration.py show order-to-cash.svg look.png` — look at it; fix overlaps,
   lines through shapes, crowding.
3. Put it in the picture slot: `"illustration": "order-to-cash.svg"` in a render_social brief
   (Feature product versions and others with a screenshot slot), or as the image in a web
   section, newsletter or slide.
4. The handover lists it under **New illustration for design review** (check_system prints it).

**Stock illustrations:** put the file in `"illustration"` the same way. `check_system.py
<file>.png` lists any colours outside CDS (IMAGE NOTE) with the nearest CDS colour; ask the
marketer to recolour them, and to confirm the licence. Skin and hair can stay natural.
