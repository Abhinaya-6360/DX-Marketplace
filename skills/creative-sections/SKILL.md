---
name: creative-sections
description: Build reusable, design-forward landing-page sections — heroes, feature blocks, testimonials, stat/numeric visuals, pricing tables, CTAs, footers, FAQs, logo strips, team grids, blog previews, timelines, comparison tables, integrations grids, before/after, and bento layouts — using STRICT Creator Design System (CDS) tokens from the bundled `design-system/` folder. Every output uses ONLY CDS colours, typography, spacing, elevation, radius, and the canonical CTA button component. Use this skill ANY time the user asks to build, design, or generate landing-page sections, marketing blocks, hero sections, feature sections, pricing tables, testimonial blocks, stat/numeric showcases, CTAs, or any individual section of a marketing/product page — even if they don't say "section" explicitly. Trigger on phrases like "build a hero", "design a pricing table", "I need a features section", "make a testimonials block", "create a landing page section", "design a stats section", "bento grid", "comparison table", or any request that's clearly one or more marketing-page blocks rather than a full app. Also trigger when the user wants creative/varied design directions for marketing UI under the CDS brand. Do NOT trigger for full SaaS apps, dashboards, admin UIs, or non-marketing components.
---

# Creative Sections — CDS-Strict

A library of reusable, mix-and-match landing-page sections. The user picks the sections and a creative direction, and Claude builds them using **only** Creator Design System (CDS) tokens — colours, type, spacing, elevation, radius, and the canonical CTA button component bundled in `design-system/`.

Style variety in this skill comes from **how CDS tokens are composed** (which colour family, which type weight, which spacing rhythm, which radius tier) — not from inventing new colours, fonts, or shadows.

---

## Data Access Rule (BLOCKING)

This skill **cannot generate output** without access to the canonical token files. Specifically, it requires:

* `design-system/DESIGN.md` — loader rules
* `design-system/index.json` — manifest of available token files
* `design-system/foundations/colours.json` — every hex value
* `design-system/foundations/typography.json` — type sizes, line heights, weights
* `design-system/foundations/spaces.json` — padding and gap values
* `design-system/foundations/radius.json` — corner radius values
* `design-system/foundations/elevation.json` — drop shadow values
* `design-system/foundations/grids.json` — breakpoints and column widths
* `design-system/components/cta-buttons.json` — CTA button variants/sizes/states
* `design-system/accessibility/wcag.json` — contrast pairings and audit results

If `design-system/` is not at the repo root, **STOP**:

* Do not generate any output.
* Do not fall back to values inlined in any other skill, file, or recipe.
* Do not use values from training data, web fetches, or memory.
* Do not invent token names, hex values, sizes, or radii.

Ask the user to either:

1. `cd` into the repo that contains the design-system folder, or
2. Explicitly point Claude at the correct project path.

This rule is BLOCKING. The design system is the single source of truth — without it, no output is valid.

---

## CDS Loading Workflow

On every invocation, in order:

1. Read `design-system/DESIGN.md` — confirms the loader rules are intact.
2. Read `design-system/index.json` — confirms token files exist.
3. Load only the token files needed for the requested sections (see Data Access Rule above for the full list).
4. Load the CTA button spec → `design-system/components/cta-buttons.json`. **All buttons in output must use one of the 5 canonical variants × 4 sizes × 3 states defined here.**
5. Load `design-system/accessibility/wcag.json` and reject any colour pairing flagged `fail` in `checklists.colours` regardless of what the user requests.

---

## Strict CDS Rules (non-negotiable)

These apply to every output:

* **Tokens only.** No raw hex, no raw px, no eyeballed values. Every colour, size, space, shadow, and radius must come from the JSON token files. If you write `#ff3b00` or `padding: 17px`, you have failed.
* **One font family.** Zoho Puvi, with the fallback stack from `typography.json`. No serif headlines, no monospace gimmicks unless rendering an actual code block.
* **No invented components and no component overrides.** Buttons must use the exact CTA button spec — 5 variants (Primary, Primary Line, Secondary, Secondary Line, Tertiary), 4 sizes (XS/SM/MD/LG), 3 states (default/hover/active). Border radius is 4px (`btn-radius`). Border width is 2px (`btn-border-width`). **You may not override colour, border, padding, or any other property of a canonical CTA variant — not even "for dark mode."** If a needed CTA variant doesn't exist, ASK the user; do not invent one.
* **One primary CTA per surface.** Per `cta-buttons.json` usage rules.
* **Spacing must be on the 4px grid.** Use named tokens (`space-md-2`, `space-lg-5`, etc.), never custom values like `13px` or `42px`.
* **Type hierarchy from typography.json.** H1 → H6 → text-large → text-medium → text-regular → text-small. Don't skip tiers without reason.
* **Use semantic colour pairings only.** Primary blue family for primary surfaces/links/marks. Secondary red family for destructive/alert. Quaternary/quinary/senary for accents and data viz only — never as core brand surfaces. White/grey for neutrals.
* **A11y is enforced, not aspirational.** Before output, cross-check every text/background pair against `accessibility/wcag.json → checklists.colours`. Reject any pair flagged `fail`. Known failing pairs include white on Secondary 500, Grey 400 on white for body, and Grey 200 interactive borders. Substitute the next-darker shade and document the choice.
* **If a token is missing for what you need → ASK the user, do not substitute.**

---

## Three terms to disambiguate

CDS uses the word "primary" in three different senses. Don't confuse them:

1. **Primary colour family** = `colours.families.primary` — Bright Royal Blue. Used for: links, brand marks, hero accents, soft surface tints. Token paths look like `color-primary-500`, `color-primary-0`, etc.
2. **Primary CTA component variant** = `cta-buttons.variants.primary` — the **red** filled button (uses the Button-cta-red scale). Used for: any "primary action" the page wants the user to take.
3. **"Primary action" semantic concept** = the most important thing on the page. Almost always rendered with the Primary CTA component (red).

When a recipe says "use Primary CTA," it means the **red** filled component, not a blue button. Blue surfaces and red CTAs coexist intentionally — that is the CTA-vs-brand discipline rule from `creator-visual-language`.

---

## Core Workflow

Always follow these four steps in order:

### 1. Understand what they want

Figure out:

* **Which section(s)** — hero, features, testimonials, stats, pricing, CTA, footer, FAQ, logos, team, blog preview, timeline, comparison, integrations, before/after, bento.
* **What product/context** — needed for realistic content (see step 3).
* **What stack they're using** — match it. Default for fresh projects: single HTML file with CDS tokens emitted as CSS custom properties from the JSON `flat` blocks.

If any of these are ambiguous, ask before continuing.

### 2. Offer 2–3 creative directions BEFORE building

Style variety in CDS-land comes from token composition, not from new design languages. Present 2–3 distinct directions the user can choose from. Each direction is a recipe of CDS tokens defined in `references/directions.md`.

The 8 available CDS-aligned creative directions:

1. **Brand Bold** — Primary 500 brand blue on white. Display + H1 in bold weight. Radius-md/lg cards, elevation-sm. Big confident brand surfaces. The default for marketing.
2. **High Contrast Mono** — Black on white only, Grey scale for hierarchy. Radius-xs/sm. Hairline borders. Swiss/architectural energy.
3. **Dark Surface** — Dark Grey 700 background, white type, Quinary 500 (Electric Lime) accent. Elevation-md for cards. Premium tech feel.
4. **Editorial Brand** — White surfaces with Primary 500 used as a single accent ribbon/highlight. Display Bold for the hero, generous lg/xl spacing. Confident, magazine-style.
5. **Triadic Energy** — Primary 500 + Secondary 600 + Tertiary 500 used together for sectional rhythm. For loud, confident multi-section pages.
6. **Yellow-Hero** — Quaternary 500 hero block, black type, Primary CTAs against white below.
7. **Lime-Pop** — Quinary 500 accents on white surfaces, black type. Senary 700 for positive/growth stats.
8. **Soft Brand** — Primary 0 / Primary 50 light surfaces, Primary 900 type for headlines, white cards. Calm fintech-adjacent feel.

Tailor 2–3 picks to the product. Examples:

* Developer tool / dense product → High Contrast Mono / Dark Surface / Brand Bold
* Consumer / playful → Yellow-Hero / Lime-Pop / Editorial Brand
* Fintech / serious → Brand Bold / Soft Brand / High Contrast Mono
* Premium / agency → Editorial Brand / Dark Surface / High Contrast Mono

### 3. Generate realistic, product-matched content

Never lorem ipsum. Specific headlines, plausible stats, real-feeling testimonials with named people and titles that fit the audience, pricing tiers that match the market, FAQ questions a real prospect would ask. Ask 1–2 clarifying questions if you don't know the product well enough.

### 4. Build, matching their stack — with CDS tokens emitted as CSS variables

When generating HTML/CSS/JSX:

* Emit CDS tokens as CSS custom properties at the top of the file using the `flat` blocks from each JSON file. Then reference them via `var(--token-name)` everywhere. Do not put raw hex/px values in the markup.
* For Tailwind: use the `tailwind` blocks where provided (radius, elevation) or arbitrary values that reference CSS variables: `bg-[var(--color-primary-500)]`, `p-[var(--space-md-2)]`.
* Buttons must render as the CTA button component spec from `components/cta-buttons.json`. Use the exact heights, paddings, gaps, font sizes, and state colours.
* Type uses the font stack from `typography.json`; sizes from the type tier names (display, h1, h2, …, text-medium, text-small).
* Section padding uses `space-lg-*` or `space-xl-*`. Component padding uses `space-md-*`. Inline gaps use `space-sm-*`.

#### Output destination

Save as a single self-contained file in the user's project. Choose the destination based on the runtime environment:

* **In Claude Code (local terminal):** save next to the user's other project files, typically in the working directory, or in `examples/` if the repo has one. Confirm the path with the user if unclear.
* **In a Claude.ai sandbox or Anthropic-hosted environment:** save to `/mnt/user-data/outputs/` and present via `present_files`.

Default to the working directory and announce the saved path. Do not assume a sandbox path exists.

---

## Section Patterns

Read `references/directions.md` for the exact CDS token recipe for each of the 8 creative directions — which colour scale levels, which type weights, which radius tiers, which elevations, which a11y notes apply.

Layout structure (centred vs split vs asymmetric heroes, 3-tier vs 4-tier pricing, etc.) is a free composition decision per section, not bound to a specific direction. The directions govern *visual language*; layout is independent.

---

## Output Format

After building, present the file and write a short message that:

1. Names the CDS direction used and why it fit the product
2. Lists the sections included
3. Lists the specific token decisions (e.g., "color-primary-500 for surfaces, color-grey-500 for body, space-lg-5 for section padding, radius-md for cards, shadow-sm on hover")
4. Notes any a11y trade-offs handled (e.g., "used color-secondary-600 not 500 for white-on-red text per wcag.json")

Keep it brief.

---

## Critical Rules (recap)

* **Read `design-system/DESIGN.md` and the relevant token JSONs every time.** Don't generate from memory.
* **Stop and ask if `design-system/` is missing.** No fallbacks, no inlined values, no inventions.
* **Always offer 2–3 directions first.** Never pick silently.
* **Tokens only — never raw values.** Emit CSS variables at the top, reference them everywhere.
* **One CTA button component spec, no overrides.** No custom buttons. If a variant is missing, ASK.
* **Realistic content, not lorem ipsum.**
* **One direction per output.** Don't mix directions across sections in a single file.
* **A11y enforced via `wcag.json`.** Reject failing pairs at generation time, not after.