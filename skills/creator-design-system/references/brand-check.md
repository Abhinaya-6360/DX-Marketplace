# Brand check — before every handover

Run this on anything you made, whatever the format. For decks, `scripts/check_deck.py`,
and for social, video and email, `scripts/render_social.py`, do the mechanical part; still
read the list below.

## Must pass (fix before handing over)

1. **Size**: exact pixel size of the template (social, video, email) or 1920 × 1080 slides.
2. **Safe area**: text, logos and the CTA sit inside the template's safe area.
3. **Red**: only on main calls to action; one red button per post, slide or email header, and at most one per section on web pages.
4. **Violet**: present only if the topic is AI or a partner.
5. **Background**: chosen from the table in `brand-rules.md`; no pattern behind faces or on
   AI or Glow gradients.
6. **Logos**: Creator lockup unchanged and in the right version for the background; Zoho logo
   about half its width, in an allowed position; customer logos in their own colours.
7. **Type**: Zoho Puvi, text styles from tokens, readable sizes; nothing overflows its slot.
8. **Icons**: from `assets/icons/icons.json` only (via `scripts/icon.py`), Regular unless active, in the right tile colour.
9. **Contrast**: grey/160 on light, white on blue, navy and midnight.

## Tell the marketer (list it, by slide or by element)

- Every sample still in place: photos, product screens, names, logos, numbers, prices, dates.
- Every number and quote they must confirm has a source.
- What they must do by hand (e.g. resize chart bars in Show).
- Who reviews it: rendered social, video and email pieces can go out after this check;
  YouTube thumbnails, web pages and print go to a designer first.

Write the handover in plain language, no file paths or jargon.
