# Creator Design System (CDS)

## Purpose

Ensure all UI follows CDS tokens, structure, and consistency across Creator
products.

All paths in this document are **relative to the repo root** (the directory
containing this file). No external URL fetching — the system is fully local.

---

## Execution Flow

1. Load rules from this file (`DESIGN.md`)
2. Load tokens from `foundations/` (see Token Sources below)
3. Load components from `components/` when building any UI element
4. Load accessibility rules from `accessibility/wcag.json`
5. If a product is specified → load `themes/{product}.json` (when added)
6. Apply token overrides from the theme (for backgrounds/layout only, never
   components)
7. Generate UI using canonical components from `components/*.json`

---

## Token Sources

Load tokens from:

* **Colours** → `foundations/colours.json`
* **Typography** → `foundations/typography.json`
* **Spacing** → `foundations/spaces.json`
* **Elevation** → `foundations/elevation.json`
* **Radius** → `foundations/radius.json`
* **Layout / Grid** → `foundations/grids.json`

The full manifest of all token files lives in `index.json`. Read it first
when you need an overview of what's available.

---

## Rules

* Use **ONLY** tokens (no hardcoded values)
* Do **NOT** use raw hex, px, or custom values
* Follow component structure strictly (see `components/*.json`)
* Maintain consistent spacing and hierarchy
* Prefer semantic tokens over primitive tokens
* If a required token is missing → **ASK**, do not substitute

---

## Theme Rules

If a product is specified:

* Load theme from `themes/{product}.json` (when product themes are added)
* Override **only** surface/background/layout tokens using theme values
* Component styles (buttons, inputs, cards) are **never** overridden by a
  theme — they come from `components/*.json` alone
* Maintain structural consistency with the base system

---

## Component Rules

* Use predefined components from `components/*.json` when available
* Follow component variants and states exactly
* Do **not** invent new component structures
* Do **not** modify component colours, sizes, variants, or states from a
  theme or product file
* Maintain consistency across UI

The current component library:

* `components/cta-buttons.json` — CTA button: 5 variants × 4 sizes × 3 states

---

## Layout Rules

* Follow the grid system from `foundations/grids.json`
* Use consistent spacing from `foundations/spaces.json`
* Maintain alignment and hierarchy
* Avoid arbitrary positioning

---

## Accessibility Rules

* Follow guidelines from `accessibility/wcag.json`
* Ensure proper contrast using tokens (≥ 4.5:1 for normal text,
  ≥ 3:1 for large text and UI components)
* Maintain a readable typography scale
* Use semantic HTML structure (`<button>`, `<nav>`, `<main>`, etc.)
* All interactive elements must have visible focus states
* Honour every check in `accessibility/wcag.json → checklists`

---

## Output Rules

* Generate clean, structured UI
* Avoid inline styles
* Use token-based values only (reference tokens by name, not by hex/px)
* Ensure consistency across all elements

---

## AI Behaviour

* Do not scan the entire system blindly — load only the files you need
* Prioritize semantic tokens over primitives
* Avoid duplication and unnecessary complexity
* When a path in this file is unclear, re-read this document before guessing