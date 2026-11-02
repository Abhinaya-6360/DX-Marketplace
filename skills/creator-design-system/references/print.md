# Print

Six CDS 2.0 print templates (Templates · Print in the CDS-2.0 Figma file) are in
`assets/print/layouts.json`. `scripts/render_print.py` turns a brief into a print PDF:

- colours in the **official CMYK values** from Foundations · Colour (tokens.json `cmyk`),
  never converted screen colours; greys in black ink only; K100 for small text
- real size, **3 mm bleed** on every edge, crop marks, trim and bleed boxes set
- Zoho Puvi embedded; patterns (Signature, Weave) drawn as vectors
- a working QR code on the roll-up when a link is given

| Template | Trim size | Text slots |
| --- | --- | --- |
| `business-card-front` | 85 × 55 mm | Name, Designation, Contact (two lines: email · phone, then web) |
| `business-card-back` | 85 × 55 mm | none (logo and Signature pattern) |
| `a4-flyer` | 210 × 297 mm | Eyebrow, Headline, Body, Benefits (up to 3), Call to action |
| `rollup-banner` | 850 × 2000 mm | Headline, QR link |
| `trifold` | A4 landscape, 2 sheets (outside, inside), folds at 100 / 200 mm | Outside: Eyebrow, Headline (cover), Why heading, Reasons (up to 4), Why body (inside flap), Contact heading, Contact, QR (back). Inside: Eyebrow, Heading, Body, Features 1–3 (number, title, text), Quote, Attribution, Call to action |
| `brochure-4pp` | A4, 4 pages (cover, inside-left, inside-right, back) | Cover: Eyebrow, Headline, Subline. Inside left: Eyebrow, Heading, Body, Quote, Attribution. Inside right: Features 1–3, Call to action. Back: Heading, Contact, QR, Legal (Zoho logo on the back only) |

For `trifold` and `brochure-4pp`, give text per page in the brief under `"pages"` (format at the
top of the script). The tri-fold's inside flap is 97 mm so it folds in cleanly; fold marks sit
outside the bleed. The 4-page brochure is delivered as four single A4 pages; the printer
imposes them on A3.

## Workflow

1. Get the facts: name, title, phone and email for cards; event, date, offer and link for
   flyers and roll-ups. Never invent them.
2. `python scripts/render_print.py slots <template>` to see the slots.
3. Write brief.json (format at the top of the script) and run
   `python scripts/render_print.py brief.json <name>.pdf --preview <name>.png`.
4. Fix every error (text too long, outside the 5 mm safe zone) by shortening the text.
5. View the preview, then hand over the PDF.

## Handover — always say this

Print is never sent straight to a vendor. A designer approves the PDF, confirms the vendor's
preset (PDF/X-4, Coated FOGRA39 or the vendor's profile, total ink under 300%), and orders
one printed proof before the full run (Guides · Print). The logo artwork colours are process
values; for large runs the designer may swap in the official print logo files. Print uses
Brand depth, Midnight or Soft gradients — never the mesh gradients, which band in print.
