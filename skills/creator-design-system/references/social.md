# Social, video and email

> **Status (v2.0):** HTML templates for every format arrive in v2.1. Until then, build from
> the specs below with `design-system/tokens.css` and the files in `assets/`, and label the
> result **Draft — designer review** in the handover.

## Formats

| Template | Size (px) | Versions | Safe area (px) |
| --- | --- | --- | --- |
| Social post · Feature | 1080 × 1080 | Product shot / Statement × Light / Bold | 64 all sides |
| Social post · Quote | 1080 × 1080 | Light / Bold | 64 all sides |
| Social post · Webinar | 1080 × 1350 | Light / Bold | 64 all sides |
| Social post · Landscape (LinkedIn, Facebook) | 1200 × 628 | Light / Bold | 48 all sides |
| Social post · X | 1600 × 900 | Light / Bold | 48 all sides |
| Story | 1080 × 1920 | Light / Bold | 250 top, 340 bottom, 65 sides |
| Reels and Shorts cover | 1080 × 1920 | Bold | 250 top, 450 bottom, 65 left, 140 right |
| Carousel · Cover / Slide | 1080 × 1350 | Cover Bold; Slide Light / Bold | 64 all sides |
| YouTube thumbnail | 1280 × 720 | Campaign · AI / Deep dive / Explainer / Customer story · Partner / Learning series · AI | 48 sides; keep the bottom-right video-length corner clear |
| Video background · Calm | 1920 × 1080 | Bold | 54 top, 96 sides, 240 bottom (lower third) |
| Email header | 1200 × 400 | Light / Bold | 48 sides, 40 top and bottom |

**Light** uses the light gradient for the topic (see `brand-rules.md`); **Bold** uses Glow
behind a product screenshot, otherwise Midnight.

## Layout, in reading order

Content margin 80 px on 1080-wide canvases (inside the 64 px safe area); scale margins with
the canvas.

1. Creator lockup top-left (220 px wide on 1080 canvases). Zoho logo half that width, bottom
   corner, or top-right on the lockup's line when the bottom is busy.
2. Tag (CDS tag: blue on Light, yellow on Bold) — optional.
3. Headline: h1 or h2 bold (80/72 px), one or two highlight words at most.
4. Supporting line: h6 regular, 32 px, grey/120 on Light, blue/20 on Bold.
5. Visual: product screenshot in a framed card (radius/large 24 px, 1 px border grey/40,
   elevation/large), or cut-out speaker photos on the diamond shape with name and role.
6. CTA button (red) only when the post asks for an action (register, sign up).

Webinar: logos row, LIVE WEBINAR tag, headline, date and time (32 px), speakers (no card
boxes, no pattern behind them), Register button on the bottom safe edge.

Quote: quote in h2, name and role below, cut-out speaker on the diamond, no pattern.

## Export

Build each piece as one HTML file at the exact size, using `tokens.css` (it loads Zoho Puvi
from `assets/fonts/`). Render to PNG with Playwright (Chromium) at device scale 1 and the
exact viewport, then view the PNG before handing it over. Deliver PNG (and a PDF for
carousels: one page per slide).
