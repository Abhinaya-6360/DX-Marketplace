---
name: creator-visual-language
description: The visual language for Zoho Creator marketing pages — Creator header/footer chrome, font stack, and the strict CTA-vs-brand colour rule built on top of the Creator Design System (CDS). Use this skill any time you're styling a Zoho Creator page or component (pricing, resources, customers, communities, about, features, or any sibling of https://www.zoho.com/en-in/creator/) so the result matches Creator's branded chrome and CDS tokens. Trigger on phrases like "Creator-branded", "Zoho Creator page styling", "match the Creator homepage", "use Creator design tokens", "apply Creator chrome", "Creator header/footer". Defers to the creator-design-system skill for all colour, type, spacing, elevation, and component values.
---

# Creator Visual Language

The shared visual language for Zoho Creator marketing pages. This skill owns
three things, and three things only:

1. The **CTA-vs-brand colour discipline rule** (which token role goes on which UI element).
2. The **header and footer markup** that wraps every Creator page.
3. The **font stack and typography role mapping** for Creator surfaces.

Everything else — colour values, spacing, elevation, components, accessibility —
comes from the canonical token files under `design-system/`. This skill
**never** holds copies of token values. It only describes the mapping.

---

## Data Access Rule (BLOCKING)

This skill **cannot generate output** without access to the canonical token
files. Specifically, it requires:

* `design-system/foundations/colours.json` — for every hex value
* `design-system/foundations/typography.json` — for font sizes and line heights
* `design-system/foundations/spaces.json` — for padding and gaps
* `design-system/components/cta-buttons.json` — for the CTA spec

If `design-system/` is not at the repo root, **STOP**. Do not proceed with
inlined values, memory, or web-fetched copies. Ask the user to point Claude
at the right project (e.g. `cd ~/path/to/repo-with-design-system` and re-run).

This is not negotiable. Generating chrome from invented or remembered hex
values silently breaks the token-discipline guarantee that the entire
architecture is built on.

---

## When to use

Any time you're producing HTML/CSS for a Zoho Creator marketing page, AND
the design-system folder is accessible. This skill tells you:

* Which CDS colours to use, and where to use each one.
* The exact header and footer markup that wraps every Creator page.
* The font stack, semantic token naming, and brand discipline rules.

It does **not** prescribe page layouts, components, grids, breakpoints, or
animations — those are separate concerns owned by `creator-design-system`.

---

## The single most important rule

**CTAs are red. Everything else is blue.**

* **`--color-cta`** — only for primary action buttons. "Get Started",
  "Start Free Trial", "Contact Sales", "Subscribe", "Talk to Sales" — buttons
  that drive a conversion.
  - Default state: `colours.json → families.buttonColorRed.scale.300`
  - Hover state:   `colours.json → families.buttonColorRed.scale.400`
  - Active state:  `colours.json → families.buttonColorRed.scale.500`

* **`--color-brand`** — the brand colour for everything else interactive
  or branded. Links, the "Creator" wordmark, nav hover, FAQ chevrons, plan
  ribbons, badges, decorative checkmarks, featured plan borders, hero
  gradient tints, card hover shadow tints, focus rings.
  - Default state: `colours.json → families.primary.scale.500`
  - Hover state:   `colours.json → families.primary.scale.600`
  - Active state:  `colours.json → families.primary.scale.700`
  - Soft surface:  `colours.json → families.primary.scale.0`
  - Soft alt:      `colours.json → families.primary.scale.50`

**Decision rule when unsure:** *Does clicking this take the user toward
signing up, paying, or contacting sales?* → red CTA. Otherwise → blue.

Never inline red into non-CTA elements. Never use blue on a primary action
button.

---

## Workflow

### Step 1 — Verify design-system is accessible

Confirm `design-system/` exists at the repo root before proceeding. If not,
stop and ask the user. Do not fall back to inlined values.

### Step 2 — Load colours and map to semantic tokens

Read `design-system/foundations/colours.json` and use the `flat` block to
generate CSS custom properties. Then map them to the semantic tokens below:

```
--color-cta:           color-button-red-300
--color-cta-hover:     color-button-red-400
--color-cta-active:    color-button-red-500

--color-brand:         color-primary-500
--color-brand-hover:   color-primary-600
--color-brand-active:  color-primary-700
--color-brand-soft:    color-primary-0
--color-brand-soft-2:  color-primary-50

--color-text-primary:    color-black
--color-text-body:       color-grey-500
--color-text-secondary:  color-grey-400  (placeholders/dividers only — fails AA for body)

--color-surface-page:    color-white
--color-surface-subtle:  color-grey-0
--color-surface-darkest: color-black

--color-border-default:  color-grey-100
--color-border-strong:   color-grey-200

--color-accent-ai:       color-tertiary-500
--color-accent-warning:  color-quaternary-500
--color-accent-success:  color-senary-500
```

Reference **semantic tokens** in component styles, never raw hex. The
semantic layer is what enforces the CTA-vs-brand discipline.

### Step 3 — Apply chrome markup

Every Creator marketing page must use this header and footer structure.

#### Header

```html
<header class="creator-header">
  <div class="creator-header-inner">
    <a href="/" class="creator-wordmark">Creator</a>
    <nav class="creator-nav">
      <a href="/features">Features</a>
      <a href="/pricing">Pricing</a>
      <a href="/customers">Customers</a>
      <a href="/resources">Resources</a>
    </nav>
    <div class="creator-header-actions">
      <a href="/login" class="creator-link">Sign in</a>
      <a href="/signup" class="creator-cta">Get Started</a>
    </div>
  </div>
</header>
```

#### Footer

```html
<footer class="creator-footer">
  <div class="creator-footer-inner">
    <a href="/" class="creator-wordmark creator-wordmark--inverse">Creator</a>
    <nav class="creator-footer-nav">
      <!-- product, resources, company, legal columns -->
    </nav>
    <div class="creator-footer-meta">
      © Zoho Corporation. All rights reserved.
    </div>
  </div>
</footer>
```

#### Header / footer CSS (semantic tokens only)

```css
.creator-header {
  background: var(--color-surface-page);
  border-bottom: 1px solid var(--color-border-default);
  position: sticky; top: 0; z-index: 100;
}

.creator-wordmark {
  color: var(--color-brand);   /* ALWAYS brand blue, never CTA red */
  font-family: var(--font-display);
  font-weight: 600;
  text-decoration: none;
}

.creator-nav a {
  color: var(--color-text-body);
}
.creator-nav a:hover {
  color: var(--color-brand);
}

.creator-cta {
  background: var(--color-cta);   /* ALWAYS CTA red, never brand blue */
  color: var(--color-surface-page);
  border-radius: var(--cds-radius-xs);  /* from radius.json — Radius/sm = 4px */
  font-weight: 600;
}
.creator-cta:hover  { background: var(--color-cta-hover); }
.creator-cta:active { background: var(--color-cta-active); }

.creator-footer {
  background: var(--color-surface-darkest);
  color: var(--color-surface-page);
}
```

For exact padding, gaps, font sizes — pull from `foundations/spaces.json`,
`foundations/typography.json`, and `components/cta-buttons.json`. **Do not
hardcode pixel values.**

### Step 4 — Font stack mapping

Use the CDS-canonical font stack from `foundations/typography.json`:

```css
:root {
  --font-display: <typography.json → fontFamily.stack>;
  --font-body:    <same stack — Zoho Puvi → Inter → system-ui fallback>;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 600;
}

body, p, button, input, .creator-nav {
  font-family: var(--font-body);
}
```

For exact size and line-height per heading and text tier, defer to
`design-system/foundations/typography.json`.

### Step 5 — Verify before saving

Before finalizing any output, scan your CSS for:

* Any raw hex codes — replace with semantic tokens or `colours.json` references.
* Any pixel values for spacing — replace with `spaces.json` token references.
* Any pixel values for font size — replace with `typography.json` token references.
* Any non-CTA element using `--color-cta` — replace with `--color-brand` or a neutral.
* Any CTA button using `--color-brand` — replace with `--color-cta`.
* The "Creator" wordmark in header and footer — must be `--color-brand`, never `--color-cta`.

---

## What this skill does NOT cover

* **Colour values** — `design-system/foundations/colours.json`.
* **Spacing, grid, breakpoints** — `design-system/foundations/{spaces,grids}.json`.
* **Typography sizes / weights** — `design-system/foundations/typography.json`.
* **Elevation, radius** — `design-system/foundations/{elevation,radius}.json`.
* **CTA component spec** (5 variants × 4 sizes × 3 states) —
  `design-system/components/cta-buttons.json`.
* **Accessibility** — `design-system/accessibility/wcag.json`.
* **Page section patterns** (hero, pricing cards, resource grids) — separate concern.
* **Animations and interactions** — separate concern.

If you need any of the above, the `creator-design-system` skill handles them.
This skill's job is purely Creator chrome, font stack, and the CTA-vs-brand
discipline — and it cannot do that job without the design-system folder.