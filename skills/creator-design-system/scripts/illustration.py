"""Draw CDS 2.0 illustrations (Figma: Guides · Imagery › 06 · Illustrations).

Usage:
  python illustration.py list                      # the six reference illustrations
  python illustration.py show 04-growth out.png    # render a reference (or any .svg) to PNG to look at it
  python illustration.py check my.svg              # check a drawing against the illustration style

Draw a new one in Python with the helpers below, then check it, render it and look at it:

  import sys; sys.path.insert(0, "scripts")
  from illustration import *
  b = ground()
  b += tile(80, 260, 130, "shopping-cart", B, WHITE)          # CDS icons, in tiles
  b += card(320, 170, 170, 230) + lines(342, 245, 4, 126)    # a document
  b += path("M210 325 L255 325 L285 295 L320 295")           # connector with a 45° bend
  b += coin(660, 320, "currency-dollar")                    # yellow: the one warm accent
  save("order-to-cash.svg", b)                               # marked as a new illustration

Compose for the space it fills (references/illustrations.md › Compose it like a design lead): in a
post it is cropped to the drawing and scaled to the full picture zone, so draw a wide band of two or
three similar-sized objects, not small pieces in empty space. The six references are examples of the
style, not a fixed set: draw a new illustration for whatever
the content is about (a process, a system, a team, an industry, a result), from the same parts.

The style (references/illustrations.md): flat 2D on an 800 × 600 canvas, CDS colours only. Blues and
greys carry the picture; other CDS colours (yellow, green, red, violet) are small accents, under 8%
of the picture (`check` measures it): yellow for highlights, green for done or success,
red only for a stop or error, violet only on AI pieces. Flat offset shadows, rounded corners, 45° bends
in lines and arrows, CDS icons in tiles, a soft ground shadow. The Creator diamond behind the picture is
optional. Never people, logos, text, or a real-looking Creator screen.
Every new illustration is listed for design review in the handover.
"""
import json, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TOK = json.load(open(SKILL / "design-system" / "tokens.json"))["colour"]
LIB = json.load(open(SKILL / "assets" / "icons" / "icons.json"))["library"]
REFS = SKILL / "assets" / "illustrations" / "style"
W, H = 800, 600

C = lambda k: TOK[k]
B, B130, B70, B40, B30, B20, B10 = (C(f"blue/{n}") for n in (100, 130, 70, 40, 30, 20, 10))
Y, Y60, Y40, Y150 = C("yellow/90"), C("yellow/60"), C("yellow/40"), C("yellow/150")
V, V20 = C("violet/100"), C("violet/20")          # AI pieces only
GR, GR40, GR20 = C("green/90"), C("green/40"), C("green/20")   # small accent: done, success
RD, RD20 = C("red/90"), C("red/20")               # small accent: only a stop or an error
WHITE, G30, G40, G60, G80 = C("base/white"), C("grey/30"), C("grey/40"), C("grey/60"), C("grey/80")


def icon(name, x, y, size, col):
    """A CDS icon (python icon.py list). Unknown names stop with the close matches."""
    if name not in LIB:
        close = [n for n in LIB if name.replace("-", "") in n.replace("-", "")][:8]
        sys.exit(f"No icon '{name}'. Close matches: {', '.join(close) or 'none'}. Run: python scripts/icon.py find <word>")
    i = LIB[name]["regular"]; vb = [float(v) for v in i["viewBox"].split()]
    return f'<g transform="translate({x},{y}) scale({size / vb[2]:.4f})" fill="{col}">{i["body"].replace("currentColor", col)}</g>'


def rr(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'


def card(x, y, w, h, r=20, fill=None, shadow=True):
    """A rounded card with the flat offset shadow (blue/40 under white, blue/30 under colour)."""
    fill = fill or WHITE
    s = rr(x, y + 10, w, h, r, B40 if fill == WHITE else B30) if shadow else ""
    return s + rr(x, y, w, h, r, fill)


def tile(x, y, s, name, bg=None, fg=WHITE):
    bg = bg or B
    return card(x, y, s, s, s * 0.22, bg) + icon(name, x + s * 0.25, y + s * 0.25, s * 0.5, fg if bg != WHITE else B)


def path(d, col=None, w=6):
    return f'<path d="{d}" fill="none" stroke="{col or B70}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def dot(x, y, r=9, col=None):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col or B}"/>'


def lines(x, y, n, w, gap=22, col=None, last=0.6):
    """Grey text lines: a document or card without real words."""
    return "".join(rr(x, y + i * gap, w * (last if i == n - 1 else 1), 10, 5, col or G40) for i in range(n))


def coin(cx, cy, name="currency-dollar", r=64):
    return (f'<circle cx="{cx}" cy="{cy + 10}" r="{r + 14}" fill="{Y60}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{Y}"/>'
            + icon(name, cx - r / 2, cy - r / 2, r, Y150))


def ground(cx=400, y=540, w=520):
    return f'<ellipse cx="{cx}" cy="{y}" rx="{w / 2}" ry="14" fill="{B20}"/>'


def diamond(cx=400, cy=310, s=380, fill=None):
    """Optional: the Creator diamond behind the picture, only when it needs grounding."""
    return f'<rect x="{cx - s / 2}" y="{cy - s / 2}" width="{s}" height="{s}" rx="{s * 0.18}" fill="{fill or B20}" transform="rotate(45 {cx} {cy})"/>'


def save(out, body, new=True):
    mark = ' data-cds-illustration="new"' if new else ' data-cds-illustration="reference"'
    Path(out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"{mark}>{body}</svg>')
    print("saved", out)


def style_problems(src):
    """What breaks the illustration style (colours are checked by check_system.py)."""
    out = []
    if re.search(r"<text\b", src, re.I):
        out.append("illustration has text in it — words go in the template's text slots, not in the picture")
    if re.search(r"<image\b", src, re.I):
        out.append("illustration embeds a picture — draw it from shapes, or use a stock illustration file instead")
    if re.search(r"(?:linear|radial)Gradient", src):
        out.append("illustration uses a gradient — keep it flat (offset shadows, no gradients)")
    if re.search(r"<filter\b|drop-shadow|feGaussianBlur", src, re.I):
        out.append("illustration uses a blur or soft shadow filter — use the flat offset shadow")
    return out


ACCENT_LIMIT = 8   # % of the 800 × 600 picture that may be yellow, green, red or violet


def accent_share(svg_path):
    """Share of the picture in accent colours (yellow, green, red, violet), in % of the 800 × 600 canvas."""
    import numpy as np
    from PIL import Image
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "a.png"
    render(svg_path, str(tmp), quiet=True)
    allpx = np.asarray(Image.open(tmp).convert("RGB"), dtype=float).reshape(-1, 3)
    px = allpx[allpx.min(1) < 245]                                   # drawn pixels (white is background or card)
    if not len(px):
        return 0.0
    fams = {k.split("/")[0]: [] for k in TOK if "/" in k}
    names = [k for k, v in TOK.items() if isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", v)]
    pal = np.array([[int(TOK[k][i:i + 2], 16) for i in (1, 3, 5)] for k in names], dtype=float)
    near = np.array([names[i].split("/")[0] for i in ((px[:, None] - pal[None]) ** 2).sum(-1).argmin(1)])
    return float(np.isin(near, ["yellow", "green", "red", "violet"]).sum() * 100 / len(allpx))


def render(svg_path, png, quiet=False):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto(Path(svg_path).resolve().as_uri()); pg.screenshot(path=png); b.close()
    if not quiet:
        print("saved", png)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "list":
        for f in sorted(REFS.glob("*.svg")):
            print(f.stem)
        sys.exit()
    if a[0] == "show":
        src = REFS / f"{a[1]}.svg" if (REFS / f"{a[1]}.svg").exists() else Path(a[1])
        render(src, a[2] if len(a) > 2 else f"{src.stem}.png"); sys.exit()
    if a[0] == "check":
        sys.path.insert(0, str(Path(__file__).parent))
        from check_system import check_file
        v = check_file(a[1], a[a.index("--topic") + 1] if "--topic" in a else None)
        share = accent_share(a[1])
        if share > ACCENT_LIMIT:
            v.append(f"accent colours cover {share:.0f}% of the drawing — keep yellow, green, red and violet as small accents (under {ACCENT_LIMIT}% of the picture); let blues and greys carry it")
        if re.search(r'fill="#e81d17"|fill="#fef1f1"', Path(a[1]).read_text(), re.I):
            print("  note: red is used — keep it only for a stop or an error in the story")
        print("\n".join("  ✗ " + x for x in v) or "fits the CDS illustration style")
        sys.exit(1 if v else 0)
    sys.exit(__doc__)
