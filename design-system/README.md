# Creator Design System (CDS) — Tokens

Machine-readable token files extracted from the [CDS Figma source](https://www.figma.com/design/HwJgDmaNzfJYTeoMwe31yU/CDS).
This folder is the **single source of truth** for every design value used across Creator products.

## Folder layout

\`\`\`
design-system/
├── index.json                  ← manifest; entry point for tooling
├── foundations/                ← atomic tokens (spacing, colour, type, etc.)
│   ├── spaces.json
│   ├── grids.json
│   ├── colours.json
│   ├── typography.json
│   ├── elevation.json
│   └── radius.json
├── components/                 ← composed component specs
│   └── cta-buttons.json
└── accessibility/              ← compliance overlay
    └── wcag.json
\`\`\`

## File anatomy

Every token file follows the same shape so consumers can rely on a predictable contract:

| Key | Purpose |
|---|---|
| `name`, `description`, `source` | Identity + Figma traceability |
| `meta` | Counts, ranges, summary stats |
| `tiers` / `families` / `breakpoints` / `variants` | Nested, semantic structure |
| `flat` | Flat key→value map ready for CSS variables or Tailwind config |
| `css` | Drop-in CSS property bundles where applicable |
| `usage` | DO/DON'T rules from the design source |

## How to consume

### 1. As CSS variables
\`\`\`js
import colours from './design-system/foundations/colours.json';
Object.entries(colours.flat).forEach(([key, value]) => {
  document.documentElement.style.setProperty(`--${key}`, value);
});
\`\`\`

### 2. As Tailwind config
\`\`\`js
const radius = require('./design-system/foundations/radius.json');
module.exports = {
  theme: { extend: { borderRadius: radius.tailwind.borderRadius } }
};
\`\`\`

### 3. As Style Dictionary input
Each `flat` block is compatible with [Style Dictionary](https://amzn.github.io/style-dictionary/) for cross-platform output (iOS, Android, web).

## How to update

1. **Source of truth is Figma.** Don't edit JSON values by hand without a corresponding Figma update.
2. When a Figma token changes, regenerate the affected JSON and re-run the WCAG audit (`accessibility/wcag.json`) for any colour, type, or component change.
3. Bump `version` in `index.json` for breaking changes (renames, removals); bump `edition` for additive changes.

## Pairing with the CDS skill

The `skills/cds-design-system/` skill should treat these JSON files as authoritative.
When the skill generates UI code or design rationale, it must pull values from these files
rather than inferring from training data — this keeps Claude's output in sync with the live design system.

## Known issues

See `accessibility/wcag.json → summary.criticalFailures` for the current list of WCAG failures
that need design-team resolution before the system can pass an AA audit.