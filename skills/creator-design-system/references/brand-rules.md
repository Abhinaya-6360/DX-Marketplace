# CDS 2.0 brand rules

These rules come from the CDS-2.0 Figma file (Foundations, Brand and Guides pages).
They apply to everything: posts, thumbnails, decks, web drafts, print. Values live in
`design-system/tokens.json` and `design-system/tokens.css`; never type a colour, size
or gradient that isn't there.

## Colour

- **Brand blue is blue/100 (#0d4ef2).** Text is grey/160 (#25272c) on light, white on blue or navy.
- **Red is only for the main call to action** (role/action/cta, red/90): buttons that ask someone
  to sign up, register, buy or contact sales. Never red for emphasis, icons, borders, tags,
  badges, charts or decoration. Never use blue for a main action. The one other use is error
  messages in forms (role/status/error, red/100), which is never a button.
  - Social posts, thumbnails, email headers and slides: **one red button** at most.
  - Web pages: every sign-up, buy or contact-sales button is red, but **at most one red button
    per section** (nav, hero, CTA band each get one). Everything else interactive is blue.
- **Violet is only for AI and partner content.** Violet glows (mesh-soft-ai, mesh-partner) and
  violet highlight words (violet/100) appear only when the piece is about AI or about partners.
  Violet icons, shapes, patterns and tags stay AI-only.
- **On AI pieces violet is an accent, never the main colour.** Blue stays the primary colour.
  Violet only for highlight words on light backgrounds, the AI tag, the `ai-sparkle` icon and its
  tile, and soft glows. Never violet cards, panels, buttons or solid violet backgrounds.
  Partner content keeps its current treatment.
- **AI backgrounds:** Bold = `gradient/ai` (blue/100 → violet/100); Light = `mesh-soft-ai`.
  On `gradient/ai` all text is white; highlight words and big numbers are yellow/100, at headline
  size only; never violet text on the AI gradient; no pattern on it.
- **Yellow (yellow/100)** is for highlight boxes and tags on bold backgrounds.
- **Customer and partner logos keep their own colours.** Never recolour them.

## Contrast (WCAG AA, always)

- Normal text needs 4.5:1 against its background; large text (24 px and up, or 19 px Semibold
  and up) and icons, borders that carry meaning and button outlines need 3:1.
- Safe pairs (all pass AA for any text size):
  | Background | Text and icons |
  | --- | --- |
  | white, grey/10, blue/10 | grey/160 (body), grey/120 (secondary), blue/100 (links, highlight), blue/130, violet/100 (AI and partner) |
  | blue/20, violet/20 (tiles, soft panels) | grey/160, blue/100, blue/130, violet/100 — not grey/120 for small text |
  | yellow/100 (highlight box) | grey/160 or blue/130 — not white, not blue/100 for small text |
  | blue/100, brand-depth, midnight, glow, violet/100 | white; yellow/100 for large highlight words only |
  | blue/130, blue/160, grey/160, grey/180 | white, yellow/100, blue/40 |
- On light backgrounds (meshes, soft gradients) and on photos, check the lightest point behind
  the text. If a pair isn't in the table, check it with `scripts/check_system.py contrast`.
- Never fade text with opacity to make it secondary; use grey/120 instead.

## Gradients (backgrounds only, marketing only)

Pick by what the piece is, not by taste:

| Situation | Gradient | Pattern texture |
| --- | --- | --- |
| Light post, thumbnail, email header, banner | `mesh-soft-blue` | Connect, light tile, 12% |
| Light, and the topic is AI | `mesh-soft-ai` | none |
| Light, and the topic is a partner | `mesh-partner` | none |
| Bold, with a product screenshot | `glow`, centred behind the screenshot | none |
| Bold, without a product screenshot | `midnight` | Connect, bold tile, 8% |
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
  - Not on pieces with the Creator × Partner co-branded lockup.

## Partners (co-branded lockup)

From Brand · Logo, section 06 · Together with partners. Creator always leads.
- One line, centred: Creator lockup first, a thin 2 px divider (grey/140 on light backgrounds,
  white at 40% on dark), then the partner's logo.
- The partner logo is about 0.85× the Creator lockup's height (Creator about 1.2× taller);
  lead by position, not by size. Leave 0.3× the lockup height on each side of the divider.
- Use it on anything about a partner (topic partner): pass `partner_logo` and the renderer
  builds the lockup in place of the Creator lockup. Leave the Zoho logo off co-branded
  pieces, so there are never three logos.
- Never put the partner first, make it larger, recolour it, or lock it up without the divider.

## Type

- Zoho Puvi only (`assets/fonts/`). Use the text styles in tokens (h1–h6, display, text-*).
- Headings are Semibold: h1–h6/semibold and display (Semibold). Use Bold only when a heading
  needs extra weight, never as the default. Body Regular; labels and buttons Semibold.
  The one exception is email newsletters: Georgia for headings, Helvetica Neue for body
  (see `references/email.md`).
- Readable on a phone: on a 1080 px canvas, headlines 72 px or more, supporting text 32 px,
  names 28–32 px.
- **Layouts adapt to the content, in every collateral** (social, deck, print, web, email). When
  there is more or less text than the template's sample, the layout adjusts the way a designer
  would: first the blocks re-space and the box grows into free space (blocks below move down).
  With less text the blocks below close up, so a heading keeps its normal gap to its paragraph
  instead of an empty slot (beside a picture, short copy closes up and centres on the picture), then the text steps down **at most two sizes
  on the same type scale**, never under the smallest sizes below. Only when that still doesn't
  fit is the text shortened, and only after asking the person. Never change their words to make
  a layout work. The renderers do this and report each change as a `layout:` line; look at the
  result in place.
- Smallest sizes: 12 px on screen. In print, body 9 pt, captions and labels 8 pt, contact and
  legal lines 7 pt, never smaller.
- Highlight words: one or two words per headline, in a yellow/100 box (bold backgrounds),
  blue/100 text (light), violet/100 text (AI and partner, light backgrounds only), or
  yellow/100 text on the AI gradient.

## Languages other than English

Zoho Puvi has Latin letters only. For other languages:
- **Social, video, YouTube, decks and newsletters:** Tamil, Hindi and other Devanagari, Arabic,
  Japanese, Chinese and Korean text uses Noto Sans for those letters (bundled in
  `assets/fonts/noto/`, or Noto Sans CJK). Arabic is set right to left and right-aligned. Every
  such piece is listed as a font note for **design review** before it goes out.
- **Other scripts** (Bengali, Telugu, Kannada, Malayalam, Gujarati, Thai, Hebrew, Cyrillic…):
  no CDS font yet — flag it and ask the design team.
- **Print:** never typeset non-English print with the print tool (it can't join these letters
  correctly); it stops and the design team makes it.
- **Web pages:** localised zoho.com pages are made by the web team. Build web drafts in English.

## Shapes and patterns

- Shape kit v1.0: bracket (solid and frame), diamond, wedge (`assets/shapes/`, recolour with
  tokens). Never combine a pattern with a bold shape, or two patterns.
- Patterns: Weave, Chain and Signature (logo family); Spark and Connect (story family).
  Spark is AI-only, in any of the four colour versions (Blue, Ink, Light, Violet). Let patterns bleed off one or two edges; Connect may run full-bleed only
  as the faint texture above: 12% on light, 8% on Midnight and blue (web hero and CTA band too).
  It should be felt, not seen, and never compete with the message. No red in patterns.
- **Behind text, a pattern is always subtle**: the faint texture or the Calm version. Full-strength
  patterns only on panels with no text on them (deck title panel, flyer side panel).

## Icons

- Always take icons from the CDS 2.0 icon set in `assets/icons/icons.json` (Phosphor, plus CDS
  custom icons such as `ai-sparkle`, `no-code`, `visual-builder`, `api`, `form`, `mobile-app` and
  the `portal-*` set). Get one with `python scripts/icon.py <name>` (`list` shows all). Check the
  list and the close matches before deciding an icon is missing.
- Never use emoji, icon fonts, other icon sets, clip art or image-generated icons.
- Only if no CDS icon fits the meaning, draw a new one in the CDS custom style: `viewBox="0 0 32 32"`,
  2-unit line (`stroke-width="2"`), round ends and corners, about 3 units of empty space on each
  side, one colour (`currentColor`), no text or letters inside. Put `data-cds-new-icon="<name>"`
  on the `<svg>`. Use it like any CDS icon (sizes, tiles, colours below), and list it in the
  handover as a new icon for the design team to review and add to the CDS 2.0 library.
- **No emoji or symbol characters in copy** (🚀 ✅ ⭐ ✨ 👉 ✓ ★ ❤ …). Replace them with the CDS
  icon that means the same, in a tile, or remove them: ✅ → `check-circle`, 🚀 → `rocket-launch`,
  ⭐ → `star`, 💡 → `lightbulb`, 📈 → `trend-up`, 🔒 → `lock`, ⚡ → `lightning`, 🤖 → `ai-sparkle` (AI) or `robot` (a literal robot),
  ✨ → `sparkle` (AI: `ai-sparkle`), 📅 → `calendar-blank`, 📍 → `map-pin`, 👥 → `users`.
  Arrows (→), bullets, dashes, © and ™ are text, not emoji, and are fine.
- Regular by default; Fill only for the selected or active item.
- Sizes 16, 20, 24 or 32 px, matched to the text beside them.
- Icon tiles: 32, 40, 48 or 64 px, radius 4 px, icon at half the tile size. Blue tile
  (blue/20, icon blue/100); violet tile (violet/20, icon violet/100) for AI content only;
  on blue backgrounds a white tile with a blue/100 icon. Never red or green tiles, never red icons.
- Icons explain; they never decorate. No stretching, outlines or gradients on icons.
- **AI agent bot illustration** (`assets/illustrations/ai-agent-bot.svg`, Figma Illustration/AI agent bot):
  approved for AI agent pieces on dark backgrounds only (Midnight, navy, blue 100, the AI gradient), as
  the main picture of a hero, section, post or slide, one per piece. Never on white or light
  backgrounds, never as a small icon, never recoloured or redrawn.
- **AI icon is `ai-sparkle`** for anything AI, agents and bots included. Never the robot face for AI;
  `robot` is only for a literal robot.
- **Icons sit in a tile beside a heading or label**, never tacked on after a sentence or mid-text.

## 3D tile

- The CDS 3D tile (Brand · Shapes) is artwork for YouTube thumbnails, social posts and email
  newsletters — never web pages, decks or print. Blue by default; violet only for AI content. One white
  Regular icon per tile, from the CDS icon set.

## Imagery and content

- Never generate product photos or Creator UI screenshots. Use what the marketer supplies;
  otherwise leave the "Product screenshot (replace)" or "Photo (replace)" slot and say so.
- **Space around pictures:** keep at least 40 px (4% of the width) between any text and a screenshot,
  illustration, tile, photo or card. Text never touches or crowds a picture.
- **Illustrations** (`references/illustrations.md`): Claude draws flat CDS-style
  illustrations for whatever the content is about (`scripts/illustration.py`), blues and greys with
  other CDS colours as small accents (under 8%: yellow highlights, green success, red only for an
  error, violet only on AI); stock illustrations are
  fine when flat, licensed and recoloured to CDS. Never people drawn in code, logos, words or a
  real-looking Creator screen. Every new or stock illustration goes to design review.
- Never invent numbers, customers, quotes, prices or certifications. Leave the sample and
  flag it.
- Keep every stat's source line.
