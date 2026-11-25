"""Shared helpers for the CDS 2.0 deck scripts.

The source deck is assets/deck/CDS-2.0-Creator-Deck-All-Slides.pptx (59 slides:
1-30 standard, 31 divider, 32-46 extras, 47-59 infographics). Never edit it in place; scripts
always write a new file.
"""
from pathlib import Path
from pptx import Presentation

SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCE_DECK = SKILL_DIR / "assets" / "deck" / "CDS-2.0-Creator-Deck-All-Slides.pptx"
EMU_PER_PT = 12700
DIVIDER_SLIDE = 31
CLOSING_SLIDES = {30, 46}
EXTRA_SLIDES = set(range(32, 60))
INFOGRAPHIC_SLIDES = set(range(47, 60))


def walk(shapes):
    """Yield every shape, descending into groups."""
    for sh in shapes:
        if sh.shape_type == 6:  # group
            yield from walk(sh.shapes)
        else:
            yield sh


def font_size(shape):
    sizes = [r.font.size.pt for p in shape.text_frame.paragraphs for r in p.runs if r.font.size]
    return max(sizes) if sizes else 12.0


def capacity(shape, fs=None):
    """Rough max characters a text box holds at a font size (its own by default).
    Zoho Puvi averages ~0.52 em per character; lines are ~1.18 em tall."""
    fs = fs or font_size(shape)
    w = (shape.width or 0) / EMU_PER_PT
    h = (shape.height or 0) / EMU_PER_PT
    per_line = max(1, int(w / (0.52 * fs)))
    lines = max(1, int(h / (1.18 * fs)))
    return int(per_line * lines * 0.9)


# The deck's own type sizes (pt), largest first. Stepping down moves one place along this list.
DECK_SIZES = [60, 44, 40, 36, 28, 24, 22, 20, 18, 16, 14, 12]
MIN_PT = 12          # nothing on a slide goes smaller than this
MAX_STEPS = 2        # at most two sizes smaller; past that, the text needs shortening


def step_size(pt, steps):
    """The deck size `steps` places below pt (pt itself if it isn't on the list or would go under MIN_PT)."""
    lower = [s for s in DECK_SIZES if s < pt - 0.01]
    if steps <= 0 or not lower:
        return pt
    return max(MIN_PT, lower[min(steps, len(lower)) - 1])


_FONTS = {}


def _font(bold, size):
    """Zoho Puvi at `size` (1 unit = 1pt) for measuring, or None when Pillow or the font isn't there."""
    key = (bold, round(size * 4))
    if key not in _FONTS:
        try:
            from PIL import ImageFont
            name = "Zoho-Puvi-Bold.ttf" if bold else "Zoho-Puvi-Regular.ttf"
            _FONTS[key] = ImageFont.truetype(str(SKILL_DIR / "assets" / "fonts" / name), max(1, round(size * 4)))
        except Exception:
            _FONTS[key] = None
    return _FONTS[key]


def _bold(shape):
    return any(r.font.bold for p in shape.text_frame.paragraphs for r in p.runs)


def line_height(shape, fs):
    """Single line spacing for Zoho Puvi as slide apps set it, or 1.18em without the font."""
    f = _font(_bold(shape), fs)
    if f is None:
        return 1.18 * fs
    a, d = f.getmetrics()
    return max((a + d) / 4, 1.2 * fs)        # PowerPoint and Zoho Show set single spacing at about 1.2em


def lines_needed(shape, text, fs):
    """Lines the text wraps to at fs: measured word by word with Zoho Puvi (estimated without it)."""
    w = (shape.width or 0) / EMU_PER_PT
    f = _font(_bold(shape), fs)
    if f is None:
        per_line = max(1, int(w / (0.52 * fs)))
        return sum(max(1, -(-len(par) // max(1, int(per_line * 0.9)))) for par in text.split("\n"))
    total = 0
    for par in text.split("\n"):
        n, cur = 1, ""
        for word in par.split():
            trial = (cur + " " + word).strip()
            if cur and f.getlength(trial) / 4 > w:
                n, cur = n + 1, word
            else:
                cur = trial
        total += n
    return total


def fit_text(slide, shape, text, apply=False, sample=None):
    """Adapt the layout to the content, like a designer would:
    1. the text fits its box as is → nothing changes;
    2. there is free space below → the box grows and the blocks stacked under it move down with it
       (they keep their gaps), as long as the stack stays clear of the next thing below and the bottom margin;
    3. otherwise the text steps down the deck's type sizes, one or two (each with the free space, too).
    Returns {"steps": k, "grow": pt} or None when even two sizes smaller there's no room.
    With apply=True the slide is changed (sizes, box height, positions)."""
    fs = font_size(shape)
    top_level = any(o.shape_id == shape.shape_id for o in slide.shapes)
    E = EMU_PER_PT
    sl_h = slide.part.package.presentation_part.presentation.slide_height / E
    x0, x1 = shape.left / E, (shape.left + shape.width) / E
    y0, h = shape.top / E, shape.height / E
    others = [o for o in slide.shapes if o.shape_id != shape.shape_id and o.width and o.height]
    over = lambda o: o.left / E < x1 - 1 and (o.left + o.width) / E > x0 + 1
    # the stack: blocks under this one in the same column, each starting within 40pt of the one above
    stack, bottom = [], y0 + h
    for o in sorted([o for o in others if over(o) and o.top / E >= y0 + h - 2], key=lambda o: o.top):
        if o.has_text_frame and o.top / E - bottom <= 40 and o.top / E >= y0 + h - 2:
            stack.append(o); bottom = (o.top + o.height) / E
        else:
            break
    floor_y = min([o.top / E for o in others if over(o) and all(o.shape_id != x.shape_id for x in stack) and o.top / E >= bottom - 2] + [sl_h - 36])
    # inside a card or panel the text keeps the card's padding (cards in a row stay the same size);
    # a full-slide background doesn't count as a card
    sl_w = slide.part.package.presentation_part.presentation.slide_width / E
    for o in others:
        ox0, oy0, ox1, oy1 = o.left / E, o.top / E, (o.left + o.width) / E, (o.top + o.height) / E
        if ox0 <= x0 + 1 and oy0 <= y0 + 1 and ox1 >= x1 - 1 and oy1 >= bottom - 1 and (ox1 - ox0) * (oy1 - oy0) < 0.6 * sl_w * sl_h:
            floor_y = min(floor_y, bottom + 24)        # no room beyond its own padding
    room = max(0.0, floor_y - 24 - bottom) if top_level else 0.0     # keep 24pt before the next block
    # the template's own breathing room under its sample text stays when the box grows
    sample = shape.text_frame.text if sample is None else sample      # the template's text, before any change
    sample_lines = lines_needed(shape, sample, fs) if sample.strip() else 1
    slack = max(0.0, h - sample_lines * line_height(shape, fs))
    # the template is the truth: whatever its sample fills, the box holds (our measure can be stricter)
    eff_h = max(h, sample_lines * line_height(shape, fs) + slack)
    # less text than the sample: the blocks stacked under it close up, so the gap from a title to its
    # paragraph stays the template's gap instead of an empty line
    n0 = lines_needed(shape, text, fs)
    if top_level and stack and n0 < sample_lines:
        shrink = (sample_lines - n0) * line_height(shape, fs)
        if apply:
            shape.height = int(max(1, shape.height - shrink * E))
            for o in stack:
                o.top = int(o.top - shrink * E)
        return {"steps": 0, "grow": -round(shrink)}
    for k in range(MAX_STEPS + 1):
        size = step_size(fs, k)
        if k and size == step_size(fs, k - 1):
            break
        n_lines = lines_needed(shape, text, size)
        need = n_lines * line_height(shape, size) + slack
        grow = max(0.0, need - eff_h)
        # a title (28pt and up) reads best in three lines or fewer: try a smaller size before a fourth line
        long_title = grow and size >= 28 and n_lines > 3 and k < MAX_STEPS and step_size(fs, k + 1) < size
        if grow <= room + 0.5 and not long_title:
            if apply:
                if k:
                    from pptx.util import Pt
                    for p in shape.text_frame.paragraphs:
                        for r in p.runs:
                            if r.font.size:
                                r.font.size = Pt(step_size(r.font.size.pt, k))
                if grow:
                    shape.height = int(shape.height + grow * E)
                    for o in stack:
                        o.top = int(o.top + grow * E)
            return {"steps": k, "grow": round(grow)}
    return None


def fit_steps(shape, text):
    """Type steps only (no free space): 0 if it fits, None if even MAX_STEPS smaller it doesn't."""
    n = len(text.replace("\n", " "))
    fs = font_size(shape)
    for k in range(MAX_STEPS + 1):
        size = step_size(fs, k)
        if k and size == step_size(fs, k - 1):
            break
        if n <= capacity(shape, size):
            return k
    return None


def fit_note(r):
    bits = []
    if r["steps"]:
        bits.append("one type size smaller" if r["steps"] == 1 else "two type sizes smaller")
    if r["grow"] > 0:
        bits.append(f"box grown {r['grow']}pt into the free space (blocks below moved down)")
    elif r["grow"] < 0:
        bits.append(f"shorter than the sample, blocks below closed up {-r['grow']}pt")
    return " and ".join(bits)


def is_furniture(shape):
    """Page numbers and the footer URL are not content slots."""
    t = shape.text_frame.text.strip()
    if t.isdigit() and len(t) <= 2:
        return True
    return t.lower() in {"zoho.com/creator"}


def text_slots(slide):
    out = []
    for sh in walk(slide.shapes):
        if sh.has_text_frame and sh.text_frame.text.strip() and not is_furniture(sh):
            out.append(sh)
    return out


def pictures(slide):
    return [sh for sh in walk(slide.shapes) if sh.shape_type == 13]


def sample_images(slide):
    """Only images the marketer must replace. They are named 'Photo (replace)';
    logos, patterns and overlays are system artwork and must stay."""
    return [p for p in pictures(slide) if "replace" in p.name.lower()]


# Slide 8's three step cards hold drawn sample screens but aren't named "(replace)".
SCREEN_SHAPES_BY_SLIDE = {8: {"Shape 3", "Shape 19", "Shape 41"}}
FIXED_LABELS = {"thank you", "?"}


def screen_regions(slide_no, slide):
    regions = []
    for sh in walk(slide.shapes):
        named = "replace" in sh.name.lower() and sh.shape_type != 13
        if named or sh.name in SCREEN_SHAPES_BY_SLIDE.get(slide_no, set()):
            regions.append((sh.left, sh.top, sh.left + sh.width, sh.top + sh.height))
    return regions


def slot_role(slide_no, slide, shape, regions=None):
    """'screen' = text drawn inside a sample product screen (replace the whole screen),
    'label'  = fixed small caps label or legal line (leave as is),
    'content' = text the marketer's story fills."""
    regions = screen_regions(slide_no, slide) if regions is None else regions
    cx, cy = shape.left + shape.width / 2, shape.top + shape.height / 2
    if any(l <= cx <= r and t <= cy <= b for l, t, r, b in regions):
        return "screen"
    t = shape.text_frame.text.strip()
    if t.startswith("©") or t.lower() in FIXED_LABELS:
        return "label"
    if t.isupper() and len(t) <= 16 and font_size(shape) <= 8:
        return "label"
    return "content"
