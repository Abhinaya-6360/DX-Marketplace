---
name: creator-design-system
description: Zoho Creator's CDS 2.0 brand system for marketing work. Use it for anything Zoho Creator marketers make — presentations and decks for Zoho Show, LinkedIn/Instagram/X/Facebook posts, stories, carousels, YouTube thumbnails, video backgrounds, email headers, email newsletters, banners, webinar promos, customer-quote posts, landing pages and zoho.com/creator web drafts. Trigger whenever the request mentions Zoho Creator, Creator, CDS, our brand, brand guidelines, on-brand, a deck, slides, a post, a banner, a thumbnail or a campaign asset, even if the user doesn't name the design system. It holds the CDS 2.0 tokens, logos, fonts, gradients, the 45-slide Zoho Show deck, and the brand rules (red only for the main CTA, violet only for AI and partner content, Zoho logo placement), and it builds decks as editable .pptx and visuals as exact-size PNGs.
---

# Zoho Creator · CDS 2.0

CDS 2.0 is Zoho Creator's design system for marketing. The source of truth is the CDS-2.0
Figma file; everything in this skill was exported from it. Use only what's here: never type a
colour, size, gradient or logo from memory.

People using this are usually marketers, not designers. Talk to them in plain language, ask
for missing facts instead of inventing them, and always tell them what they still need to
replace or confirm.

Use the same everyday words as the brand guidelines site (its "Words we use" page). Design
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
   - `assets/icons/icons.json` — the CDS icon set (318 icons, Regular and Fill) with tile spec and rules; get any icon with `python scripts/icon.py <name>` (`list` shows all names).
   - `assets/shapes/` — Shape kit v1.0 (set `color` to a token).
   - `assets/patterns/` — Connect tiles (light and bold) for the calm texture.
   - `assets/fonts/` — Zoho Puvi Regular, Medium, Semibold, Bold.
   - `assets/swatches/` — CDS-2.0-print-swatches.ase (official CMYK) and CDS-2.0-screen-swatches.ase (RGB) for agencies, printers and designers.
   - `assets/social/layouts.json` — the social, video, email and YouTube templates; `scripts/render_social.py` renders them to PNG and checks them.
   - `assets/print/layouts.json` — the print templates; `scripts/render_print.py` makes CMYK PDFs with bleed.
   - `scripts/build_web.py` — builds web page drafts from the Templates · Web sections.
   - `scripts/build_email.py` — builds email newsletters (email-safe HTML + images, zipped).
   - `assets/deck/` — the 45-slide Zoho Show deck (plus one divider slide); `scripts/build_deck.py` and `check_deck.py` build and check decks.
4. Before handing anything over, run through `references/brand-check.md`, fix what fails, and
   give the marketer the "tell the marketer" list.

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
