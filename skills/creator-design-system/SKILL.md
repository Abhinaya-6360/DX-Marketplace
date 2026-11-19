---
name: creator-design-system
description: Zoho Creator's CDS 2.0 brand system for marketing work. Use it for anything Zoho Creator marketers make — presentations and decks for Zoho Show, LinkedIn/Instagram/X/Facebook posts, stories, carousels, YouTube thumbnails, video backgrounds, email headers, email newsletters, banners, webinar promos, customer-quote posts, landing pages and zoho.com/creator web drafts. Trigger whenever the request mentions Zoho Creator, Creator, CDS, our brand, brand guidelines, on-brand, a deck, slides, a post, a banner, a thumbnail or a campaign asset, even if the user doesn't name the design system. It holds the CDS 2.0 tokens, logos, fonts, gradients, the 45-slide Zoho Show deck, and the brand rules (red only for the main CTA and form error messages, violet only for AI and partner content, Zoho logo placement), and it builds decks as editable .pptx and visuals as exact-size PNGs.
---

# Zoho Creator · CDS 2.0

CDS 2.0 is Zoho Creator's design system for marketing. The source of truth is the CDS-2.0
Figma file; everything in this skill was exported from it. Use only what's here: never type a
colour, size, gradient or logo from memory.

People using this are usually marketers, not designers. Talk to them in plain language, ask
for missing facts instead of inventing them, and always tell them what they still need to
replace or confirm.

Use the same everyday words as the brand guidelines site. Design
names stay in the files and in Figma; in what you say to marketers, use the plain word first
and give the design name in brackets only when they need to find it in Figma:

| Design name | Say |
| --- | --- |
| lockup / mark | full logo / logo symbol |
| clear space | empty space around the logo |
| mesh (mesh-soft-blue, mesh-soft-ai, mesh-partner) | light background · Blue / AI / Partner |
| CTA, Primary / Secondary / Inverse / Link button | main button, outline button, white button, text link |
| role/text/body and other roles | what it's for: body text colour, main button colour… |
| step 100, 10–180 scale | shade 100, shades from light (10) to dark (180) |
| breakpoint, gutter | screen size, gap between columns |
| tracking, line height | letter spacing, line spacing |
| AA / AAA | easy to read / very easy to read |
| safe area | the border text and logos must stay inside |
| detach | break the template's link to the library |

Radius and elevation keep their names (radius: how rounded the corners are; elevation: the
shadow that lifts something off the page). Template and pattern versions keep their names too
(Light and Bold, Calm and Bold, Blue, Ink, Light, Violet, Brand depth, Midnight, Glow).

## System first: stay in CDS 2.0 and flag every violation

Everything you make uses only the system: CDS colours and gradients, Zoho Puvi text styles,
the spacing and radius scale, elevation styles, CDS logos, shapes and patterns, the CDS icon
set and the CDS templates. Never improvise outside it.

- **No emoji or outside symbols, anywhere**: not in headlines, lists, buttons, slides, posts
  or emails (🚀 ✅ ⭐ ✨ 👉 ✓ ★ …). Where an emoji would go, use a CDS icon in a CDS icon tile
  (`python scripts/icon.py list`), or leave it out.
- **Icons always come from the CDS 2.0 icon set** (`assets/icons/icons.json`, via
  `scripts/icon.py`). Never take one from the web or another set, an icon font, emoji or an
  image generator. Only if no CDS icon fits the meaning, draw a new one in the CDS custom style
  (rules in `references/brand-rules.md` › Icons), mark it `data-cds-new-icon="<name>"`, and list
  it in the handover as a new icon for the design team to review and add to the library.
- **Readable for everyone (WCAG AA)**: normal text 4.5:1, large text (24 px and up, or 19 px
  Semibold) and icons 3:1. Use the pairs from `python scripts/check_system.py pairs`; check
  anything else with `python scripts/check_system.py contrast <text> <background>`.
- **Elegant by default**: one message and one focal point, generous space from the spacing
  scale, one accent colour plus the brand blue, Semibold headings with Regular body, no more
  than three text sizes in a block, and the CDS template layout untouched.
- **Flag violations, every time.** When a request, a brief, pasted copy or a file you're
  given breaks the system (an emoji, an outside colour or font, a non-CDS icon, red that isn't
  the main button, violet outside AI or partner content, text that fails AA, a pattern behind
  a face, a generated product screen…), don't quietly do it and don't quietly drop it. Say in
  one plain line what doesn't fit and why, offer two or three on-system options that look good
  and pass AA, and build the best one by default. Only if the marketer still insists, make it
  with `--allow-violation` and list it under **System violations** in the handover.
- Every build and render script stops on emoji and outside colours in the brief;
  `scripts/check_system.py` checks the finished file. Every handover ends with one line:
  "System check: passes CDS 2.0" or the list of System violations.

## Always

1. Read `references/brand-rules.md` before making anything. Those rules are the brand.
2. Pick the module for the request and read its reference:

   | Request | Read |
   | --- | --- |
   | Presentation, deck, slides, pitch, webinar talk | `references/deck.md` |
   | Social post, story, carousel, thumbnail, video background, email header, banner | `references/social.md` |
   | Landing page, web page, web section, zoho.com/creator | `references/web.md` |
   | Business card, flyer, roll-up banner, anything printed | `references/print.md` |
   | Email newsletter, customer email, product update email | `references/email.md` |

3. Build with the files in this skill:
   - `design-system/tokens.css` — CSS variables for every colour, role, space, radius,
     elevation and the ten gradients, plus Zoho Puvi `@font-face` and text-style classes.
   - `design-system/tokens.json` — the same values for scripts.
   - `assets/logos/` — Creator lockup and Zoho logo, colour and white.
   - `assets/icons/icons.json` — the CDS icon set (363 icons plus 5 social logos, Regular and Fill) with tile spec and rules; get any icon with `python scripts/icon.py <name>` (`list` shows all names).
   - `assets/shapes/` — Shape kit v1.0 (set `color` to a token).
   - `assets/patterns/` — Connect tiles (light and bold) for the calm texture.
   - `assets/fonts/` — Zoho Puvi Regular, Medium, Semibold, Bold.
   - `assets/swatches/` — CDS-2.0-print-swatches.ase (official CMYK) and CDS-2.0-screen-swatches.ase (RGB) for agencies, printers and designers.
   - `assets/social/layouts.json` — the social, video, email and YouTube templates; `scripts/render_social.py` renders them to PNG and checks them.
   - `assets/print/layouts.json` — the print templates; `scripts/render_print.py` makes CMYK PDFs with bleed.
   - `scripts/build_web.py` — builds web page drafts from the Templates · Web sections.
   - `scripts/check_system.py` — the system guard: emoji, outside colours, fonts and icons, red and violet use, WCAG AA contrast; `pairs` lists the AA-safe colour pairs.
   - `scripts/build_email.py` — builds email newsletters (email-safe HTML + images, zipped).
   - `assets/deck/` — the 45-slide Zoho Show deck (plus one divider slide); `scripts/build_deck.py` and `check_deck.py` build and check decks.
4. Before handing anything over, run `python scripts/check_system.py <file>` on what you made
   (the .html, .pptx, or the brief .json for PNG and PDF output), then run through
   `references/brand-check.md`, fix what fails, and give the marketer the "tell the marketer" list.

## What to deliver

- **Decks**: an editable .pptx built from the master deck, ready to import into Zoho Show.
- **Social, video, email**: PNG at the exact size from the CDS template (plus PDF for carousels).
- **Web**: one self-contained HTML file plus a preview PNG, labelled as a draft for design and dev review.
- **Print**: a CMYK PDF at real size with 3 mm bleed and crop marks, for a designer to approve.
- **Newsletters**: a zip (index.html + images) for any email tool, plus a preview image.

Social posts, stories, carousels, email headers, video backgrounds and YouTube thumbnails can
be published by the marketer once the check passes and every sample is replaced. Web pages
and print go to a designer first.

## Swatch files

When someone asks for brand colours, swatches or a colour palette for an agency, printer or
designer, give them the files from `assets/swatches/` as downloads (print for printing,
screen for everything else) and say how to load them: Swatches panel › menu › Open Swatch
Library › Other Library. Never send hex or CMYK values typed from memory.

## When the brief is thin

Ask once, briefly, for what decides the result: the format or channel, the one message,
the audience, and any real numbers, quotes, photos or screenshots. If they say "just make
it", go ahead with sample slots left in place and list them in the handover.
