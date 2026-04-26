---
name: creator-visual-language
description: The visual language for Zoho Creator marketing pages — CDS color palette, semantic tokens, Creator header/footer chrome, and the strict CTA-vs-brand color rule. Use this skill any time you're styling a Zoho Creator page or component (pricing, resources, customers, communities, about, features, or any sibling of https://www.zoho.com/en-in/creator/) so the result matches Creator's branded chrome and the Coda Design System (CDS). Trigger on phrases like "Creator-branded", "Zoho Creator page styling", "match the Creator homepage", "use Creator design tokens", "apply Creator chrome", "Creator header/footer", or any time the user shares Creator-related content and wants it styled correctly. This skill defines what a Creator page looks like — load it before writing any HTML/CSS for one.
---

# Creator Visual Language

The shared visual language for Zoho Creator marketing pages: CDS color tokens, header/footer chrome, font stack, and the strict color rule that distinguishes CTAs from brand accents.

## When to use

Any time you're producing HTML/CSS for a Zoho Creator marketing page or component. This skill tells you:

1. Which colors to use, and where to use each one.
2. The exact header and footer markup that wraps every Creator page.
3. The font stack, semantic token naming, and brand discipline rules.

It does **not** prescribe page layouts — section composition, grid patterns, and animations are separate concerns. This skill only defines the visual language those pages share.

## The single most important rule

**CTAs are red. Everything else is blue.**

- **`#E42527` red (`--color-cta`)** — only for primary action buttons. "Get Started", "Start Free Trial", "Contact Sales", "Subscribe", "Talk to Sales" — buttons that drive a conversion. Hover `#A41719`, active `#680B0C`.
- **`#0047FF` blue (`--color-brand`)** — the brand color for everything else interactive or branded. Links, the "Creator" wordmark, nav hover, FAQ chevrons, plan ribbons, badges, decorative checkmarks, featured plan borders, hero gradient tints, card hover shadow tints, focus rings.

**Decision rule when unsure:** *Does clicking this take the user toward signing up, paying, or contacting sales?* → red CTA. Otherwise → blue.

Never inline red into non-CTA elements. Never use blue on a primary action button.

## Workflow

### Step 1 — Read the chrome reference

Load `references/creator-chrome.md`. It contains:

- The full CDS brand palette (98 tokens, 11 families, extracted from Foundations/brandColours node 7074:749 in the CDS Figma)
- The semantic token mapping (`--color-cta`, `--color-brand`, plus text/surface/border tokens)
- The exact header and footer HTML markup
- The header and footer CSS skeleton
- The font stack and typography rules
- A mapping table of "where to apply each token"

Don't reverse-engineer any of this from memory or from the live www.zoho.com/creator site (which uses an older red-themed color scheme). The CDS palette in the chrome reference is the source of truth.

### Step 2 — Apply tokens consistently

When generating CSS:

- Define all CDS raw tokens (`--cds-primary-500`, `--cds-button-red-300`, etc.) and semantic tokens (`--color-cta`, `--color-brand`, `--color-text-body`, etc.) at `:root`.
- Reference **semantic tokens** in component styles, never raw scale tokens. The semantic layer enforces the CTA-vs-brand discipline.
- Use the chrome reference's header and footer markup verbatim — don't improvise the nav structure.
- Use the Zoho Puvi + Inter font stack per CDS. Headings in Zoho Puvi 600, body and UI in Inter.

### Step 3 — Verify before saving

Before finalizing any output, scan your CSS for:

- Any raw hex codes — replace with tokens.
- Any non-CTA element using `--color-cta` (red) — replace with `--color-brand` (blue) or a neutral.
- Any CTA button using `--color-brand` (blue) instead of `--color-cta` (red).
- The "Creator" wordmark in header and footer — must be blue (`--color-brand`), not red.

## Quick reference

```css
/* CTA — RED, only for primary action buttons */
--color-cta:        #E42527;   /* button bg, hover-state border/text on outline CTAs */
--color-cta-hover:  #A41719;
--color-cta-active: #680B0C;

/* Brand — BLUE, primary color for everything else */
--color-brand:        #0047FF;   /* links, wordmark, ribbons, badges, checkmarks, etc. */
--color-brand-hover:  #003ACC;
--color-brand-active: #012B99;
--color-brand-soft:   #F3F7FF;   /* hero gradient end, soft section bg */
--color-brand-soft-2: #E4EDFF;   /* alt soft surface */

/* Text */
--color-text-primary:   #000000;   /* headings */
--color-text-body:      #595959;   /* body copy */
--color-text-secondary: #919191;   /* muted */

/* Surfaces */
--color-surface-page:    #FFFFFF;
--color-surface-subtle:  #FAFAFA;   /* alt section bg */
--color-surface-darkest: #000000;   /* footer / inverted CTA bands */

/* Borders */
--color-border-default: #EBEBEB;
--color-border-strong:  #D1D1D1;

/* Accents — sparing, intent-driven */
--color-accent-ai:      #5E05FF;   /* violet — AI / premium */
--color-accent-warning: #FED70B;   /* yellow */
--color-accent-success: #03FF17;   /* green */
```

For the full 98-token palette, semantic mapping, where-to-apply table, header/footer HTML, and CSS skeletons, see `references/creator-chrome.md`.

## What this skill does NOT cover

- Page section patterns (hero, pricing cards, resource grids, customer story layouts, etc.) — those are page-shape decisions, not visual-language decisions.
- Animations or interactions (scroll fade-up, accordions, hover lifts) — separate concern.
- Grid system and breakpoints — covered in the broader CDS skill (`/mnt/skills/user/cds-design-system/`).
- Content-document parsing and authoring rules — separate concern.

If you need any of the above, layer the relevant skill on top of this one. This skill's job is purely to make sure colors, fonts, and chrome are right.
