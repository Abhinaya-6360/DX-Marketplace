# Web pages (zoho.com/creator)

> **Status (v2.0):** web output is a **reviewable HTML draft** for design and dev, never
> production code. Full section templates arrive in v2.2.

## Grid

Page width 1720 px · 12 columns · 88 px columns · 24 px gutters · 1320 px content, centred,
200 px side margins.

## Match the page to its topic first

| Page topic | Hero background | Hero visual panel | CTA band | Eyebrows and highlight words |
| --- | --- | --- | --- | --- |
| Default | soft-blue | blue/100 with the Connect pattern | blue/100 with the Connect pattern | blue/100 |
| AI | soft-violet | gradient/ai, no pattern | gradient/ai, no pattern | violet/100 |
| Partner | mesh-partner | white card on the mesh, no pattern | midnight with the calm Connect texture | violet/100 |

Use one eyebrow colour on the whole page. Feature-card icon tiles follow the same choice: blue
tiles by default, violet tiles on AI pages.

## Sections (Templates · Web in the CDS-2.0 Figma file)

Assemble pages from these, in this order when they're all used:

1. **Nav**: Creator lockup (colour) left; links (Features, Solutions, Pricing, Resources,
   Customers) in text-medium/medium grey/160; right: "Sign in" (secondary button, blue) and
   "Sign up free" (primary button, **red**). White, 1 px bottom border grey/40, sticky.
2. **Hero** (1720 × 720), background and panel from the topic table; left: tag, headline h2
   bold, body text-large, buttons ("Start free trial" red primary with arrow, "Book a demo"
   secondary); right: a 640 × 520 panel, radius/large, holding the product screenshot card.
3. **Feature grid**: centred section header (eyebrow, title, description), then 3 feature
   cards (white, 1 px grey/40 border, radius/large, 32 px padding, a 48 px icon tile with a
   24 px icon from `scripts/icon.py`).
4. **Stats**: blue/10 band, section header, 4 stat blocks. Values only from the marketer,
   with a source; otherwise "00%" placeholders.
5. **CTA band** (background from the topic table above): centred h3 headline in white, one line,
   "Start free trial" (red) and "Talk to sales" (inverse) buttons.

Section padding: 120 px top and bottom, 200 px sides; 64 px between header and content.

## Rules

- **CTAs are red, everything else is blue.** Ask: does this click move someone toward signing
  up, paying or contacting sales? Then red — **at most one red button per section** (nav,
  hero, CTA band). Links, nav hover, badges, ribbons, checkmarks and focus rings are blue/100.
- Use `tokens.css` variables, never raw hex or invented sizes.
- The Creator lockup is the SVG in `assets/logos/`, never a typed "Creator" wordmark.
- **Footer:** CDS 2.0 has no footer template yet. Use a simple footer on role/surface/dark
  (blue/160): white Creator lockup, link columns (Product, Resources, Company, Legal) in
  text-medium, and "© Zoho Corporation. All rights reserved." Flag it as provisional in the
  handover.
- Live zoho.com pages may still use pre-CDS 2.0 colours. Drafts follow CDS 2.0; that
  difference is expected.
