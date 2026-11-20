# Web pages (zoho.com/creator)

> Web output is a **reviewable HTML draft** (plus a preview PNG) that should already look
> designed: marketers can share it and use it to brief the web team. It is never production code.

The goal: a marketer who isn't a designer asks for a page and gets one that looks like the
CDS 2.0 example pages. Claude gets there by **starting from a recipe** and **only using the
sections below**: never invent a layout, a colour, a size or a font.

## Workflow

1. **Brief.** Ask once for: what the page is for, the audience, the one message, the topic
   (default, AI or partner), the main action (the red button label), real numbers with sources,
   quotes with names, and any screenshots, photos or logos. Missing facts stay as samples.
2. **Pick a recipe** from `assets/web/recipes/` (table below). Copy it to page.json.
3. **Adapt it:** keep the section order that tells the story (hero → proof → what it does →
   how it works → proof → action → questions). Remove sections you have nothing real for; add one
   from the catalogue only when the story needs it. 6–10 sections is the sweet spot.
4. **Write the copy** for every field, in plain words. Mark one or two highlight words per
   headline with `**double asterisks**`.
5. **Build:** `python scripts/build_web.py page.json <name>.html --preview <name>.png`
6. **Check:** `python scripts/check_system.py <name>.html --topic <topic>`. Fix everything.
7. **Look at the preview** (split it into parts if it's long). Fix crowding, empty sections,
   long headlines, repeated section types next to each other, then rebuild.
8. **Hand over** the HTML and PNG with the "To replace" list in plain language, and the System
   check line. Web pages go to the web team before they go live.

## Recipes (assets/web/recipes/, built from the Figma example pages)

| Recipe | Use it for | Sections |
| --- | --- | --- |
| `landing` | A simple product or feature page | hero split → logos → features → testimonial → CTA → FAQ |
| `ai-product` | An AI product or AI feature (topic ai) | hero cards → logos → comparison → bento → accordion steps → resources → testimonial → CTA → FAQ dark |
| `platform-overview` | A platform or capability overview | hero chips → orbit (AI agent bot) → platform layers → stacked cards → big-text tabs → dark list → CTA |
| `deployment` | A solution page with a sign-up form | hero form → options → dark benefit cards → steps → side tabs → CTA → FAQ dark |
| `erp-extension` | Extending a system (ERP, CRM…) | hero diagram → logos → features → dark side tabs → testimonial → CTA → FAQ |
| `industry` | An industry page (education, healthcare…) | hero centred → bento → big-text tabs → photo accordion → testimonial → CTA → FAQ |
| `partner-hub` | Partner or customer stories hub (topic partner) | hero centred with numbers → story cards → large quote → light CTA |
| `partner-story` | One partner or customer story | hero photo → timeline → testimonial → story cards → light CTA |
| `event` | Event, hackathon or webinar | hero event with countdown → brief cards → stages timeline → FAQ → dark CTA |
| `press` | Press and news | hero centred → news cards → light CTA |

## Section catalogue (Templates · Web in the CDS-2.0 Figma file)

Every section takes `eyebrow` (small label), `title` (with `**highlight**`) and `lead` unless noted.

| type | layout / tone | Figma template | Fields |
| --- | --- | --- | --- |
| `nav` | — | Nav | `links`, `primary` (red), `secondary` |
| `hero` | `split` (default) | Hero, Split hero · Product screenshot | `tag`, `headline`, `body`, `primary`, `secondary`, `screenshot` |
| `hero` | `centred` | Hero · Centred, Centred with search | `tag`, `headline`, `body`, `stats` (up to 3), optional buttons |
| `hero` | `screenshot` | Hero · Product screenshot (centred) | as split; screenshot below, full width |
| `hero` | `diagram` | Hero · Product diagram | `nodes` (4: icon, label), `cards` (2: title, text) |
| `hero` | `form` | Hero · Sign-up form | `fields`, `form_title`, `primary` (Submit), `consent` |
| `hero` | `event` | Hero · Event, Event with trophy and countdown | `meta`, `badge`, `headline`, `year`, `body`, `date`, `place`, `visual`, `countdown` |
| `hero` | `video` | Hero · Story with video | `logo`, `eyebrow`, `headline`, `video_still` |
| `hero` | `cards` | Hero · AI with app cards | `headline`, `body`, `primary`, `note`, `cards` (3: title, icon, text) |
| `hero` | `chips` | Hero · Centred with floating chips | `chips` (up to 6: icon, label) |
| `hero` | `photo` | Hero · Story with photo | `photo`, `eyebrow`, `headline`, `body`, `facts` |
| `logos` | — | Logo wall, Stats and logos strip | `title`, `stats` (value, label, source), `logos` (image paths) |
| `features` | — | Feature grid | `cards` (2–6: icon, title, text) |
| `benefits` | blue band | Why choose (benefit cards) | `cards` (icon, title, points) |
| `bento` | — | What you can build, Bento grid | `cards` (title, text, image) |
| `options` | — | Options grid | `options` (first is highlighted: icon, title, text, points), `note` |
| `stacked` | — | Stacked feature cards | `cards` (title, text, points, stat, stat_label) |
| `resources` | — | Resource cards | `cards` (title) — link cards on CDS gradients |
| `tabs` | `side` · `bigtext` · `top`; `tone: dark` | Side tabs, Big-text tabs, Top tabs | `tabs` (icon, label; the first also title, text, points, image) |
| `accordion` | `steps` · `photos` · `side` | How to build, Photo accordion, Side-by-side accordion | `items` (first is open: steps / photo / text) |
| `steps` | `vertical` (default) · `timeline` | Getting started, Story timeline | `items` (title, text, tags / when) |
| `comparison` | — | Comparison (us vs them) | `them`, `us` (label, points, image) |
| `darklist` | list · `cards` | Two-column list · dark, Benefit grid · dark | `items` (icon, title, text) |
| `columns` | — | Three columns + banner | `columns` (title, items), `banner` |
| `platform` | — | Platform layers | `layers` (icon, label), `blocks` (title, text) |
| `orbit` | — | Agent lifecycle · dark (AI agent bot) | `nodes` (6: icon, label), `steps` (title, text, image) |
| `stories` | — | Story cards grid | `cards` (logo, tag, title, text) |
| `stats` | — | Stats | `stats` (value, label, source) |
| `testimonial` | `card` · `large` | Testimonial, large quote | `quote`, `name`, `role`, `photo`, `logo` |
| `faq` | `tone: light` · `dark` | FAQ | `title`, `items` (q, a) |
| `cta` | `band` · `light` · `dark` | CTA band, CTA · centred light, CTA · dark centred | `headline`, `body`, `primary`, `secondary` |
| `footer` | — | (dev team) | placeholder band only; never design a footer |

## Making it look good (what the examples do)

- **Rhythm:** alternate light and dark or tinted sections; never two dark sections or two card
  grids in a row. One full-colour band (CTA) near the end.
- **One hero, one CTA band.** Every page ends with a CTA, then FAQ if there are real questions.
- **Headlines:** 3–9 words, one or two highlighted words. Leads: one sentence.
- **Cards:** 3 per row (2 or 4 for numbers). Titles 2–5 words, text one line.
- **Lists:** 2–4 points. Tabs: 3–6. FAQ: 3–8 questions.
- **Pictures:** use the marketer's real screenshots and photos; otherwise the grey "(replace)"
  slots stay and go on the handover list. Never generate product screens or photos of people.
- **AI pages** (topic ai): violet only as an accent (highlights on light, tags, ai-sparkle tiles);
  the bold sections use the AI gradient with yellow highlights. The **AI agent bot**
  (`orbit` section) is for dark backgrounds only, one per page.

## Topic colours (applied for you)

| Topic | Light hero / sections | Bold sections | Highlights |
| --- | --- | --- | --- |
| default | soft blue, light background · Blue | blue 100 with the faint Connect texture | blue 100 (yellow on dark) |
| ai | soft violet, light background · AI | AI gradient, no pattern | violet 100 on light, yellow on dark |
| partner | light background · Partner | Midnight with the faint texture | violet 100 on light, yellow on dark |

## Rules

- **Red is only for the main button**: at most one red button per section (nav, hero, CTA).
  Everything else interactive is blue.
- Only CDS icons (`python scripts/icon.py list` shows the name and what each is for).
- The Creator logo is the SVG in `assets/logos/`, never typed text.
- Stats need a source; otherwise keep the sample and flag it.
- Live zoho.com pages may still use pre-CDS 2.0 colours. Drafts follow CDS 2.0.
