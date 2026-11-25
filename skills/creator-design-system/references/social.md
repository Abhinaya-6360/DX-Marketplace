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
6. **The layout adapts to the content.** Don't move or resize things by hand: the renderer does
   it like a designer would, and prints each change as a `layout:` line. More text than the
   sample: text above a picture pushes the picture down (it shrinks a little to keep its place),
   text beside a picture flows down its column, and if there still isn't room the headline (then
   the supporting text) steps down one or two CDS sizes. Less text: the picture moves up, or the
   text closes up as one group centred on the picture. **Spacing rhythm**, the same in every
   template and tone: tag (or eyebrow) to headline, and headline to the supporting text or date,
   0.4 × the headline size (32 px for an 80 px headline), measured on the letters; text to the
   picture below it at least 40 px and at most 6% of the width (65 px on a 1080 px post). A
   picture that has reached its largest size sits centred in the room left. **Fix any error that's left** (text too
   long, collisions, outside the safe area) by shortening the text, after asking the person, and
   render again.
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
| `reels-cover` | 1080 × 1920 | default | Reels and Shorts cover (the empty top and bottom are for the app's buttons and captions — keep them clear) |
| `carousel-cover` | 1080 × 1350 | default (Bold), ai | First slide of a carousel: headline plus one supporting line |
| `carousel-slide` | 1080 × 1350 | light, bold, ai | Inside slides: render one per slide, numbered |
| `email-header` | 1200 × 400 | light, bold | Newsletter and campaign email header |
| `video-background` | 1920 × 1080 | default | Background behind a talking-head video, with lower third |

**Topic** changes only the background and accents, following `brand-rules.md`: AI gives the
soft AI mesh with a violet tag and violet highlights on Light, or the AI gradient on Bold with white
text and **yellow** highlights (never violet text on the gradient); partner gives the partner mesh
and violet highlights. Violet is an accent only. Use AI or partner only when the content is about them.

**Images:** a product screenshot replaces the drawn sample in the card. Speaker photos must be
transparent cut-out PNGs (person only, no background). If none are given, the template keeps
neutral placeholders and the check lists them.

**Stories and Reels covers** leave the top and bottom empty on purpose: the app puts its
buttons, profile and reply bar there. Never fill those bands; if a marketer asks why it looks
empty, say so.

**Carousels:** always build from `carousel-cover` and `carousel-slide` (AI news and stories: the
`ai` version of both). Render the cover, then one `carousel-slide` per point with "Slide number" (01,
02…) and "Page counter" (02 / 06…), then combine the PNGs into a PDF, one page per slide. The page
counter counts the cover as page 1, so point 01 sits on page 02; tell the marketer this. No one-off art
in other styles (boarding passes, badges, mascots): the middle slot is a product screenshot or a CDS
illustration (`references/illustrations.md`). Icons only
in tiles, never after a sentence.

**Tags (labels like NEW, GUIDE, LIVE WEBINAR)** never look like buttons. Three styles (Figma Tag ›
Chip, Outline, Eyebrow), chosen for you by the layout: the soft **chip** by default; the **eyebrow**
(small spaced capitals, no box) on text-led statement layouts; the thin **outline** over photos and
busy backgrounds (Webinar, Reels covers, anything with a speaker or customer photo). On Bold, AI and
dark backgrounds they're white. Override with `"tag_style"` only if the design clearly needs it.

**Illustrations:** pass `"illustration"` instead of `"screenshot"`. Feature product versions switch to
`illustration-light` / `illustration-bold` (Figma Layout=Illustration: centred tag, headline and text
over a 920 × 324 picture zone); on other templates the text above a centred illustration is centred
for you. Headlines are balanced so no line ends on a lone word.

## YouTube thumbnails

`youtube` (1280 × 720) has three versions, rendered like every other template:

| Version | Use it for | Slots and images |
| --- | --- | --- |
| `deep-dive` | Feature deep dives, how-tos (Midnight) | Eyebrow, Headline, Highlight (yellow box); `icon` on the front tile |
| `campaign-ai` | AI campaigns (soft AI mesh) | Headline with **highlighted** words, Prompt (the chat bubble); `icon` and `icon2` on the tiles |
| `customer-story-partner` | Partner and customer stories (partner mesh) | Quote with **highlighted** words, Name, Role; `photo` (cut-out), `partner_logo` (shown in the Creator | partner co-branded lockup) |

The artwork uses the CDS **3D tile** (Brand · Shapes): blue by default, violet only for AI.
Pick tile icons from `scripts/icon.py list` that match the topic (for example `star`,
`shield-check`, `flow`, `chart-bar`, `users-three`). Keep the video-length corner (bottom
right) clear — the templates already do.

## Who publishes

Everything rendered here with no errors — posts, stories, carousels, email headers, video
backgrounds and YouTube thumbnails — can be published by the marketer once every sample is
replaced. Web pages and print go to a designer first.
