# Decks for Zoho Show

Claude never designs slides. It builds every deck from
`assets/deck/CDS-2.0-Creator-Deck-All-Slides.pptx` — the same 46 slides marketers have in
Zoho Show — so the result is on-brand and editable after import.

## Workflow

1. **Get the brief.** Audience, goal, the one message, length (minutes or slides), date,
   presenter, and any real numbers, quotes, screenshots or photos. Ask for what's missing
   in one message; don't guess facts.
2. **Pick an outline** below and adjust it to the brief. Keep the standard flow:
   problem → product → proof → close. One cover, one close.
3. **Read the slots.** `references/deck-slots.json` lists every slide's text slots with their
   shape id, sample text and max characters. For the slides you chose, write the new text
   for each slot, under its max. Skip a slot only if its sample still fits the story.
4. **Write plan.json** (format in `scripts/build_deck.py`) with slides in order, the text by
   shape id, and a one- or two-sentence talk track per slide.
5. **Build:** `python scripts/build_deck.py plan.json <name>.pptx`
6. **Check:** `python scripts/check_deck.py plan.json`. Fix every error and rebuild.
7. **Hand over** the .pptx with: how to import (Zoho Show → Import), and the "To check"
   list from the check, in plain language, grouped by slide.

Run the scripts from the skill's `scripts/` folder (they find the source deck themselves).
To check the look, render slides to images with LibreOffice (`soffice --headless
--convert-to pdf`) and view them.

## The slides

Standard 1–30 (in order): 1 Cover · 2 Agenda · 3 Section divider · 4 Full-bleed statement ·
5 Problem · 6 Problem and solution · 7 Overview (six capabilities) · 8 Three ways to start ·
9 Text + image · 10 Timeline (five steps) · 11 Roadmap (by quarter) · 12 Feature list ·
13 Video · 14 Callouts (parts of a screen) · 15 Platform orbit · 16 AI (Zia) — AI decks only ·
17 Mobile app · 18 Integrations · 19 Security and compliance · 20 Three points (numbers) ·
21 Bar chart · 22 Donut chart · 23 Team · 24 Testimonial · 25 Case study · 26 Logo wall ·
27 Pricing · 28 Demo · 29 Next steps · 30 Thank you (closing, Zoho logo).

31 is the divider between standard and extras. It never stays in a finished deck.

Extras 32–46: 32 Event opener (replaces the cover) · 33 Title on photo (replaces the cover) ·
34 Section divider · dark · 35 Solution (three pillars) · 36 Use cases · 37 Before and after ·
38 Product · Midnight · 39 Screenshot on pattern · 40 Layers · 41 Line chart · 42 ROI ·
43 Funnel · 44 Comparison table · 45 Pull quote · 46 Questions (closing).

## Story outlines (defaults — adjust to the brief)

| Deck | Slides, in order |
| --- | --- |
| Product or feature launch | 1 · 5 · 6 · 12 or 14 · 8 · 20 or 42 · 24 · 28 · 29 · 30 |
| Customer pitch | 1 · 2 · 5 · 6 · 7 · 15 · 18 · 19 · 24 or 25 · 26 · 27 · 29 · 30 |
| Webinar or event talk | 32 · 2 · 3 · 4 · 9 · 10 · 13 · 23 · 46 |
| Internal update | 1 · 2 · 11 · 21 or 22 · 41 · 29 · 30 |
| Partner (Powered by Zoho Creator) | 1 · 5 · 35 · 36 · 25 · 45 · 28 · 30 |

Add 16 (AI) only to decks about AI. Use 3 (or 34 on dark decks) before each section in
decks longer than about 12 slides.

## Deck rules

- Text: stay under each slot's max; shorten, never shrink the font, never add text boxes.
- Colour: theme colours only. Red only on the main call to action. Violet only for AI and
  partner content.
- Numbers on 5, 20, 24, 42, 43 and charts: use only numbers the marketer gave, with a source.
  Otherwise leave the sample and flag it.
- Charts: 22 and the table on 44 are editable in Show. The bars on 21 and the lines on 41 are
  shapes; resize them only if asked, otherwise flag them.
- Samples to flag: "Photo (replace)" images, product screens drawn with shapes (8, 12, 14,
  17, 28, 38, 39), partner and customer logos (18, 25, 26), prices (27), certifications (19),
  presenter details (1, 30, 46).
- Each source slide can be used once. If the story needs a second copy, tell the marketer to
  duplicate it in Show.
