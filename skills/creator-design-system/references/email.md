# Email newsletters

Based on the three newsletters on Templates · Web in the CDS-2.0 Figma file (Creator Bytes,
Customer Email 1, Customer Email 2). `scripts/build_email.py` builds them as email-safe HTML:
600 px wide, table layout, inline styles, images as PNG (many inboxes block SVG), a hidden
preheader, and a mobile rule for narrow screens. It works with any email tool.

## Fonts (the one exception to Zoho Puvi)

Email apps can't load web fonts, so newsletters use Georgia for headings (title 46/51, section
headings 26/34, story headings 40/46) and Helvetica Neue for body (16/24, item titles 18
medium, links and buttons 14 bold). Everything else in the email follows CDS 2.0: colours,
logos, red CTA, violet for AI only. (Foundations · Typography → Email typography.)

## Sections

| Section | Use it for |
| --- | --- |
| Header | Creator lockup left, Zoho logo right, grey/30 rule — always first, built in |
| Title + hero tile | Georgia title with an optional 3D tile (blue; violet only for AI) |
| Greeting + intro | "Hi there," and one or two short paragraphs |
| `band` | A themed group of items on a tinted band: blue (default), violet (AI only), green, yellow; header icon tile + Georgia heading + white card of items |
| `list` | Items with icon tiles and "READ MORE →" links, separated by rules (Customer Email 1) |
| `story` | Customer spotlight, video, editor's pick: Georgia heading, optional 3D tile and image, text, link (Creator Bytes) |
| `cta` | One red button with a line above it — at most one per email |
| Sign-off + footer | Blue band: "Regards, The Zoho Creator Team", follow line, social icons — always last, built in |

## Workflow

1. Get the content: subject, preheader, title, intro, the sections and their items, real links,
   any images. Ask once for what's missing; never invent features, numbers or links.
2. Pick icons with `python scripts/icon.py list`; one tone per band; violet only if the band is
   about AI (`"ai": true`).
3. Write email.json (format at the top of `scripts/build_email.py`) and run
   `python scripts/build_email.py email.json <name>/`.
4. Fix every error, look at `<name>/preview.png`, then hand over `<name>.zip` (index.html +
   images) with the "To do before sending" list.

## Handover

Tell the marketer to import the zip into their email tool (or upload the images folder and
rebuild with `--base-url` if the tool needs hosted images), and to send a test to themselves
in Gmail and Outlook before the real send.
