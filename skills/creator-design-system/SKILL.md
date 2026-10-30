---
name: creator-design-system
description: Zoho Creator's CDS 2.0 brand system for marketing work. Use it for anything Zoho Creator marketers make — presentations and decks for Zoho Show, LinkedIn/Instagram/X/Facebook posts, stories, carousels, YouTube thumbnails, video backgrounds, email headers, banners, webinar promos, customer-quote posts, landing pages and zoho.com/creator web drafts. Trigger whenever the request mentions Zoho Creator, Creator, CDS, our brand, brand guidelines, on-brand, a deck, slides, a post, a banner, a thumbnail or a campaign asset, even if the user doesn't name the design system. It holds the CDS 2.0 tokens, logos, fonts, gradients, the 46-slide master deck, and the brand rules (red only for the main CTA, violet only for AI and partner content, Zoho logo placement), and it builds decks as editable .pptx and visuals as exact-size PNGs.
---

# Zoho Creator · CDS 2.0

CDS 2.0 is Zoho Creator's design system for marketing. The source of truth is the CDS-2.0
Figma file; everything in this skill was exported from it. Use only what's here: never type a
colour, size, gradient or logo from memory.

People using this are usually marketers, not designers. Talk to them in plain language, ask
for missing facts instead of inventing them, and always tell them what they still need to
replace or confirm.

## Always

1. Read `references/brand-rules.md` before making anything. Those rules are the brand.
2. Pick the module for the request and read its reference:

   | Request | Read |
   | --- | --- |
   | Presentation, deck, slides, pitch, webinar talk | `references/deck.md` |
   | Social post, story, carousel, thumbnail, video background, email header, banner | `references/social.md` |
   | Landing page, web page, web section, zoho.com/creator | `references/web.md` |

3. Build with the files in this skill:
   - `design-system/tokens.css` — CSS variables for every colour, role, space, radius,
     elevation and the ten gradients, plus Zoho Puvi `@font-face` and text-style classes.
   - `design-system/tokens.json` — the same values for scripts.
   - `assets/logos/` — Creator lockup and Zoho logo, colour and white.
   - `assets/icons/icons.json` — the CDS icon set (318 icons, Regular and Fill) with tile spec and rules; get any icon with `python scripts/icon.py <name>` (`list` shows all names).
   - `assets/shapes/` — Shape kit v1.0 (set `color` to a token).
   - `assets/patterns/` — Connect tiles (light and bold) for the calm texture.
   - `assets/fonts/` — Zoho Puvi Regular, Medium, Semibold, Bold.
   - `assets/social/layouts.json` — the social, video and email templates; `scripts/render_social.py` renders them to PNG and checks them.
   - `assets/deck/` — the 46-slide master deck; `scripts/build_deck.py` and `check_deck.py` build and check decks.
4. Before handing anything over, run through `references/brand-check.md`, fix what fails, and
   give the marketer the "tell the marketer" list.

## What to deliver

- **Decks**: an editable .pptx built from the master deck, ready to import into Zoho Show.
- **Social, video, email**: PNG at the exact size from the CDS template (plus PDF for carousels).
- **Web**: one HTML file, labelled as a draft for design and dev review.

Social posts, stories, carousels, email headers and video backgrounds can be published by the
marketer once the check passes and every sample is replaced. YouTube thumbnails, web pages and
print go to a designer first.

## When the brief is thin

Ask once, briefly, for what decides the result: the format or channel, the one message,
the audience, and any real numbers, quotes, photos or screenshots. If they say "just make
it", go ahead with sample slots left in place and list them in the handover.
