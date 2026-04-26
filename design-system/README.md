# Creator Design System (CDS)

Centralized design tokens, components, themes, and accessibility rules for
all Creator products. Everything ships as JSON so it can be consumed by any
language or tool.

Extracted from the CDS Figma design system.

---

## Repo Structure

```
design-system/
├── DESIGN.md                            # Loader rules and AI behaviour
├── README.md                            # This file
├── LICENSE
├── index.json                           # Manifest of every token file
├── foundations/
│   ├── colours.json                     # Full colour palette (10 families × up to 12 shades)
│   ├── typography.json                  # Zoho Puvi scale: Display + H1–H6 + Text
│   ├── spaces.json                      # Spacing tokens (Sm/Md/Lg/Xl)
│   ├── elevation.json                   # Drop-shadow tiers (XS → XL)
│   ├── radius.json                      # Corner-radius tokens (XS → Full)
│   └── grids.json                       # Responsive grid breakpoints
├── components/
│   └── cta-buttons.json                 # CTA button: 5 variants × 4 sizes × 3 states
└── accessibility/
    └── wcag.json                        # WCAG 2.2 AA rules + 47-check audit
```

---

## Usage

All files are JSON and can be loaded directly.

```js
// Node / any JS runtime
const colours = require('./foundations/colours.json');
const primaryBlue = colours.families.primary.scale['500'].hex; // "#0047FF"

const cta = require('./components/cta-buttons.json');
const primaryDefault = cta.variants.primary.states.default;
// { background, backgroundToken, text, textToken, border }
```

```python
# Python
import json
with open('foundations/colours.json') as f:
    colours = json.load(f)
primary_blue = colours['families']['primary']['scale']['500']['hex']  # "#0047FF"
```

Consuming projects typically generate CSS custom properties, Tailwind configs,
or Figma token exports from these JSON files at build time. Each foundation
file ships a `flat` block ready for that purpose.

---

## Figma Source

* **Design File**: [CDS](https://www.figma.com/design/HwJgDmaNzfJYTeoMwe31yU/CDS)
* **File Key**: `HwJgDmaNzfJYTeoMwe31yU`

Each JSON file includes a `source` object with the Figma node ID it was
extracted from.

---

## Colour Palette — `foundations/colours.json`

10 colour families with full scales (0 → 950). Six families are Pantone-matched
at the 500 level.

| Family | Role |
| --- | --- |
| `primary` | Primary actions, links, brand marks (`primary-500` = `#0047FF`) |
| `secondary` | Destructive actions, error states (`secondary-500` = `#FF0405`) |
| `tertiary` | AI features, premium states (`tertiary-500` = `#5E05FF`) |
| `quaternary` | Highlights, warning states (`quaternary-500` = `#FED70B`) |
| `quinary` | Data viz, callouts (`quinary-500` = `#E6FF0A`) |
| `senary` | Success states, growth metrics (`senary-500` = `#03FF17`) |
| `grey` | Neutral text hierarchy, borders, dividers |
| `darkGrey` | Dark-mode surfaces, code blocks |
| `blackAndWhite` | Pure backgrounds, high-contrast type |
| `buttonColorRed` | Reserved scale for destructive button states |

### Shade Scale

* **0–100** — Light tints, backgrounds
* **200–400** — Lighter accents
* **500** — Base colour (most commonly used)
* **600–700** — Darker accents
* **800–950** — Dark shades, text on light backgrounds

All values are uppercase hex (e.g., `#0047FF`). RGB triplets are also stored
for colour math and gradients.

---

## Typography — `foundations/typography.json`

* **Font Family**: `'Zoho Puvi', Inter, system-ui, sans-serif`
* **Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Display & Headings

| Tier | Size | Line Height |
| --- | --- | --- |
| Display Bold | 80px | 88px |
| Small Display | 64px | 72px |
| H1 | 80px | 96px |
| H2 | 60px | 68px |
| H3 | 52px | 60px |
| H4 | 44px | 52px |
| H5 | 36px | 44px |
| H6 | 28px | 36px |

### Text

| Tier | Size | Line Height |
| --- | --- | --- |
| Large | 20px | 28px |
| Medium | 16px | 24px |
| Regular | 14px | 22px |
| Small | 12px | 18px |

Each tier exposes all four weight variants. Letter-spacing is stored as both
a percentage and a resolved em value.

---

## Grid — `foundations/grids.json`

Centred grids across all breakpoints.

| Breakpoint | Min Width | Max Width | Columns | Column Width | Gutter |
| --- | --- | --- | --- | --- | --- |
| Desktop XL (XL) | 1720px | — | 12 | 88px | 24px |
| Desktop L (LG) | 1400px | 1720px | 12 | 88px | 24px |
| Desktop (ML) | 1200px | 1400px | 12 | 56px | 32px |
| Laptop (MD) | 992px | 1200px | 12 | 48px | 16px |
| Tablet L (SM) | 768px | 992px | 12 | 48px | 16px |
| Tablet (XS) | 768px | — | 8 | 64px | 16px |
| Mobile (XXS) | 576px | — | 4 | 104px | 16px |

Ready-to-use `@media` queries are included in the `mediaQueries` block of
`foundations/grids.json`.

---

## Spacing — `foundations/spaces.json`

A 4-pixel base scale across 33 tokens, grouped into four categories:

| Category | Range | Count |
| --- | --- | --- |
| Small (`sm-1` … `sm-5`) | 4px → 20px — micro / inline | 5 |
| Medium (`md-1` … `md-8`) | 24px → 80px — component padding & gaps | 8 |
| Large (`lg-1` … `lg-10`) | 88px → 160px — section spacing | 10 |
| X-Large (`xl-1` … `xl-10`) | 168px → 240px — page-level / hero | 10 |

The entire scale is 4px-aligned. Off-scale values (e.g. 18px, 22px) are not
permitted.

---

## Elevation — `foundations/elevation.json`

Five drop-shadow tiers for depth and surface temporality:

| Tier | Use For |
| --- | --- |
| XS | Resting cards · row elevation |
| S (Small) | Hover state · raised panels |
| M (Medium) | Dropdowns · popovers |
| L (Large) | Side sheets · drawer overlays |
| XL (X-large) | Dialogs · modals · focused surfaces |

Each tier ships raw `shadow` CSS, individual `properties` (offsetX/Y, blur,
spread, colour, opacity), and a ready-to-use `css` string.

---

## Radius — `foundations/radius.json`

Five corner-radius tokens:

| Tier | Value | Use For |
| --- | --- | --- |
| XS | 2px | Input fields · dense tables |
| S (Small) | 8px | Cards · buttons · badges (default) |
| M (Medium) | 16px | Feature cards · modals |
| L (Large) | 24px | Hero banners · highlight cards |
| Full | 999px | Avatars · pills · chips · toggles |

---

## CTA Component — `components/cta-buttons.json`

### Variants

| Variant | Default Background | Default Text |
| --- | --- | --- |
| `primary` | `#E42527` | `#FFFFFF` |
| `primaryLine` | transparent (outlined) | `#0047FF` |
| `secondary` | `#000000` | `#FFFFFF` |
| `secondaryLine` | transparent (outlined) | `#000000` |
| `tertiary` | `#FFFFFF` | `#000000` |

### Sizes

| Size | Padding | Font | Height |
| --- | --- | --- | --- |
| `xs` | 12px 16px | 16px | 32px |
| `sm` | 16px 24px | 16px | 40px |
| `md` | 20px 24px | 20px | 48px |
| `lg` | 24px 32px | 24px | 56px |

### States

Each variant exposes `default`, `hover`, and `active` states.

### Other

* Border radius: `4px` (all variants/sizes)
* Font weight: 600 (Semibold)
* Icon: 24px, optional, defaults to ArrowRight

---

## Themes — `themes/{product}.json`

*(Reserved for future use.)*

Product themes will override only **surface, background, and layout tokens** —
never component styles. The schema will match the base colour schema so it
can be substituted cleanly:

```json
{
  "meta": { "name": "shift", "type": "theme" },
  "colors": {
    "primary": { "50": "...", "100": "...", "...": "...", "950": "..." },
    "gray":    { "...": "..." }
  }
}
```

---

## Accessibility — `accessibility/wcag.json`

A single machine-readable file containing:

* **Rules** — every WCAG 2.2 AA rule that applies to the system (contrast,
  focus visibility, target size, text spacing, reflow, name/role/value, etc.)
* **Checklists** — 47 page-by-page audit checks tied to actual token values
  across spaces, grids, colours, typography, elevation, radius, and CTA
  components.
* **Summary** — counts by status (pass / fail / review) and a list of critical
  failures that need design-team resolution.
* **Tooling** — recommended design, code, and manual a11y tools.
* **Process** — design / development / QA accessibility process steps.

Re-run the audit against this file whenever any token changes.

---

## Notes

* All colours are stored in uppercase hex (e.g., `#0047FF`)
* CTA buttons use Zoho Puvi Semibold (600)
* Letter spacing is stored as both a percentage (source) and a resolved em
  value (derived)
* Each token file ships a `flat` block ready for CSS-variable / Tailwind /
  Style Dictionary generation

---

## License

MIT — see [LICENSE](./LICENSE).