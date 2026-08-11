# Creator Design System (CDS)

## Purpose

Ensure all UI follows CDS tokens, structure, and consistency across Creator
products.

All paths in this document are relative to `${CLAUDE_PLUGIN_ROOT}/design-system/`
— the design-system folder bundled with the `creator-design-skills` plugin,
**not** the user's current working directory. Since this folder ships
inside the plugin itself, it is available regardless of which project the
user has open. No external URL fetching — the system is fully local.

---

## Execution Flow

1. Load rules from this file (`${CLAUDE_PLUGIN_ROOT}/design-system/DESIGN.md`)
2. Load tokens from `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/` (see Token Sources below)
3. Load components from `${CLAUDE_PLUGIN_ROOT}/design-system/components/` when building any UI element
4. Load accessibility rules from `${CLAUDE_PLUGIN_ROOT}/design-system/accessibility/wcag.json`
5. Detect the product from the request. Check the request text for a
   product name matching any key under `tokens.themes` in
   `${CLAUDE_PLUGIN_ROOT}/design-system/index.json`
   (e.g. "Bookings", "Zoho Bookings", "bookings page/pricing/dashboard").
   If a match is found → load `${CLAUDE_PLUGIN_ROOT}/design-system/themes/{product}.json`.
   If no product is named or matched, skip this step — foundations apply
   as-is (Creator's shared `primary` is the default, since it lives in
   `foundations/colours.json`, not a theme file).
6. Apply token overrides from the theme (surface/background/layout tokens,
   or a product-specific primary colour family when the product's brand
   anchor differs from the shared foundation — see Theme Rules)
7. Generate UI using canonical components from `${CLAUDE_PLUGIN_ROOT}/design-system/components/*.json`

---

## Token Sources

Load tokens from:

* **Colours** → `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/colours.json`
* **Typography** → `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/typography.json`
* **Spacing** → `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/spaces.json`
* **Elevation** → `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/elevation.json`
* **Radius** → `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/radius.json`
* **Layout / Grid** → `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/grids.json`

The full manifest of all token files lives in
`${CLAUDE_PLUGIN_ROOT}/design-system/index.json`. Read it first when you
need an overview of what's available.

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
* Load theme from `${CLAUDE_PLUGIN_ROOT}/design-system/themes/{product}.json` once detected
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

* `${CLAUDE_PLUGIN_ROOT}/design-system/components/cta-buttons.json` — CTA button: 5 variants × 4 sizes × 3 states

---

## Layout Rules

* Follow the grid system from `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/grids.json`
* Use consistent spacing from `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/spaces.json`
* Maintain alignment and hierarchy
* Avoid arbitrary positioning

---

## Accessibility Rules

* Follow guidelines from `${CLAUDE_PLUGIN_ROOT}/design-system/accessibility/wcag.json`
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

## Missing-Folder Fallback

If, for some reason, `${CLAUDE_PLUGIN_ROOT}/design-system/` cannot be found
(this should not normally happen — the folder ships inside the plugin),
do not fall back to inlined values, training data, or invented tokens.
Tell the user the plugin install looks incomplete or corrupted and suggest
reinstalling it:

```
/plugin uninstall creator-design-skills
/plugin install creator-design-skills@DX-Marketplace
```

---

## AI Behaviour

* Do not scan the entire system blindly — load only the files you need
* Prioritize semantic tokens over primitives
* Avoid duplication and unnecessary complexity
* When a path in this file is unclear, re-read this document before guessing
