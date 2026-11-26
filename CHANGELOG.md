# Changelog

## 2.8.6 — Nov 2026
- Illustrations (Figma Guides · Imagery › 06 · Illustrations): Claude draws flat illustrations in the CDS house style for whatever the content is about; the six references (order to cash, integrations, approvals, growth, dashboards, extending a legacy system) are examples of the style, not a fixed set. Blues and greys carry the picture; other CDS colours are small accents under 8% of the picture (yellow highlights, green success, red only for an error, violet only on AI), measured by `illustration.py check`. New `scripts/illustration.py` (drawing helpers, `check`, `show`), six references in `assets/illustrations/style/`, and `references/illustrations.md` (style, picture order, how to draw and place one). The Creator diamond behind a picture is optional. Never people drawn in code, logos, words or a real-looking Creator screen.
- Design-lead pass (SKILL.md): alignment on one axis, the picture filling its zone, balanced headlines, one focal point; content never changes. Feature gets `illustration-light` / `illustration-bold` (Figma Template/Social post · Feature › Layout=Illustration): centred tag, headline and text over a full-width picture zone; a Feature product brief with an illustration switches to it. On other templates, text above a centred illustration is centred automatically. Headlines and centred text are balanced (no lone last word); the illustration's ground shadow becomes a faint glow on Bold backgrounds.
- Breathing room: render_social keeps at least 40 px (4% of the width) between any text and a screenshot, illustration, tile, photo or card. It moves or shrinks the picture, or narrows text beside it, and reports what it can't fix ("Too close"). brand-rules.md and SKILL.md state the rule for every format.
- Social tags no longer look like buttons: three label styles from the Figma Tag set (new Chip, Outline and Eyebrow styles in Blue, Violet and White), chosen by the layout: soft chip by default, eyebrow on statement layouts, outline over photos and busy backgrounds (Webinar, Reels covers); white on Bold, AI and dark backgrounds; `"tag_style"` overrides. Smaller than the old solid block, uppercase with a little letter spacing.
- Stock illustrations are allowed when flat, licensed and recoloured to CDS. `check_system.py <picture>.png` lists colours outside CDS as IMAGE NOTES with the nearest CDS colour (skin and hair can stay natural).
- render_social.py: `"illustration"` puts a CDS illustration (SVG) or a stock illustration (PNG) in the picture zone, with no card frame: cropped to the drawing and scaled to fill the full width between the text margins (clear of text beside it and of the logos), sitting on the zone's bottom edge; it is listed for design review. check_system reports NEW ILLUSTRATION(S) for review and flags text, embedded pictures, gradients or blur inside an illustration.
- Icons: `python icon.py find <word>` searches names and what-it's-for lines; SKILL.md says to name only icons that exist (a test suggested `invoice`, `order` and `workflows`, which aren't in the set: use `receipt`, `package`, `flow`).
- Layouts adapt to the content, in every collateral (brand-rules.md, SKILL.md): with more or less text than the sample, the layout re-spaces and grows into free space first, then steps the type down at most two sizes on the same scale (never under the minimum sizes), and only then asks for shorter text, after asking the person. Each change prints as a `layout:` line.
  - Social (render_social.py): text above a picture pushes it down or lets it move up (the picture keeps 0.6–1.35× its size); text beside a picture flows down its column; short copy beside a picture closes up as one group centred on the picture; text beside a picture is set clear of it before it wraps. Then the headline, then the supporting text, steps down one or two CDS sizes. A video lower third keeps its own place below the safe area. Spacing rhythm: tag (or eyebrow) to headline and headline to supporting text or date are 0.4 × the headline size in every template and tone (they were 16–49 px, and X Light and Bold differed); text to the picture below is 40 px to 6% of the width, and a picture at its largest size sits centred in the room left; footer items (page counter, swipe cue) stay put.
  - Decks (build_deck.py, check_deck.py, deck_common.py): wraps are measured with Zoho Puvi; a box grows into free space below and the blocks stacked under it move down; inside a card the card keeps its padding so a row of cards stays equal; then the type steps down the deck's sizes (never under 12 pt); titles keep to three lines; less text than the sample closes up the blocks below it, so a title keeps its normal gap to its paragraph. check_deck makes the same changes in memory and lists them under To check; it errors only when text still doesn't fit. The template's own sample always fits.
  - Print (render_print.py): the same flow, plus a block low on the page (a back-cover heading) can rise into the space above; buttons and list items step down before they're called too long; less text closes up the blocks below; a heading in a colour band (A4 flyer) sits at the band's foot, close to the paragraph after it; body text never goes under 9 pt, labels and contact lines don't step.
  - Web and email pages are fluid HTML already; the rule is documented for them too.
- Fix: on slides 27 and 37 a text slot and the page number share an id; build_deck and check_deck now use the text slot (as deck_inventory lists it) instead of overwriting the page number.
- Restored from the 2.8.5 merge: icon fonts from other sets (Font Awesome, Material, Bootstrap Icons, Ionicons, Glyphicons) are flagged; the piece type (`kind`) uses the 2.8.4 email detection, so emails are recognised in the language check too.

## 2.8.5 — Nov 2026
Fixes from the pre-rollout test (all formats, 12 violation cases, real-world requests), for sharing with the whole Zoho Creator group.
- check_system.py: icons from other sets (Font Awesome, Material…) are now flagged whatever their format (any quote style or grid size); the illustration assets count as CDS artwork.
- check_system.py: one main button — more than one red button in a post, slide or email, or in one web section, is flagged.
- check_system.py: an outside colour on a button now says the main button is always red/90.
- Languages: Zoho Puvi is Latin only. Tamil, Devanagari, Arabic (bundled Noto Sans, assets/fonts/noto/) and Japanese, Chinese, Korean (Noto Sans CJK) render in social, video, YouTube, decks and newsletters, Arabic right to left, and every such piece gets a FONT NOTE for design review. Other scripts are flagged. Non-English print stops (the print tool can't join these letters); non-English web drafts are flagged (the web team localises zoho.com).
- render_social.py: an AI or partner version sets its topic automatically, and rendered pages carry it, so the checker no longer asks "is this AI?" for them.
- render_social.py: speaker names, roles and companies that don't fit the Webinar card are flagged.
- Carousel cover: headline plus one supporting line (Figma Templates · Social and video, Bold and AI). social.md: Stories and Reels covers keep their top and bottom empty for the app's buttons.

## 2.8.4 — Nov 2026
- check_system.py recognises an email page on its own, whatever the file name (build_email's new `cds-template` marker, the email-client meta tag, or a table-based email layout), so the Georgia and Helvetica Neue email exception applies without `--email`. A newsletter saved as index.html no longer fails on its fonts. Web pages that use Georgia are still flagged.
- build_email.py marks its output with `<meta name='cds-template' content='email'>`.

## 2.8.3 — Nov 2026
- icons.json: every icon now has a what-it's-for line (363 of 363; `python scripts/icon.py list` shows them), so Claude picks icons by meaning. The 296 Phosphor lines come from the brand site and are now in the CDS-2.0 Figma icon descriptions too, so Figma, skill and site match word for word. 25 lines were tidied on the way (UK spelling, clearer wording); Brain, MagicWand and Sparkle now say they are not the AI icon (use ai-sparkle).

## 2.8.2 — Nov 2026
- icons.json: what-it's-for lines match the CDS-2.0 Figma icon descriptions word for word (Figma wins; the brand site follows it). Changed: ai-sparkle (agents and bots included; violet tile on AI content), robot (only for literal robots, e.g. hardware or robotics), portal-loan-application (form with a coin). Figma Icon/AISparkle description updated to the same wording.
- Deck: slide 46 Questions speaker note rewritten for the new slide (no speaker details or QR code any more). deck-slots.json regenerated.

## 2.8.1 — Nov 2026
- check_system.py no longer flags the CDS 3D tile on AI pieces. The "solid violet background on a card, panel or button" rule (2.7.1) caught the tile's violet bevel layers (violet/150 and violet/130, 200 px), so the YouTube `campaign-ai` thumbnail failed the plugin's own check. Everything inside an element marked `data-el="tile"` is now skipped by that rule (brand-rules.md allows the violet tile for AI content); real violet cards, panels and buttons are still flagged.
- build_email.py: the flat icon tile is marked `data-el="tile"` too (the 3D hero and story tiles already were, through render_social's tile3d), so AI newsletters with a violet `hero_tile` pass.
- check_system.py: the HTML walker's element stack is now per check (it was shared between checks in one run).

## 2.8.0 — Nov 2026
Deck infographics and web page templates, matching the CDS-2.0 Figma file (Templates · Deck and Templates · Web).
- Deck: 13 infographic slides added as editable slides 47–59 (Figma I01–I13): stepped stats, rating gauge, cost breakdown, SWOT, data table, progress rings, overview with chart, three points as bubbles, KPI dashboard, pricing plans, bar chart with a highlight, partners, matrix. Charts and the table are real PowerPoint charts and tables, editable in Zoho Show. The deck is now 58 slides plus the divider.
- Slide 44 Comparison table rebuilt as an editable five-column table (Zoho Creator against spreadsheets, custom code and point tools; Yes / Partly / No), and slide 46 Questions redesigned (light, big blue question mark, no contact details), matching Figma E13 and E15.
- deck.md: infographic list, outlines that use them (new: Business case or QBR), and rules for their numbers, prices, logos and photos. deck-slots.json regenerated; check_deck.py asks to confirm the numbers on each infographic.
- Web: build_web.py now builds pages from the full CDS 2.0 section library (new scripts/web_sections.py, ~40 sections from Templates · Web: heroes, features, bento, tabs, accordions, steps, comparison, platform, orbit with the AI agent bot, stories, stats, testimonials, FAQ, CTA). Ten page recipes in assets/web/recipes/ (landing, ai-product, platform-overview, deployment, erp-extension, industry, partner-hub, partner-story, event, press) so anyone can get a page that looks designed. web.md rewritten: workflow, recipes, section catalogue, how to make it look good.
- AI agent bot illustration (assets/illustrations/ai-agent-bot.svg) for dark backgrounds on AI pieces, one per piece.
- icons.json: what each custom and new icon is for; `icon.py list` shows it.
- check_system.py: contrast check ignores see-through backgrounds (no false failures on tinted cards).

## 2.7.1 — Nov 2026
Fixes from colleague testing and the 19 Nov Figma decisions (CDS-2.0 file, Foundations · Colour, Brand · Patterns, Templates · Social and video).
- AI colour: blue stays the primary colour; on AI pieces violet is an accent only (highlight words on light backgrounds, the AI tag, ai-sparkle and its tile, soft glows). Never violet cards, panels, buttons or solid violet backgrounds. Bold AI background = gradient/ai, light = mesh-soft-ai. Partner content unchanged.
- On the AI gradient all text is white and highlight words are yellow/100 (they were violet and couldn't be read). render_social.py updated; web stat numbers are always blue/100.
- AI icon: ai-sparkle for anything AI, agents and bots included; robot only for a literal robot. Icons sit in a tile beside a heading, never after a sentence.
- Carousels: carousel-cover and carousel-slide gain an `ai` version (AI gradient, no texture, yellow highlights), matching Figma Tone=AI. social.md: always build carousels from the templates, no custom illustrations, and the page counter counts the cover as page 1.
- check_system.py flags violet text on the AI gradient, solid violet cards/panels/buttons, the robot icon on AI pieces (briefs and HTML).
- Patterns subtler: Connect texture 12% on light (was 22%), 8% on Midnight and blue (was 12%); web hero and CTA band texture 8% (was 35% / 12%). Behind text a pattern is always subtle (faint texture or Calm); full-strength patterns only on panels with no text. Deck patterns unchanged.

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
