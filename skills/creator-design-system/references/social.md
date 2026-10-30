# Social, video and email

Every format below is a CDS 2.0 template exported from the CDS-2.0 Figma file into
`assets/social/layouts.json`. Claude never designs these: it fills a template and renders it
with `scripts/render_social.py`, which produces the exact-size PNG and runs the brand check.

## Workflow

1. **Get the brief:** channel, the one message, Light or Bold, topic (default, AI or partner),
   and anything real: product screenshot, speaker names, roles and photos, date and time.
   Ask once for what's missing; never invent facts.
2. **Pick the template and version** from the table below.
3. **See its text slots:** `python scripts/render_social.py slots <template>`.
4. **Write brief.json** (format at the top of `scripts/render_social.py`): template, version,
   topic, text per slot, tag, and image paths. Mark one or two highlight words with **double
   asterisks**.
5. **Render:** `python scripts/render_social.py brief.json <name>.png`.
6. **Fix every error** the check reports (text too long, collisions, outside the safe area) by
   shortening the text — never by changing sizes or positions — and render again.
7. **View the PNG**, then hand it over with the "To replace before publishing" list in plain
   language.

## Templates

| Template | Size (px) | Versions | Use it for |
| --- | --- | --- | --- |
| `feature` | 1080 × 1080 | product-light, product-bold, statement-light, statement-bold | Feature or launch post; "statement" when there's no screenshot |
| `quote` | 1080 × 1080 | light, bold | Customer quote with a cut-out photo |
| `webinar` | 1080 × 1350 | light, bold | Webinar or event with two speakers |
| `landscape` | 1200 × 628 | light, bold | LinkedIn or Facebook link post |
| `x` | 1600 × 900 | light, bold | X post |
| `story` | 1080 × 1920 | light, bold | Instagram, Facebook or LinkedIn story |
| `reels-cover` | 1080 × 1920 | default | Reels and Shorts cover |
| `carousel-cover` | 1080 × 1350 | default | First slide of a carousel |
| `carousel-slide` | 1080 × 1350 | light, bold | Inside slides: render one per slide, numbered |
| `email-header` | 1200 × 400 | light, bold | Newsletter and campaign email header |
| `video-background` | 1920 × 1080 | default | Background behind a talking-head video, with lower third |

**Topic** changes only the background and accents, following `brand-rules.md`: AI gives the
soft AI mesh (or the AI gradient on Bold), a violet tag and violet highlights; partner gives the
partner mesh and violet highlights. Use AI or partner only when the content is about them.

**Images:** a product screenshot replaces the drawn sample in the card. Speaker photos must be
transparent cut-out PNGs (person only, no background). If none are given, the template keeps
neutral placeholders and the check lists them.

**Carousels:** render the cover, then one `carousel-slide` per point with "Slide number" (01,
02…) and "Page counter" (02 / 06…), then combine the PNGs into a PDF, one page per slide.

## YouTube thumbnails

The five thumbnail versions (Campaign · AI, Deep dive, Explainer, Customer story · Partner,
Learning series · AI) use custom 3D artwork and are not in the renderer yet. Until they are,
build them from these specs with `design-system/tokens.css` and label them **Draft — designer
review**: 1280 × 720, 48 px safe area with the bottom-right video-length corner clear,
Creator lockup top-left, Zoho logo top-right in a white tab, headline 80–96 px with one
highlighted phrase, an eyebrow of at least 28 px.

## Who publishes

Posts, stories, carousels, email headers and video backgrounds rendered with no errors can be
published by the marketer once every sample is replaced. YouTube thumbnails, web pages and
print go to a designer first.
