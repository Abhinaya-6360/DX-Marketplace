# Creator — Product Rules

## Theme

Auto-load `design-system/themes/creator.json` (when published) for surface
and background tokens.

## Surface Rules

* Use Creator-mapped theme tokens for page backgrounds and section surfaces.
* Do **not** use generic `grey-*` or `darkGrey-*` foundation tokens directly
  — only the Creator-mapped theme tokens (once the theme file is added).

## Component Rules

Components remain on the base CDS system:

* CTA buttons → `design-system/components/cta-buttons.json`
* Inputs, cards, forms → base CDS components

The Creator theme **never** overrides component colours, sizes, variants,
or states.

## Layout Rules

Follow the base grid system from `design-system/foundations/grids.json`. No
Creator-specific layout overrides at this time.

## Typography

Use the base `design-system/foundations/typography.json` scale unchanged.

* Font family: `'Zoho Puvi', Inter, system-ui, sans-serif`
* Display + H1–H6 + Text (Large / Medium / Regular / Small)
* Four weights: Regular (400), Medium (500), Semibold (600), Bold (700)

## Brand Anchors

Creator surfaces should lean on the brand anchor colours at the 500 level:

* Primary: Bright Royal Blue `#0047FF` (Pantone Reflex Blue C)
* Secondary: Vivid Red `#FF0405` (Pantone Red 032 C)
* Tertiary: Vibrant Violet `#5E05FF` (Pantone Violet C)

These anchors are immutable — never substitute with a tint or shade unless
explicitly mapped in the theme.

## Accessibility

All Creator surfaces must pass the contrast checks in
`design-system/accessibility/wcag.json`. Pay special attention to:

* White text on Secondary 500 (`#FF0405`) — fails AA at 3.94:1. Use
  Secondary 600 (`#D10000`) for white-text combinations.
* Grey 400 (`#919191`) on white — fails AA for body text. Reserve for
  borders and placeholders only.
* Grey 200 (`#D1D1D1`) for any interactive border — fails non-text contrast.
  Use Grey 500 or darker for form field borders.

## Notes

This file defines product-specific rules for the Creator product. As Creator
introduces its own theme tokens or component variations, document them here.