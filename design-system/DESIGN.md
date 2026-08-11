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
5. Detect the product from the request. Check the request text for a
   product name matching any key under `tokens.themes` in `index.json`
   (e.g. "Bookings", "Zoho Bookings", "bookings page/pricing/dashboard").
   If a match is found → load `themes/{product}.json`. If no product is
   named or matched, skip this step — foundations apply as-is (Creator's
   shared `primary` is the default, since it lives in
   `foundations/colours.json`, not a theme file).
6. Apply token overrides from the theme (surface/background/layout tokens,
   or a product-specific primary colour family when the product's brand
   anchor differs from the shared foundation — see Theme Rules)
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

* Detect product from the request per Execution Flow step 5 — do not wait
  for a formal parameter; a plain-language product name is sufficient
* Load theme from `themes/{product}.json` once detected
* Override **only** surface/background/layout tokens using theme values,
  unless the theme defines its own `primary` colour family (e.g. Bookings)
  — in that case, use the theme's primary family in place of
  `foundations/colours.json → primary` for that product only
* Component styles (buttons, inputs, cards) are **never** overridden by a
  theme — they come from `components/*.json` alone
* Maintain structural consistency with the base system
* If a product is named but no matching entry exists in `index.json →
  tokens.themes` → **ASK** which theme to use rather than defaulting silently

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