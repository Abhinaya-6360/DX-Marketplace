# Changelog

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
