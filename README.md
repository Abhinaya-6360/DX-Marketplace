# 🎨 DX-Marketplace

> Build better UI. Faster. With AI.

An AI-powered **design intelligence layer** for Claude — enabling structured
thinking, scalable systems, and consistent visual design across Creator
products.

---

## ⚡ Why this exists

Design today is:

* ❌ Inconsistent across teams
* ❌ Hard to scale
* ❌ Dependent on individual thinking

**DX-Marketplace solves this by turning design expertise into reusable,
AI-powered skills built on the Creator Design System (CDS).**

---

## 🧠 What you get

A modular set of Claude skills that help you:

* Think like a senior product designer
* Enforce CDS tokens, components, and accessibility automatically
* Build scalable design systems
* Generate UI patterns aligned with the Creator visual language
* Standardize design decisions across teams

---

## 🎯 Core Skills

| Folder | Skill name | What it does |
| --- | --- | --- |
| `skills/creator-design-system/` | `creator-design-system` | Enforces strict CDS token / component / accessibility usage from the local design system. |
| `skills/creator-visual-language/` | `creator-visual-language` | Applies the Creator visual language: Chrome patterns, composition, brand voice. |

---

## 🚀 Installation

### Option A — Claude Code plugin marketplace

```
/plugin marketplace add Abhinaya-6360/DX-Marketplace
/plugin install creator-design-skills
```

### Option B — Clone directly

```
git clone https://github.com/Abhinaya-6360/DX-Marketplace
```

Everything you need — skills, CDS tokens, components, accessibility audit —
is in this single repo. No submodule setup needed.

---

## ⚙️ Usage

These skills **auto-activate** based on how you describe your task. There
are no slash commands — just describe what you want and Claude matches the
right skill from its description.

Example prompts that activate each skill:

* `creator-design-system` → *"Build a dashboard UI using CDS tokens."*
* `creator-visual-language` → *"Apply the Creator Chrome visual language to this landing page."*

---

## 🏗️ Architecture

```
DX-Marketplace/
├── .claude-plugin/
│   └── marketplace.json              # Plugin manifest
├── design-system/                    # CDS design system (tokens, components, accessibility)
│   ├── DESIGN.md                     # Loader rules and AI behaviour
│   ├── README.md                     # Design system documentation
│   ├── LICENSE
│   ├── index.json                    # Manifest of every token file
│   ├── foundations/                  # Spaces, grids, colours, typography, elevation, radius
│   ├── components/                   # CTA buttons (more components to come)
│   └── accessibility/                # WCAG 2.2 AA rules + 47-check audit
├── skills/
│   ├── creator-design-system/
│   │   ├── SKILL.md
│   │   └── products/
│   │       └── creator.md
│   └── creator-visual-language/
│       ├── SKILL.md
│       └── references/
│           └── creator-chrome.md
├── LICENSE
└── README.md
```

---

## 💼 Real-world use cases

**Designers** — structured UI thinking, faster decisions, consistent systems.
**Marketers** — landing page clarity, conversion-focused layouts.
**Engineers** — pull tokens directly into CSS variables, Tailwind config, or
Style Dictionary.
**Teams** — standardize design language across Creator products.

---

## 🔥 Vision

This is a foundation for:

* 🧠 AI-powered design systems
* 🏗️ Prompt-driven UI builders
* 🔄 Design → Code automation
* 🛡️ Brand consistency engines

---

## 🧩 Roadmap

* ✅ Core CDS tokens (spaces, grids, colours, typography, elevation, radius)
* ✅ CTA button component
* ✅ WCAG 2.2 AA audit checklist
* 🔜 More component specs (inputs, cards, navigation)
* 🔜 Product themes (`design-system/themes/{product}.json`)
* 🔜 Theme factory skill
* 🔜 UI thinking skill
* 🔜 Design QA automation

---

## 👨‍💻 Creator

**Abhinaya** — Design × AI × Product Systems
GitHub: <https://github.com/Abhinaya-6360>

---

## 🤝 Contribute

Want to expand this system? You can add:

* New design skills
* New component specs
* New product themes
* Automation workflows

See `CONTRIBUTING.md` (coming soon) for guidelines.

---

## ⭐ Support

If this helps your workflow, ⭐ the repo and share it with your team.

---

## 📜 License

MIT — see [LICENSE](./LICENSE).