# creator-design-skills

Claude plugin for Zoho Creator marketing, built on CDS 2.0.

## Install

In Claude Code:

```
/plugin install creator-design-skills --marketplace Abhinaya-6360/DX-Marketplace
```

- `skills/creator-design-system/` — the brand system, all assets and every format (decks, social, YouTube, web, print)

Source of truth: the CDS-2.0 Figma file. When CDS changes, re-export tokens and assets from
Figma into `skills/creator-design-system/design-system/` and `assets/`, update the
references, bump the version and note it in CHANGELOG.md.
