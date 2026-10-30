# creator-design-skills

Claude plugin for Zoho Creator marketing, built on CDS 2.0.

## Install

In Claude Code:

```
/plugin install creator-design-skills --marketplace Abhinaya-6360/DX-Marketplace
```

- `skills/creator-design-system/` — the brand system and all assets (start here)
- `skills/creator-visual-language/` — web entry point, reads creator-design-system

Source of truth: the CDS-2.0 Figma file. When CDS changes, re-export tokens and assets from
Figma into `skills/creator-design-system/design-system/` and `assets/`, update the
references, bump the version and note it in CHANGELOG.md.
