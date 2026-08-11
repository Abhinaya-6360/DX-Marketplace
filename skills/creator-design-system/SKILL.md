---
name: creator-design-system
description: Apply Creator Design System (CDS) tokens, components, and themes when building any UI, landing page, dashboard, or component. Enforces strict token usage from the local CDS design system — never invents colours, sizes, radii, or typography. Use whenever the request involves Creator UI, CDS, a design system, building a component, a landing page, a dashboard, or any web page design.
triggers:
  - creator ui
  - cds
  - design system
  - build ui
  - create component
  - landing page
  - dashboard ui
  - web page design
---

# Creator Design System Skill

## Purpose

Ensure every UI strictly follows CDS tokens, components, and themes from the
design-system folder bundled with this plugin. No invented tokens, no
external fetches, no component overrides.

---

## Data Access Rule (BLOCKING)

* **Never** fetch tokens, components, or themes from external URLs (GitHub
  links, CDNs, the web).
* **Always** read from the design-system folder bundled with this plugin,
  at:
  + `${CLAUDE_PLUGIN_ROOT}/design-system/DESIGN.md`
  + `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/*.json`
  + `${CLAUDE_PLUGIN_ROOT}/design-system/components/*.json`
  + `${CLAUDE_PLUGIN_ROOT}/design-system/accessibility/*.json`
  + `${CLAUDE_PLUGIN_ROOT}/design-system/themes/*.json`
* Product-specific rules live **inside this skill**, in `./products/`
  (relative to this SKILL.md's own folder).

If `${CLAUDE_PLUGIN_ROOT}/design-system/` is not present, **STOP**:

* Do not generate any UI output.
* Do not fall back to values inlined in any other skill.
* Do not use values from training data, web fetches, or memory.
* Do not invent token names, hex values, sizes, or radii.

This should not normally happen — the design-system folder ships inside the
`creator-design-skills` plugin, so it is available no matter which project
the user has open. If it's genuinely missing, tell the user the plugin
install looks incomplete or corrupted and suggest reinstalling it:

```
/plugin uninstall creator-design-skills
/plugin install creator-design-skills@DX-Marketplace
```

This rule is BLOCKING. The design system is the single source of truth — without
it, no output is valid.

---

## Token Priority

When resolving any style value, walk this order top-down:

1. **Component tokens** — from `${CLAUDE_PLUGIN_ROOT}/design-system/components/*.json`
2. **Foundation tokens** — from `${CLAUDE_PLUGIN_ROOT}/design-system/DESIGN.md` and
   `${CLAUDE_PLUGIN_ROOT}/design-system/foundations/*.json`
3. **Product tokens** — from `${CLAUDE_PLUGIN_ROOT}/design-system/themes/{product}.json`

A lower-priority layer never overrides a higher one.

---

## Token Validation Rule

Before using any token:

* Verify it exists in the current product scope or in the foundation system.
* Never invent token names, hex values, or spacing numbers.
* If a required token is missing → **ASK the user**, do not substitute.

---

## Component Authority Rule

All UI components (Button, CTA, Input, etc.) must strictly follow definitions
from `${CLAUDE_PLUGIN_ROOT}/design-system/components/*.json`.

* Do **not** override component colours, sizes, variants, or states.
* Product files (e.g. `products/shift.md`, `products/crm.md`) must **not**
  modify component styles.
* Components are isolated from product themes.

### Component Isolation Example

* CTA → uses `${CLAUDE_PLUGIN_ROOT}/design-system/components/cta-buttons.json` only
  (Primary red `#E42527`, Primary Line blue `#0047FF`).
* Background → may use a Shift product theme (e.g. Shift darkGrey).
* Product tokens apply only to: **backgrounds, layout, sections** — never to
  components.

---

## Token Scope Rule (Product Context)

When a product context is active (e.g. Shift):

* Use **only** tokens defined in that product's scope.
* Do **not** use generic foundation tokens like `grey-900` or `primary-500`
  unless they are explicitly mapped into the product theme.

Correct for Shift: `darkGrey-*`, `shift-primary`
Avoid for Shift: `grey-900`, `primary-500` (unless mapped)

If a required product token is missing → ASK instead of substituting.

---

## Product Activation Rule

When a product is specified (e.g. Shift):

* Auto-load `${CLAUDE_PLUGIN_ROOT}/design-system/themes/{product}.json` for theme tokens
  (Creator and Bookings themes already ship with this plugin).
* Auto-load `./products/{product}.md` for product-specific rules and context.
* Apply product tokens to:
  + page background
  + sections
  + layout surfaces
* Do **not** apply product tokens to:
  + components (CTA, inputs, buttons)

---

## Product Overrides

If the request names a specific product:

1. Look inside `./products/` (relative to this skill).
2. Match the product name (e.g. `shift`, `crm`, `books`).
3. Apply product-specific rules and tokens on top of the base system.

Product rules override the base design system **only where explicitly
permitted** (backgrounds, layout, sections — never components).

---

## Accessibility Authority

All output must respect `${CLAUDE_PLUGIN_ROOT}/design-system/accessibility/wcag.json`:

* Verify text/background pairs against the contrast checklist before output.
* Honour the focus-visible rule (2px solid outline, 2px offset minimum).
* Honour target-size minimums (24×24 CSS px, 44×44 for touch surfaces).
* If a generated UI would fail any check in the WCAG checklist, fix the
  issue at the token level — do not ship the failing output.

---

## Prioritize

1. Semantic tokens
2. Component rules
3. Typography and spacing
4. Accessibility verification

---

## Auto-Activation Hint

This skill should activate automatically whenever a request involves UI,
layout, components, design systems, styling, or frontend generation in a
Creator or CDS context.
