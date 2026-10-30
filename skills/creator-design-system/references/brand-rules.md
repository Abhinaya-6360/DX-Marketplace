# CDS 2.0 brand rules

These rules come from the CDS-2.0 Figma file (Foundations, Brand and Guides pages).
They apply to everything: posts, thumbnails, decks, web drafts, print. Values live in
`design-system/tokens.json` and `design-system/tokens.css`; never type a colour, size
or gradient that isn't there.

## Colour

- **Brand blue is blue/100 (#0d4ef2).** Text is grey/160 (#25272c) on light, white on blue or navy.
- **Red is only for the main call to action** (role/action/cta, red/90): buttons that ask someone
  to sign up, register, buy or contact sales. Never red for emphasis, icons, borders, tags,
  badges, charts or decoration. Never use blue for a main action.
  - Social posts, thumbnails, email headers and slides: **one red button** at most.
  - Web pages: every sign-up, buy or contact-sales button is red, but **at most one red button
    per section** (nav, hero, CTA band each get one). Everything else interactive is blue.
- **Violet is only for AI and partner content.** Violet glows (mesh-soft-ai, mesh-partner) and
  violet highlight words (violet/100) appear only when the piece is about AI or about partners.
  Violet icons, shapes, patterns and tags stay AI-only.
- **Yellow (yellow/100)** is for highlight boxes and tags on bold backgrounds.
- **Customer and partner logos keep their own colours.** Never recolour them.

## Gradients (backgrounds only, marketing only)

Pick by what the piece is, not by taste:

| Situation | Gradient | Pattern texture |
| --- | --- | --- |
| Light post, thumbnail, email header, banner | `mesh-soft-blue` | Connect, light tile, 22% |
| Light, and the topic is AI | `mesh-soft-ai` | none |
| Light, and the topic is a partner | `mesh-partner` | none |
| Bold, with a product screenshot | `glow`, centred behind the screenshot | none |
| Bold, without a product screenshot | `midnight` | Connect, bold tile, 12% |
| Calm web section or text-heavy slide | `soft-blue` (or `soft-violet` for AI, `soft-yellow` for offers) | none |
| Print | Soft · blue, Soft · violet or Midnight (meshes band in print) | as above |

- Keep copy inside the white glow (top-left) on soft meshes.
- Never put a gradient on the logo, shapes or text. No gradients in product UI.
- A gradient uses at most two colours; a mesh may layer two such gradients. Never red in a gradient.
- **No pattern or texture behind faces, speaker cards or photos of people.**
- No pattern on the AI or Glow gradients.

## Logos

- **Creator lockup** top-left inside the safe area. Colour version on white or light; white
  version on blue, navy or photos (`assets/logos/`). Never stretch, recolour or rebuild it.
- **Zoho logo** about half the Creator lockup's width, always smaller than it.
  - Default: bottom corner inside the safe area (bottom-left on YouTube thumbnails, so it
    clears the video-length badge).
  - When the bottom is busy: top-right, vertically centred on the Creator lockup's line,
    set on the right safe edge. Never above that line.
  - Full colour on white; all-white on blue, navy or photos.
  - Decks: closing slide only. Never lock it up with Creator in a new arrangement.

## Type

- Zoho Puvi only (`assets/fonts/`). Use the text styles in tokens (h1–h6, display, text-*).
- Readable on a phone: on a 1080 px canvas, headlines 72 px or more, supporting text 32 px,
  names 28–32 px. Never shrink text to make it fit; shorten it.
- Highlight words: one or two words per headline, in a yellow/100 box (bold backgrounds),
  blue/100 text (light), or violet/100 text (AI and partner only).

## Shapes and patterns

- Shape kit v1.0: bracket (solid and frame), diamond, wedge (`assets/shapes/`, recolour with
  tokens). Never combine a pattern with a bold shape, or two patterns.
- Patterns: Weave, Chain and Signature (logo family); Spark and Connect (story family).
  Spark is AI-only. Let patterns bleed off one or two edges; Connect may run full-bleed only
  as the calm texture above. No red in patterns.

## Icons

- Only the CDS icon set in `assets/icons/icons.json` (Phosphor, plus CDS custom icons such as
  `ai-sparkle`, `no-code`, `visual-builder` and the `portal-*` set). Never draw, import or
  mix in other icons or emoji. Get one with `python scripts/icon.py <name>` (`list` shows all).
- Regular by default; Fill only for the selected or active item.
- Sizes 16, 20, 24 or 32 px, matched to the text beside them.
- Icon tiles: 32, 40, 48 or 64 px, radius 4 px, icon at half the tile size. Blue tile
  (blue/20, icon blue/100); violet tile (violet/20, icon violet/100) for AI content only;
  on blue backgrounds a white tile with a blue/100 icon. Never red or green tiles, never red icons.
- Icons explain; they never decorate. No stretching, outlines or gradients on icons.

## Imagery and content

- Never generate product photos or Creator UI screenshots. Use what the marketer supplies;
  otherwise leave the "Product screenshot (replace)" or "Photo (replace)" slot and say so.
- Never invent numbers, customers, quotes, prices or certifications. Leave the sample and
  flag it.
- Keep every stat's source line.
