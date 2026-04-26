# Creator Chrome — Header & Footer

The exact markup, font stack, and CDS-aligned colors used across https://www.zoho.com/en-in/creator/. Copy these verbatim into every generated page.

## Brand colors — from CDS Figma (Foundations/brandColours, node 7074:749)

The Creator brand palette is **CDS-defined**: 11 families, 98 tokens. Use these exact values — the live www.zoho.com/creator site uses an older red-based theme; the CDS palette is the source of truth.

### Section 02 — Brand (the hero palette)

```css
/* Primary — Bright Royal Blue (Pantone Reflex Blue C) */
--cds-primary-0:   #F3F7FF;
--cds-primary-50:  #E4EDFF;
--cds-primary-100: #CCDAFF;
--cds-primary-200: #9AB6FF;
--cds-primary-300: #6691FF;
--cds-primary-400: #336DFF;
--cds-primary-500: #0047FF;   /* CORE — primary buttons, links, brand marks */
--cds-primary-600: #003ACC;   /* hover */
--cds-primary-700: #012B99;   /* active */
--cds-primary-800: #001D66;
--cds-primary-900: #000E33;
--cds-primary-950: #000719;

/* Secondary — Vivid Red (Pantone Red 032 C) — destructive / error / critical only */
--cds-secondary-500: #FF0405;
--cds-secondary-600: #D10000;
--cds-secondary-700: #9F0101;

/* Tertiary — Vibrant Violet (Pantone Violet C) — AI / premium / creative */
--cds-tertiary-500: #5E05FF;
--cds-tertiary-600: #4900D1;
--cds-tertiary-700: #37009F;
```

### Section 03 — Accents (use sparingly, with intent)

```css
--cds-quaternary-500: #FED70B;   /* Radiant Yellow — highlights, warnings, marketing emphasis */
--cds-quinary-500:    #E6FF0A;   /* Electric Lime — data viz, callout badges */
--cds-senary-500:     #03FF17;   /* Vivid Green — success / positive deltas */
```

### Section 01 — Neutrals (12 tokens each scale)

```css
/* Absolute */
--cds-white: #FFFFFF;
--cds-black: #000000;

/* Grey Scale — neutral greys for body text, borders, dividers */
--cds-grey-0:   #FAFAFA;
--cds-grey-50:  #F5F5F5;
--cds-grey-100: #EBEBEB;
--cds-grey-200: #D1D1D1;
--cds-grey-300: #B5B5B5;
--cds-grey-400: #919191;
--cds-grey-500: #595959;   /* CORE — body text default */
--cds-grey-600: #4F4F4F;
--cds-grey-700: #454545;
--cds-grey-800: #383838;
--cds-grey-900: #262626;
--cds-grey-950: #1A1A1A;

/* Dark Grey — near-black scale for dense data, dark surfaces, dark mode */
--cds-dark-500: #0F0F0F;   /* CORE — Deep Neutral */
--cds-dark-700: #0A0A0A;
--cds-dark-900: #050505;
```

### Section 04 — Reserved component scales

The Button Action Red ramp is **the primary CTA color** for Creator marketing pages. Use the full scale.

```css
/* Button Action Red — primary CTA across all Creator pages */
--cds-button-red-0:   #FEF1F1;
--cds-button-red-50:  #FDE3E3;
--cds-button-red-100: #F9ADAE;
--cds-button-red-200: #F77071;
--cds-button-red-300: #E42527;   /* CORE — primary CTA, hero buttons, plan CTAs */
--cds-button-red-400: #A41719;   /* hover */
--cds-button-red-500: #680B0C;   /* active / pressed */
--cds-button-red-600: #320203;
```

## Semantic mapping (use these in component styles)

**Strict color rule, no exceptions:**
- **`#E42527` red is for CTA buttons only** — buttons that initiate a primary action ("Get Started", "Start Free Trial", "Contact Sales", "Subscribe", footer band action button, header action button). Solid filled buttons or outline-buttons-on-hover that lead to conversion.
- **`#0047FF` blue is the primary brand color for everything else interactive** — links, the Creator wordmark, nav hover states, FAQ chevrons, outline button hovers (when the button is not a CTA), section accents, plan ribbons, badges, decorative checkmarks, featured borders, hero tints, focus rings.
- **Complementary accents** from the CDS palette are used where intent matches: violet `#5E05FF` for AI/premium moments, yellow `#FED70B` for warning/marketing emphasis, lime `#E6FF0A` for data viz, green `#03FF17` for success only.

If you're unsure whether something is a "CTA" or not, ask: *does clicking this take the user toward signing up, paying, or contacting sales?* If yes → red. If it's a link, hover affordance, decorative element, or section accent → blue.

```css
/* CTA — RED, only for primary action buttons */
--color-cta:               var(--cds-button-red-300);   /* #E42527 */
--color-cta-hover:         var(--cds-button-red-400);   /* #A41719 */
--color-cta-active:        var(--cds-button-red-500);   /* #680B0C */
--color-cta-soft:          var(--cds-button-red-50);    /* tinted bg / focus ring */

/* Brand — BLUE, primary color for everything non-CTA */
--color-brand:             var(--cds-primary-500);      /* #0047FF */
--color-brand-hover:       var(--cds-primary-600);
--color-brand-active:      var(--cds-primary-700);
--color-brand-soft:        var(--cds-primary-0);        /* #F3F7FF — hero tints, soft surfaces */
--color-brand-soft-2:      var(--cds-primary-50);       /* #E4EDFF */

/* Text */
--color-text-primary:   var(--cds-black);
--color-text-body:      var(--cds-grey-500);
--color-text-secondary: var(--cds-grey-400);
--color-text-on-dark:   var(--cds-white);
--color-text-link:      var(--color-brand);

/* Surfaces */
--color-surface-page:    var(--cds-white);
--color-surface-subtle:  var(--cds-grey-0);
--color-surface-muted:   var(--cds-grey-50);
--color-surface-dark:    var(--cds-dark-500);
--color-surface-darkest: var(--cds-black);

/* Borders */
--color-border-default: var(--cds-grey-100);
--color-border-strong:  var(--cds-grey-200);

/* Accents — use sparingly */
--color-accent-ai:      var(--cds-tertiary-500);   /* #5E05FF — AI/premium */
--color-accent-warning: var(--cds-quaternary-500); /* #FED70B */
--color-accent-data:    var(--cds-quinary-500);    /* #E6FF0A */
--color-accent-success: var(--cds-senary-500);     /* #03FF17 */
```

### Where to apply each token

| Element | Token |
|---|---|
| Primary CTA button (filled) | `--color-cta` |
| Primary CTA button hover | `--color-cta-hover` |
| Outline CTA button hover (text/border) | `--color-cta` |
| Header "Get Started" / "Start Trial" / "Contact Sales" | `--color-cta` |
| Plan card CTA on featured plan (filled) | `--color-cta` |
| Plan card CTA on non-featured plan (outline → hover red) | `--color-cta` on hover |
| Footer band CTA | `--color-cta` |
| "Creator" wordmark in logo | `--color-brand` |
| Nav link hover | `--color-brand` |
| Inline links | `--color-brand` |
| Featured plan border / accent strokes | `--color-brand` |
| "Most Popular" ribbon, badges, chips | `--color-brand` |
| Plan card checkmarks | `--color-brand` |
| FAQ chevron + question hover | `--color-brand` |
| Hero soft gradient | `--color-brand-soft` |
| Card hover shadow tint | `--color-brand` (rgba) |
| AI / premium feature accents | `--color-accent-ai` |
| Success states / positive metrics | `--color-accent-success` |

## Font stack

Per CDS — Zoho Puvi for headings, Inter for body and UI.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
--font-puvi:  'Zoho Puvi', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-inter: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

Headings use Zoho Puvi 600 with `letter-spacing: -0.96px` (large displays) or `-0.4px` (20px Inter labels).

## Header

Sticky bar, Zoho logo left, primary nav center, Sign In + Get Started right. Mobile collapses to hamburger. The "Creator" wordmark in the logo uses `--color-action-primary` (CDS blue), not red.

```html
<header class="creator-header">
  <div class="creator-header__inner">
    <a href="/" class="creator-header__logo" aria-label="Zoho Creator">
      <span class="creator-header__logo-text">Zoho <span>Creator</span></span>
    </a>
    <nav class="creator-header__nav" aria-label="Main">
      <a href="/creator/features.html">Features</a>
      <a href="/creator/solutions/">Solutions</a>
      <a href="/creator/pricing.html">Pricing</a>
      <a href="/creator/resources/">Resources</a>
      <a href="/creator/customers.html">Customers</a>
    </nav>
    <div class="creator-header__actions">
      <a href="/creator/login.html" class="creator-header__signin">Sign In</a>
      <a href="/creator/signup.html" class="creator-header__cta">Get Started</a>
    </div>
    <button class="creator-header__menu-toggle" aria-label="Toggle menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
```

```css
.creator-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--color-surface-page);
  border-bottom: 1px solid var(--color-border-default);
  height: 64px;
}
.creator-header__inner {
  max-width: var(--grid-max-width);
  margin: 0 auto;
  padding: 0 48px;
  display: flex;
  align-items: center;
  height: 100%;
  gap: 32px;
}
.creator-header__logo-text {
  font-family: var(--font-puvi);
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -0.4px;
  color: var(--color-text-primary);
}
.creator-header__logo-text span { color: var(--color-brand); }
.creator-header__nav { display: flex; gap: 28px; flex: 1; }
.creator-header__nav a {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  text-decoration: none;
  transition: color 0.15s ease;
}
.creator-header__nav a:hover,
.creator-header__nav a.is-active { color: var(--color-brand); }
.creator-header__actions { display: flex; gap: 12px; align-items: center; }
.creator-header__signin {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  text-decoration: none;
}
.creator-header__signin:hover { color: var(--color-brand); }
.creator-header__cta {
  background: var(--color-cta);
  color: #fff !important;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s ease;
}
.creator-header__cta:hover { background: var(--color-cta-hover); }
.creator-header__menu-toggle { display: none; flex-direction: column; gap: 4px; background: none; border: none; cursor: pointer; padding: 8px; }
.creator-header__menu-toggle span { display: block; width: 22px; height: 2px; background: var(--color-text-primary); }

@media (max-width: 900px) {
  .creator-header__nav,
  .creator-header__signin { display: none; }
  .creator-header__menu-toggle { display: flex; margin-left: auto; }
}
```

## Footer

Footer uses `--color-surface-darkest` (CDS Black `#000000`). The "Creator" wordmark keeps `--color-action-primary`.

```html
<footer class="creator-footer">
  <div class="creator-footer__inner">
    <div class="creator-footer__col creator-footer__brand">
      <span class="creator-footer__brand-text">Zoho <span>Creator</span></span>
      <p>An AI-powered low-code platform that helps you build custom apps for any business need.</p>
    </div>
    <div class="creator-footer__col">
      <h4>Product</h4>
      <ul>
        <li><a href="/creator/features.html">Features</a></li>
        <li><a href="/creator/pricing.html">Pricing</a></li>
        <li><a href="/creator/integrations.html">Integrations</a></li>
        <li><a href="/creator/security.html">Security</a></li>
      </ul>
    </div>
    <div class="creator-footer__col">
      <h4>Resources</h4>
      <ul>
        <li><a href="/creator/resources/">Resource hub</a></li>
        <li><a href="/creator/community/">Community</a></li>
        <li><a href="/creator/customers.html">Customer stories</a></li>
        <li><a href="https://help.zoho.com/portal/en/kb/creator">Help</a></li>
      </ul>
    </div>
    <div class="creator-footer__col">
      <h4>Company</h4>
      <ul>
        <li><a href="/creator/about.html">About</a></li>
        <li><a href="/creator/careers.html">Careers</a></li>
        <li><a href="/creator/contact.html">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="creator-footer__legal">
    <span>© 2026 Zoho Corporation Pvt. Ltd. All rights reserved.</span>
    <div class="creator-footer__legal-links">
      <a href="/privacy.html">Privacy Policy</a>
      <a href="/terms.html">Terms of Service</a>
    </div>
  </div>
</footer>
```

```css
.creator-footer { background: var(--color-surface-darkest); color: var(--cds-grey-300); padding: 64px 0 0; }
.creator-footer__inner {
  max-width: var(--grid-max-width);
  margin: 0 auto;
  padding: 0 48px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 48px;
}
.creator-footer__brand-text {
  font-family: var(--font-puvi);
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -0.4px;
  color: #fff;
}
.creator-footer__brand-text span { color: var(--color-brand); }
.creator-footer__brand p { margin-top: 16px; font-size: 14px; line-height: 1.6; color: var(--cds-grey-400); max-width: 320px; }
.creator-footer__col h4 { font-family: var(--font-inter); font-size: 14px; font-weight: 600; color: #fff; margin: 0 0 16px; letter-spacing: 0.3px; text-transform: uppercase; }
.creator-footer__col ul { list-style: none; padding: 0; margin: 0; }
.creator-footer__col li { margin-bottom: 10px; }
.creator-footer__col a { color: var(--cds-grey-400); font-size: 14px; text-decoration: none; transition: color 0.15s ease; }
.creator-footer__col a:hover { color: #fff; }
.creator-footer__legal {
  border-top: 1px solid var(--cds-grey-800);
  padding: 24px 48px;
  max-width: var(--grid-max-width);
  margin: 48px auto 0;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--cds-grey-500);
}
.creator-footer__legal-links { display: flex; gap: 24px; }
.creator-footer__legal-links a { color: var(--cds-grey-500); text-decoration: none; }
.creator-footer__legal-links a:hover { color: #fff; }

@media (max-width: 768px) {
  .creator-footer__inner { grid-template-columns: 1fr 1fr; gap: 32px; padding: 0 24px; }
  .creator-footer__brand { grid-column: 1 / -1; }
  .creator-footer__legal { flex-direction: column; gap: 12px; padding: 24px; }
}
```

## Important usage rules — strict, no exceptions

1. **`#E42527` is for CTA buttons only.** Specifically: filled primary buttons that drive a conversion action ("Get Started", "Start Free Trial", "Contact Sales", "Subscribe", "Talk to Sales"), and the hover state of outline CTAs. Hover `#A41719`, active `#680B0C`. Use the semantic token `--color-cta`.
2. **`#0047FF` is the primary brand color for everything else interactive or branded.** Links, the "Creator" logo wordmark, nav hover, FAQ chevrons, plan ribbons, badges, decorative checkmarks, featured plan borders, hero gradient tints, card hover shadow tints, focus rings. Use `--color-brand`.
3. **Decision rule when unsure:** "Does clicking this take the user toward signing up, paying, or contacting sales?" → red CTA. Otherwise → blue.
4. **Complementary accents** are intent-driven: violet for AI/premium, yellow for warnings/marketing emphasis, lime for data viz, green for success only.
5. **Don't tint backgrounds with red.** Hero gradients, soft section backgrounds, card hover shadows — all use blue (`--color-brand-soft` for backgrounds, `rgba(0, 71, 255, 0.08)` for shadows).
6. **Vivid Red `#FF0405` (Section 02 Secondary)** is a different scale, reserved for error/critical alerts. Don't confuse with Button Action Red `#E42527`.
