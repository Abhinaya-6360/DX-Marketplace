# Changelog

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
