# CDS Direction Recipes

Each direction is a specific composition of CDS tokens. Use these recipes verbatim — do not substitute tokens or invent values. All token names map to entries in `design-system/foundations/*.json` and `design-system/components/cta-buttons.json`.

---

## Token reference key

* `colours.flat["color-X-Y"]` → `var(--color-X-Y)` in CSS
* `spaces.flat["space-X-Y"]` → `var(--space-X-Y)`
* `radius.flat["radius-X"]` → `var(--radius-X)`
* `elevation.flat["shadow-X"]` → `var(--shadow-X)`
* `typography` tier names: `display`, `h1`–`h6`, `text-large`, `text-medium`, `text-regular`, `text-small`

CTA buttons always use the spec from `components/cta-buttons.json` — never override any colour, border, padding, or other property. The spec already includes light-on-light and dark-on-dark behaviours via the 5 variants.

**Hex values are intentionally omitted from this file.** Resolve every token name to its hex by reading `colours.json`. Single source of truth.

---

## "Primary" disambiguation

Three things are called "primary" in CDS — don't confuse them in any recipe:

1. **Primary colour family** = `color-primary-*` — Bright Royal Blue scale.
2. **Primary CTA variant** = `cta-buttons.variants.primary` — the red filled button (uses Button-cta-red scale).
3. **Primary action** = the most important action on the page, rendered with the Primary CTA variant.

When a recipe says "Primary CTA," it means the red filled button. Blue surfaces and red CTAs coexist by design — see `creator-visual-language` for the full CTA-vs-brand discipline.

---

## 1. Brand Bold

The default. Big, confident, brand-forward.

| Surface | Token |
|---|---|
| Page background | `color-white` |
| Section alt background | `color-grey-0` for rhythm |
| Body text | `color-grey-500` |
| Headline text | `color-black` |
| Brand accent | `color-primary-500` |
| Brand accent hover/active | `color-primary-600` / `color-primary-700` |
| Card background | `color-white` |
| Card border | none — use `shadow-xs` resting, `shadow-sm` hover |
| Card radius | `radius-md` |
| Highlighted/featured card radius | `radius-lg` |
| Hero padding (vertical) | `space-xl-3` desktop · `space-lg-5` tablet · `space-md-6` mobile |
| Section padding | `space-lg-5` desktop |
| Component padding | `space-md-2` |
| Inline gap | `space-sm-3` to `space-sm-4` |

**Type recipe**

* Hero headline: `display`, bold
* Section headlines: `h2`, bold
* Card titles: `h5`, semibold
* Body: `text-medium`, regular
* Eyebrow / labels: `text-small`, semibold, uppercase, letter-spacing 0.08em

**CTA recipe**

* Hero primary: `Primary` variant, `LG` size
* Hero secondary: `Secondary Line` variant, `LG` size
* Pricing CTAs: `Primary` variant on featured tier, `Secondary Line` on others, `MD` size

---

## 2. High Contrast Mono

Black on white, grey hierarchy. No colour. Swiss/architectural.

| Surface | Token |
|---|---|
| Page background | `color-white` |
| Section alt background | `color-grey-0` |
| Body text | `color-grey-700` |
| Headline text | `color-black` |
| Borders (decorative) | `color-grey-200` |
| Borders (interactive) | `color-grey-500` (Grey 200 fails non-text contrast) |
| Hairline rule | 1px solid `color-grey-200` |
| Card radius | `radius-xs` |
| Button radius | per CTA spec (`btn-radius` = 4px) |
| Elevation | none — use hairline rules instead |
| Section padding | `space-lg-5` desktop |
| Hero padding | `space-xl-2` desktop |
| Component padding | `space-md-2` |

**Type recipe**

* Hero headline: `display`, bold
* Section eyebrow: `text-small`, semibold, uppercase
* Body: `text-medium`, regular, max-width 65ch
* Stats numbers: `h1`, bold

**CTA recipe**

* Primary: `Secondary` variant (black fill, white text), `LG` size
* Secondary: `Secondary Line` variant (black border, transparent), `LG` size
* Tertiary CTAs: `Tertiary` variant, `MD` size

**Forbidden:** any colour family except black, white, and grey scales.

---

## 3. Dark Surface

Dark mode marketing. Premium tech.

| Surface | Token |
|---|---|
| Page background | `color-dark-grey-700` |
| Section alt background | `color-dark-grey-500` |
| Body text | `color-grey-200` (passes 9.9:1 on dark-grey-700) |
| Headline text | `color-white` |
| Borders | `color-grey-800` |
| Brand accent (fills/decoration) | `color-quinary-500` (Electric Lime) |
| Brand accent (text) | `color-quinary-300` (better contrast on dark backgrounds) |
| Card background | `color-dark-grey-500` |
| Card radius | `radius-md` |
| Card elevation | `shadow-md` |
| Section padding | `space-lg-5` desktop |
| Hero padding | `space-xl-3` desktop |

**Type recipe**

* Hero headline: `display`, bold, `color-white`
* Accent word in headline: same size, `color-quinary-300` for type-on-dark contrast
* Body: `text-medium`, `color-grey-200`
* Stats numbers: `h1`, bold, `color-quinary-300`

**CTA recipe**

The CDS CTA spec works on dark surfaces without overrides:

* Primary action: `Primary` variant, `LG` size — the red filled button reads correctly on dark grey at 4.66:1 contrast (white-on-red).
* Secondary action: `Secondary` variant, `LG` size — black fill with white text. On a dark grey page background, the black button reads as a deeper, distinct shape; pairs naturally with the Primary red.
* Tertiary action: `Primary Line` variant, `LG` size — blue outline with blue text. The brand-blue stroke (`color-primary-500`) has 4.5:1+ contrast against `color-dark-grey-700` background and is the "ghost" CTA for dark surfaces.

**Do not** override the `Tertiary` variant (white background / black text) onto a dark surface — it inverts the page rhythm and breaks the component spec. Use `Primary Line` instead.

**A11y note**

Test any quinary text against the dark background. Use the **300** level for type, reserve the **500** level for fills and decorative elements only.

---

## 4. Editorial Brand

White surfaces with Primary 500 as a single editorial accent.

| Surface | Token |
|---|---|
| Page background | `color-white` |
| Body text | `color-grey-700` |
| Headline text | `color-black` |
| Single accent | `color-primary-500` — used for one ribbon/underline/highlight per section, no more |
| Card border | 1px `color-grey-100` |
| Card radius | `radius-sm` |
| Elevation | `shadow-xs` only |
| Section padding | `space-xl-1` desktop |
| Hero padding | `space-xl-5` desktop |
| Component padding | `space-md-3` |

**Type recipe**

* Hero headline: `display`, bold, with one accent word wrapped in a `color-primary-500` underline or background highlight
* Numbered eyebrows ("01 / FEATURES"): `text-small`, semibold, uppercase, `color-grey-500`
* Body: `text-large` for hero subhead, `text-medium` for everything else
* Pull quotes: `h4`, regular, italic via `font-style: italic`

**CTA recipe**

* Primary: `Primary Line` variant, `LG` size — editorial restraint
* Secondary: `Tertiary` variant, `LG` size

---

## 5. Triadic Energy

Primary + Secondary + Tertiary used together for section-by-section rhythm.

| Section pattern | Tokens |
|---|---|
| Section A (hero) | bg `color-primary-500`, type `color-white` |
| Section B (features) | bg `color-white`, type `color-black` |
| Section C (testimonials) | bg `color-tertiary-500`, type `color-white` |
| Section D (stats) | bg `color-white`, type `color-black` |
| Section E (pricing) | bg `color-secondary-600` (NOT 500 — fails contrast), type `color-white` |
| Section F (CTA) | bg `color-black`, type `color-white` |
| Card radius | `radius-md` |
| Card elevation on coloured sections | none — cards invert to white-on-coloured |
| Section padding | `space-lg-5` desktop |

**Type recipe**

* All headlines: `display` or `h2`, bold
* Body: `text-medium`, regular

**CTA recipe**

* On `color-primary-500` blue or `color-tertiary-500` violet sections: `Primary` variant — the red CTA pops against blue/violet at high contrast.
* On `color-secondary-600` red sections: `Tertiary` variant (white background, black text) — gives a clean inverse against red without overriding any spec.
* On `color-white` sections: `Primary` variant standard.
* On `color-black` CTA section: `Tertiary` variant (white-on-dark inverse) or `Primary` variant (red on black, also strong).

**A11y note**

Always use Secondary **600** not **500** when white text sits on it (Secondary 500 + white fails AA at 3.94:1; Secondary 600 + white passes at 4.97:1).

---

## 6. Yellow-Hero

Yellow hero block grabs attention; rest of page is calm.

| Surface | Token |
|---|---|
| Hero background | `color-quaternary-500` (Radiant Yellow) |
| Hero text | `color-black` (passes 13.5:1 contrast) |
| Page body background | `color-white` |
| Body text | `color-grey-700` |
| Headlines below hero | `color-black` |
| Brand accent below hero | `color-primary-500` |
| Card radius | `radius-md` |
| Elevation | `shadow-xs` resting, `shadow-sm` hover |
| Hero padding | `space-xl-3` desktop |
| Section padding | `space-lg-5` desktop |

**Type recipe**

* Hero headline: `display`, bold, black on yellow
* Body in hero: `text-large`, black
* Section headlines: `h2`, bold

**CTA recipe**

* In hero (on yellow): `Secondary` variant (black fill, white text), `LG` — passes contrast trivially against yellow
* Below hero: `Primary` variant, `MD` size
* Tertiary actions: `Tertiary` variant

---

## 7. Lime-Pop

Lime as accent, white surfaces, black type, senary green for positive metrics.

| Surface | Token |
|---|---|
| Page background | `color-white` |
| Section alt background | `color-grey-0` |
| Body text | `color-grey-700` |
| Headline text | `color-black` |
| Accent fills (small) | `color-quinary-500` (Electric Lime) — pairs with black text only at 17:1 |
| Positive metric colour | `color-senary-700` (passes 4.5:1+ on white) |
| Negative metric colour | `color-secondary-600` |
| Card radius | `radius-md` |
| Elevation | `shadow-xs` resting |
| Section padding | `space-lg-5` desktop |

**Type recipe**

* Hero: `display`, bold, with one word wrapped in a `color-quinary-500` background block
* Stats numbers: `h1`, bold — `color-senary-700` if positive, `color-grey-700` if neutral
* Body: `text-medium`

**CTA recipe**

* Primary: `Primary` variant, `LG` size
* Secondary: `Secondary Line` variant, `LG` size

---

## 8. Soft Brand

Light brand tints for calm, trustworthy surfaces.

| Surface | Token |
|---|---|
| Page background | `color-primary-0` |
| Section alt background | `color-white` |
| Body text | `color-grey-700` |
| Headline text | `color-primary-900` |
| Card background | `color-white` |
| Card border | 1px `color-primary-100` |
| Card radius | `radius-lg` |
| Elevation | `shadow-xs` resting, `shadow-sm` hover |
| Brand accent | `color-primary-500` |
| Section padding | `space-lg-5` desktop |
| Hero padding | `space-xl-2` desktop |

**Type recipe**

* Hero: `h1`, bold (slightly less assertive than display), `color-primary-900`
* Section headlines: `h2`, semibold
* Body: `text-medium`, `color-grey-700`
* Eyebrow: `text-small`, semibold, uppercase, `color-primary-700`

**CTA recipe**

* Primary: `Primary` variant, `LG` size — the red pops responsibly against calm tints
* Secondary: `Primary Line` variant, `LG` size

---

## Cross-cutting rules for ALL directions

1. **Buttons.** Always render exactly per `components/cta-buttons.json`. Heights: XS=32, SM=40, MD=48, LG=56. Padding/gap/font-size from the spec. **No overrides — ever.**
2. **Spacing rhythm.** Section padding scales: desktop `space-lg-5` (or `space-xl-*` for hero), tablet `space-md-6`, mobile `space-md-3`.
3. **Radius nesting.** Inner elements use a smaller radius than their container. Card at `radius-md` → button at `btn-radius` (4px) → chip at `radius-full`.
4. **Elevation hierarchy.** XS rest → S hover → M floating UI. Don't stack shadows.
5. **Type rhythm.** No more than 4 different sizes per section. Hierarchy comes from weight + size, not from inventing styles.
6. **A11y enforced, not aspirational.** Cross-check every text/background pair against `accessibility/wcag.json → checklists.colours`. Reject any pair flagged `fail`. Known failing pairs:
   * White text on `color-secondary-500` → use `color-secondary-600` instead, or large text only.
   * `color-grey-400` body text on white → use `color-grey-500` or darker.
   * `color-grey-200` for any interactive border → use `color-grey-500` or darker.