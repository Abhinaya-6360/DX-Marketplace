# Changelog

## 2.7.0 — Nov 2026
- 45 icons added to assets/icons/icons.json (363 icons plus 5 social logos), from the deck icon clean-up: 1,212 old deck icons were mapped to the library with no repeats. 17 new Creator icons in the CDS custom style (32 grid, 2-unit line, round ends, Regular and Fill): api, ocr, erp, llm, ai-app-builder, ai-code, app-deploy, app-migration, app-settings, blueprint, cloud-app, code-editor, data-import, developer, form, integrations, mobile-app (llm, ai-app-builder and ai-code are AI-only, violet). 28 from Phosphor: butterfly, certificate, charging-station, file-pdf, footprints, gavel, hand, hand-coins, hand-fist, hand-heart, hand-pointing, hand-tap, hands-clapping, identification-badge, identification-card, link-break, mask-happy, password, pill, plant, police-car, recycle, security-camera, shuffle, solar-panel, steering-wheel, steps, translate. Matches the CDS-2.0 Figma file, Foundations · Icons.
- Icon rule: icons always come from the CDS 2.0 icon set; never emoji, icon fonts, other sets or generated images. If no CDS icon fits, Claude draws one in the CDS custom style, marks it data-cds-new-icon, and lists it in the handover for design review (replaces "never draw an icon"). SKILL.md, brand-rules.md, brand-check.md, icons.json (rule text and custom_style) and icon.py updated.
- check_system.py accepts a marked new icon that follows the custom style and reports it as NEW ICON for design review; an unmarked outside icon, or a marked one off-style, is still a violation.

## 2.6.0 — Nov 2026
- System first: SKILL.md now says to stay inside CDS 2.0 every time and to flag every violation. When a request or the marketer's material breaks the system, Claude says what doesn't fit, offers two or three on-system options that pass WCAG AA, and builds the best one; a violation is only made if the marketer insists, and it is listed under System violations in the handover.
- No emoji or symbol characters in any output; brand-rules.md maps common emoji to CDS icons (✅ check-circle, 🚀 rocket-launch, ⭐ star …).
- WCAG AA contrast written into the rules, with a table of safe text and background pairs (grey/120 is not for small text on blue/20 or violet/20; blue/100 is not for small text on yellow).
- New scripts/check_system.py: checks briefs, HTML, SVG and .pptx for emoji, outside colours, fonts and icons, red outside the main button, violet outside AI and partner topics, and AA contrast; `pairs` lists the safe pairs, `contrast` checks one pair.
- build_web, build_email, build_deck, render_social and render_print stop when the brief has emoji or outside colours (exit 2), unless run with --allow-violation.
- build_email.py example used an icon that isn't in the set (note-pencil); now pencil-simple.

## 2.5.0 — Nov 2026
- Headings are Semibold by default, matching the CDS-2.0 Figma file: display styles, social and video headlines (h1–h6), print headlines and big numbers, and web page drafts (h1, h2, stat numbers) move from Bold to Semibold. Bold stays available for a heading that needs extra weight. Names (business cards, speaker names) stay Bold.
- brand-rules.md: new line on heading weight.
- Not yet changed: the Zoho Show deck (.pptx) still uses Bold titles.

## 2.4.3 — Nov 2026
- SKILL.md no longer points to the brand site's "Words we use" page, which was removed; the plain-words table stays.
- Brand check and the skill description now include the form-error exception for red (red/100, never a button), matching the 2.4.2 brand rule.

## 2.4.2 — Nov 2026
- Red: besides the main button, red/100 is also allowed for error messages in forms (role/status/error), never as a button. Matches the brand site's Colours, Buttons and Form controls pages.

## 2.4.1 — Nov 2026
- Plain words for marketers: SKILL.md now lists the everyday words from the brand site's "Words we use" page (full logo, main button, light background, shade 100 …), so Claude speaks the same language as the site. Design and file names are unchanged.
- Text XL now has all four weights (Medium, Semibold and Bold added), matching the CDS-2.0 Figma text styles.
- Print minimums written into the rules: body 9 pt, captions and labels 8 pt, contact and legal lines 7 pt, never smaller.
- tokens.json gains a `descriptions` map: a one-line use note for every colour, role, spacing and radius token, the same text as the variable descriptions in the CDS-2.0 Figma file. Values and keys are unchanged.

## 2.4.0 — Nov 2026
- Built on 2.3.2 (the CDS-2.0 audit sync); nothing from 2.3.2 changes.
- Email newsletters: scripts/build_email.py builds email-safe newsletters (600 px, table layout, inline styles, PNG images, preheader, mobile rule) from the CDS newsletter sections — header, title with 3D tile, greeting, tinted bands (blue, violet for AI, green, yellow), item lists, stories, one red CTA, sign-off and social footer — and zips them for any email tool with a preview.
- Email typography exception: Georgia headings and Helvetica Neue body, email only. 3D tile now allowed in email.
- Swatch files: CDS-2.0-print-swatches.ase (official CMYK) and CDS-2.0-screen-swatches.ase (RGB). Handed over when someone asks for brand colours, and with every print PDF.
- Five Phosphor social logos added to the icon set for email footers.

## 2.3.2 — Nov 2026
- Synced with the CDS-2.0 Figma file after the Nov 2026 audit.
- Partner co-branding: partner logo about 0.85× the Creator lockup height (was 0.78×), 0.3× the lockup height between each logo and the divider (was 0.23×), matching Brand · Logo 06.
- Spark pattern: AI-only, in any of the four colour versions.
- Deck: the Zoho Show deck is 45 slides (30 standard + 15 extras); the .pptx also holds divider slide 31, which never stays in a finished deck.

## 2.3.1 — Nov 2026
- Fixed: the plugin failed to load when installed from DX-Marketplace ("conflicting manifests") since 2.0.1. The marketplace entry now uses `strict: true`, so plugin.json and the marketplace skills list work together.
- Plugin description now covers YouTube thumbnails and print (business cards, flyers, roll-up banners, brochures).

## 2.3.0 — Nov 2026
- Brochures: A4 tri-fold (outside and inside sheets, 100/100/97 mm panels, fold marks) and 4-page A4 brochure (cover, inside left, inside right, back), in the official CMYK values with 3 mm bleed. Text is given per page. Matching templates added to Templates · Print in Figma.

## 2.2.2 — Nov 2026
- Removed creator-visual-language. It only pointed to creator-design-system, which already covers web pages, so the plugin now has one skill: creator-design-system.
- Co-brand divider: 2 px grey/140 on light backgrounds (white at 40% on dark), so it reads clearly on the soft meshes.
- No Zoho logo on pieces with the Creator × Partner co-branded lockup (including the Partner YouTube thumbnail), to avoid three logos.
- Web footer: the development team adds the common zoho.com product footer; page drafts show a placeholder band instead of a designed footer.

## 2.2.1 — Nov 2026
- Partner co-branding (Brand · Logo 06): Creator lockup first, thin grey/60 divider, partner logo about 0.78× the lockup height on one line. Used on the Partner YouTube thumbnail and on any partner-topic post given `partner_logo`. Partner thumbnail now also carries the Zoho logo top-right.

## 2.2.0 — Oct 2026
- YouTube thumbnails: Deep dive, Campaign · AI and Customer story · Partner, rendered like the other social templates. Artwork uses the new CDS 3D tile (blue, or violet for AI) with any icon from the CDS set; highlight box, eyebrow, prompt bubble, cut-out photo and customer logo supported.
- Print: business card front and back, A4 flyer and roll-up banner. scripts/render_print.py makes real-size PDFs in the official CMYK values from Foundations · Colour, with 3 mm bleed, crop marks, embedded Zoho Puvi, vector patterns and a working QR code. Designer approval and a printed proof are still required.
- Web: scripts/build_web.py builds responsive page drafts from the Templates · Web sections (nav, hero, features, stats, CTA band, footer) by topic, with a full-page preview and checks (one red button per section, sources for stats). New CDS 2.0 footer; feature cards use the CDS Icon tile.
- Icons now inherit colour correctly when placed on tiles and in web pages.

## 2.1.0 — Oct 2026
- Social, video and email templates: 11 templates in 21 versions (Feature, Quote, Webinar, Landscape, X, Story, Reels cover, Carousel cover and slide, Email header, Video background) exported from the CDS-2.0 Figma file into assets/social/layouts.json.
- scripts/render_social.py fills a template from a brief and renders an exact-size PNG with Zoho Puvi, the gradients, logos and Connect texture; handles topic (default, AI, partner), highlight words, screenshots and speaker photos.
- Built-in brand check: text overflow, collisions, safe area, and a list of samples to replace.
- Rendered social pieces no longer need designer review; YouTube thumbnails still do (their 3D artwork arrives in a later version).

## 2.0.1 — Oct 2026
- Web: hero panel, CTA band, eyebrows and icon tiles now follow the page topic (default, AI, partner), so AI pages no longer get a blue CTA band with a pattern.
- Red rule clarified: one red button per post, slide or email header; on web pages, at most one per section (nav, hero, CTA band). Matches Components · Buttons.
- Added the CDS icon set (318 icons, Regular and Fill: Phosphor plus the CDS custom icons) in one file, assets/icons/icons.json, with scripts/icon.py to get any icon. Kept to one file so the skill stays under the 200-file upload limit.
- One eyebrow colour per web page.

## 2.0.0 — Oct 2026
- Rebuilt on CDS 2.0 (CDS-2.0 Figma file). The v1 product token files are removed.
- Everything a skill needs now lives inside the skill folder, so it works in claude.ai as well as Claude Code (v1's shared design-system folder isn't visible to skills in claude.ai).
- creator-design-system: CDS 2.0 brand rules, tokens (colour, roles, spacing, radius, type, elevation, ten gradients), logos, Shape kit, Connect texture, Zoho Puvi, the 46-slide master deck with build and brand-check scripts.
- creator-visual-language: now a thin web entry point that reads creator-design-system (no duplicated values).
- Social and web: specs and rules included; HTML templates follow in 2.1 (social) and 2.2 (web).
