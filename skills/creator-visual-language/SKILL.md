---
name: creator-visual-language
description: The visual language for Zoho Creator marketing pages — Creator header/footer chrome, font stack, and the strict CTA-vs-brand colour rule built on top of the Creator Design System (CDS). Use this skill any time you're styling a Zoho Creator page or component (pricing, resources, customers, communities, about, features, or any sibling of https://www.zoho.com/en-in/creator/) so the result matches Creator's branded chrome and CDS tokens. Trigger on phrases like "Creator-branded", "Zoho Creator page styling", "match the Creator homepage", "use Creator design tokens", "apply Creator chrome", "Creator header/footer". Defers to the creator-design-system skill for all colour, type, spacing, elevation, and component values.
---

# Creator Visual Language

The shared visual language for Zoho Creator marketing pages. This skill owns
three things, and three things only:

1. The **CTA-vs-brand colour discipline rule** (which hex goes on which UI element).
2. The **header and footer markup** that wraps every Creator page.
3. The **font stack and typography role mapping** for Creator surfaces.

Everything else — the full colour palette, spacing, elevation, components,
accessibility — comes from the `creator-design-system` skill, which reads the
canonical token files in `design-system/foundations/` and
`design-system/components/`.

---

## When to use

Any time you're producing HTML/CSS for a Zoho Creator marketing page. This
skill tells you:

* Which CDS colours to use, and where to use each one.
* The exact header and footer markup that wraps every Creator page.
* The font stack, semantic token naming, and brand discipline rules.

It does **not** prescribe page layouts, components, grids, breakpoints, or
animations — those are separate concerns owned by `creator-design-system`.

---

## The single most important rule

**CTAs are red. Everything else is blue.**

* **`#E42527` red (`--color-cta`)** — only for primary action buttons.
  "Get Started", "Start Free Trial", "Contact Sales", "Subscribe", "Talk to
  Sales" — buttons that drive a conversion. Hover `#A41719`, active `#680B0C`.
  These hex values come from `design-system/foundations/colours.json` →
  `families.buttonColorRed.scale.300/400/500`.
* **`#0047FF` blue (`--color-brand`)** — the brand colour for everything
  else interactive or branded. Links, the "Creator" wordmark, nav hover, FAQ
  chevrons, plan ribbons, badges, decorative checkmarks, featured plan
  borders, hero gradient tints, card hover shadow tints, focus rings.
  These hex values come from `design-system/foundations/colours.json` →
  `families.primary.scale.500/600/700` and `scale.0/50` for soft surfaces.

**Decision rule when unsure:** *Does clicking this take the user toward
signing up, paying, or contacting sales?* → red CTA. Otherwise → blue.

Never inline red into non-CTA elements. Never use blue on a primary action
button.

---

## Workflow

### Step 1 — Load colour values from CDS

Read `design-system/foundations/colours.json`. Use the `flat` block to
generate CSS custom properties. Map them to the semantic tokens below.

### Step 2 — Define semantic tokens at `:root`

```css
:root {
  /* CTA — RED, only for primary action buttons */
  --color-cta:        #E42527;   /* button bg */
  --color-cta-hover:  #A41719;
  --color-cta-active: #680B0C;

  /* Brand — BLUE, primary colour for everything else */
  --color-brand:        #0047FF;   /* links, wordmark, ribbons, badges */
  --color-brand-hover:  #003ACC;
  --color-brand-active: #012B99;
  --color-brand-soft:   #F3F7FF;   /* hero gradient end, soft section bg */
  --color-brand-soft-2: #E4EDFF;   /* alt soft surface */

  /* Text — from colours.json families.grey.scale */
  --color-text-primary:   #000000;   /* headings */
  --color-text-body:      #595959;   /* body copy (grey-500) */
  --color-text-secondary: #919191;   /* muted (grey-400) */

  /* Surfaces */
  --color-surface-page:    #FFFFFF;
  --color-surface-subtle:  #FAFAFA;   /* alt section bg (grey-0) */
  --color-surface-darkest: #000000;   /* footer / inverted CTA bands */

  /* Borders */
  --color-border-default: #EBEBEB;   /* grey-100 */
  --color-border-strong:  #D1D1D1;   /* grey-200 */

  /* Accents — sparing, intent-driven */
  --color-accent-ai:      #5E05FF;   /* tertiary-500 — AI / premium */
  --color-accent-warning: #FED70B;   /* quaternary-500 — yellow */
  --color-accent-success: #03FF17;   /* senary-500 — green */
}
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

#### Header / footer CSS skeleton

```css
.creator-header {
  background: var(--color-surface-page);
  border-bottom: 1px solid var(--color-border-default);
  position: sticky; top: 0; z-index: 100;
}

.creator-wordmark {
  color: var(--color-brand);   /* ALWAYS blue, never red */
  font-family: 'Zoho Puvi', Inter, system-ui, sans-serif;
  font-weight: 600;
  font-size: 24px;
  text-decoration: none;
}

.creator-nav a {
  color: var(--color-text-body);
}
.creator-nav a:hover {
  color: var(--color-brand);
}

.creator-cta {
  background: var(--color-cta);   /* ALWAYS red, never blue */
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: 600;
}
.creator-cta:hover  { background: var(--color-cta-hover); }
.creator-cta:active { background: var(--color-cta-active); }

.creator-footer {
  background: var(--color-surface-darkest);
  color: #FFFFFF;
  padding: 80px 0 40px;
}
```

### Step 4 — Font stack

Use the CDS-canonical font stack:

```css
:root {
  --font-display: 'Zoho Puvi', Inter, system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-body:    Inter, system-ui, -apple-system, 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 600;   /* Semibold */
}

body, p, button, input, .creator-nav {
  font-family: var(--font-body);
}
```

For exact size and line-height per heading and text tier, defer to
`design-system/foundations/typography.json`.

### Step 5 — Verify before saving

Before finalizing any output, scan your CSS for:

* Any raw hex codes — replace with semantic tokens.
* Any non-CTA element using `--color-cta` (red) — replace with `--color-brand` (blue) or a neutral.
* Any CTA button using `--color-brand` (blue) instead of `--color-cta` (red).
* The "Creator" wordmark in header and footer — must be blue (`--color-brand`), not red.

---

## What this skill does NOT cover

* **Full colour palette** — comes from `design-system/foundations/colours.json`
  via the `creator-design-system` skill.
* **Spacing, grid, breakpoints** — `design-system/foundations/{spaces,grids}.json`.
* **Typography sizes / weights** — `design-system/foundations/typography.json`.
* **Elevation, radius** — `design-system/foundations/{elevation,radius}.json`.
* **CTA component spec** (5 variants × 4 sizes × 3 states) —
  `design-system/components/cta-buttons.json`.
* **Accessibility** — `design-system/accessibility/wcag.json`.
* **Page section patterns** (hero, pricing cards, resource grids, customer
  story layouts) — separate concern.
* **Animations and interactions** (scroll fade-up, accordions, hover lifts) —
  separate concern.

If you need any of the above, the `creator-design-system` skill handles them.
This skill's job is purely Creator chrome, font stack, and the CTA-vs-brand
discipline.