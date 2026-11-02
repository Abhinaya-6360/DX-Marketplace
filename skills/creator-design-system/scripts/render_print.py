"""Render a CDS 2.0 print template to a CMYK PDF with bleed and crop marks.

Usage:
  python render_print.py list
  python render_print.py slots a4-flyer
  python render_print.py brief.json out.pdf [--preview out.png]

brief.json:
{
  "template": "a4-flyer",
  "text": {"Eyebrow": "WEBINAR · 20 NOV 2026", "Headline": "Automate approvals in minutes",
           "Body": "Two or three short sentences.", "Call to action": "Register at zoho.com/creator"},
  "list": {"Benefits": ["First benefit", "Second benefit", "Third benefit"]},
  "qr": "https://www.zoho.com/creator/"          # roll-up banner
}

Sets (tri-fold = outside + inside sheets; brochure-4pp = cover, inside-left, inside-right, back)
take text per page:
{"template": "trifold", "qr": "https://…",
 "pages": {"outside": {"text": {...}, "list": {...}}, "inside": {"text": {...}}}}
{"template": "brochure-4pp",
 "pages": {"cover": {...}, "inside-left": {...}, "inside-right": {...}, "back": {...}}}

Colours are the official CMYK values from Foundations · Colour (tokens.json "cmyk"), not
converted screen colours. Every edge has 3 mm bleed and crop marks; text and logos must sit
5 mm inside the trim. Zoho Puvi is embedded. A designer approves and orders a printed proof
before anything goes to a vendor (Guides · Print).
"""
import json, re, sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from reportlab.graphics.barcode import qr as rlqr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

SKILL = Path(__file__).resolve().parent.parent
A = SKILL / "assets"
T = json.load(open(A / "print" / "layouts.json"))["templates"]
TOK = json.load(open(SKILL / "design-system" / "tokens.json"))
CMYK = TOK["cmyk"]["values"]
MM = 72 / 25.4
BLEED, SAFE, MARK = 3 * MM, 5 * MM, 10 * MM

for w in ("Regular", "Medium", "Semibold", "Bold"):
    pdfmetrics.registerFont(TTFont(f"Puvi-{w}", str(A / "fonts" / f"Zoho-Puvi-{w}.ttf")))

# Logo artwork colours (not palette tokens). Process values; confirm against the official
# print logo files before a large run.
LOGO_CMYK = {"#0a0a0a": [0, 0, 0, 100], "#000000": [0, 0, 0, 100], "black": [0, 0, 0, 100],
             "#226db4": [85, 50, 0, 0], "#e42527": [0, 95, 90, 0], "#089949": [90, 10, 95, 5],
             "#f9b21d": [0, 32, 95, 0], "white": [0, 0, 0, 0], "#ffffff": [0, 0, 0, 0]}


def cm(tok, alpha=1):
    c, m, y, k = CMYK[tok]
    return CMYKColor(c / 100, m / 100, y / 100, k / 100, alpha=alpha)


def cm_list(v, alpha=1):
    return CMYKColor(*(x / 100 for x in v), alpha=alpha)


# ---------- minimal SVG path support (absolute M L H V C Z, as exported by Figma) ----------
NUM = re.compile(r"[MLHVCZmlhvcz]|-?\d*\.?\d+(?:e-?\d+)?")


def draw_svg_path(c, d, ox, oy, s, H):
    p = c.beginPath()
    toks = NUM.findall(d)
    i, cmd, x, y = 0, None, 0, 0
    X = lambda v: ox + v * s
    Y = lambda v: H - (oy + v * s)
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in "Zz":
                p.close(); continue
            continue
        if cmd == "M":
            x, y = float(toks[i]), float(toks[i + 1]); p.moveTo(X(x), Y(y)); i += 2; cmd = "L"
        elif cmd == "L":
            x, y = float(toks[i]), float(toks[i + 1]); p.lineTo(X(x), Y(y)); i += 2
        elif cmd == "H":
            x = float(toks[i]); p.lineTo(X(x), Y(y)); i += 1
        elif cmd == "V":
            y = float(toks[i]); p.lineTo(X(x), Y(y)); i += 1
        elif cmd == "C":
            a = [float(v) for v in toks[i:i + 6]]
            p.curveTo(X(a[0]), Y(a[1]), X(a[2]), Y(a[3]), X(a[4]), Y(a[5])); x, y = a[4], a[5]; i += 6
        else:
            i += 1
    return p


def draw_svg_file(c, path, r, H, recolour=None, even_odd=False):
    s = Path(path).read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    x, y, w, h = r
    sc = w / vb[2]
    for m in re.finditer(r'<path ([^>]*)/>', s):
        a = m.group(1)
        d = re.search(r' ?d="([^"]+)"', a).group(1)
        fill = (re.search(r'fill="([^"]+)"', a) or [None, "black"])[1].lower()
        col = recolour or LOGO_CMYK.get(fill, [0, 0, 0, 100])
        c.setFillColor(cm_list(col) if isinstance(col, list) else col)
        c.drawPath(draw_svg_path(c, d, x, y, sc, H), stroke=0, fill=1, fillMode=1 if 'evenodd' in a else 0)


# ---------- patterns: generated from the Figma motifs ----------
SIG = ("M12.6 19.2C11.95 19.2 11.34 18.95 10.88 18.49L2.8 10.4C2.59 10.18 2.59 9.82 2.8 9.6L10.88 1.51C11.34 1.05 11.95 0.8 12.6 0.8"
       "C13.25 0.8 13.86 1.05 14.32 1.51L17.2 4.39C17.41 4.61 17.41 4.97 17.2 5.19L12.39 10L17.2 14.81C17.41 15.03 17.41 15.39 17.2 15.61"
       "L14.32 18.49C13.86 18.95 13.25 19.2 12.6 19.2ZM3.99 10L11.67 17.69C11.92 17.94 12.25 18.08 12.6 18.08C12.95 18.08 13.28 17.94 13.53 17.69"
       "L16.01 15.21L11.2 10.4C10.98 10.18 10.98 9.82 11.2 9.6L16.01 4.79L13.53 2.31C13.28 2.06 12.95 1.92 12.6 1.92C12.25 1.92 11.93 2.06 11.68 2.31L3.99 10Z")
WEAVE = ["M7.5 69.27C5.05 69.27 2.75 68.32 1.02 66.58L-29.38 36.13C-30.21 35.31 -30.21 33.97 -29.38 33.14L1.03 2.69C2.76 0.96 5.05 0 7.5 0"
         "C9.96 0 12.25 0.95 13.98 2.69L24.8 13.53C25.62 14.35 25.62 15.69 24.8 16.51L6.7 34.64L24.8 52.76C25.62 53.58 25.62 54.92 24.8 55.75"
         "L13.98 66.59C12.24 68.31 9.95 69.27 7.5 69.27ZM-24.91 34.64L4.01 63.6C4.94 64.53 6.18 65.04 7.5 65.04C8.81 65.04 10.05 64.53 10.98 63.6"
         "L20.32 54.25L2.22 36.13C1.4 35.31 1.4 33.97 2.22 33.14L20.32 15.02L11 5.68C10.07 4.75 8.83 4.23 7.51 4.23C6.2 4.23 4.96 4.75 4.03 5.68L-24.91 34.64Z",
         "M5.25 3.03L-24.68 33.84V35.08L8.27 68.02L22.03 53.37L3.74 35.08L22.03 14.3L13.51 5.16L5.25 3.03Z"]


def draw_pattern(c, el, H, sc):
    x, y, w, h = [v * sc for v in el["r"]]
    c.saveState()
    clip = c.beginPath(); clip.rect(x, H - y - h, w, h); c.clipPath(clip, stroke=0, fill=0)
    c.setFillColor(cm(el["fill"], el.get("opacity", 1)))
    k = el["tile"] / (120 if el["kind"] == "signature" else 240) * sc
    if el["kind"] == "signature":   # 20-unit grid, odd rows shifted half a step
        step = 20 * k
        rows = int(h / step) + 2
        for r_ in range(rows):
            off = 0 if r_ % 2 == 0 else -10 * k
            for cc in range(int(w / step) + 2):
                c.drawPath(draw_svg_path(c, SIG, x + off + cc * step, y + r_ * step, k, H), stroke=0, fill=1)
    else:                            # 60-unit grid, odd rows shifted half a step
        step = 60 * k
        for r_ in range(-1, int(h / step) + 2):
            off = 30 * k if r_ % 2 == 0 else 0
            for cc in range(-1, int(w / step) + 2):
                for d in WEAVE:
                    c.drawPath(draw_svg_path(c, d, x + off + cc * step, y + r_ * step, k, H), stroke=0, fill=1)
    c.restoreState()


def gradient_rect(c, r, H, cols):
    x, y, w, h = r
    c.saveState()
    p = c.beginPath(); p.rect(x, H - y - h, w, h); c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(x, H - y, x + w, H - y - h, (cm(cols[0]), cm(cols[1])), extend=True)
    c.restoreState()


def wrap(text, font, size, width):
    lines = []
    for para in text.split("\n"):
        lines += simpleSplit(para, font, size, width) or [""]
    return lines


SETS = json.load(open(A / "print" / "layouts.json")).get("sets", {})


def draw_page(c, tkey, b, errors, samples):
    t = T[tkey]
    sc = t["scale"]
    W, H = t["size"][0] * sc, t["size"][1] * sc
    PW, PH = W + 2 * (BLEED + MARK), H + 2 * (BLEED + MARK)
    c.setPageSize((PW, PH))
    off = BLEED + MARK
    c.setTrimBox((off, off, off + W, off + H)); c.setBleedBox((off - BLEED, off - BLEED, off + W + BLEED, off + H + BLEED))
    c.saveState(); c.translate(off, off)
    bg = t["bg"]
    if "gradient" in bg:
        gradient_rect(c, (-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED), H, bg["gradient"])
    else:
        c.setFillColor(cm(bg["fill"])); c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, stroke=0, fill=1)
    safe = (SAFE, SAFE, W - SAFE, H - SAFE)
    txt, lst = b.get("text", {}), b.get("list", {})
    label = t["name"]
    for el in t["el"]:
        k = el["t"]
        r = [v * sc for v in el["r"]]
        x, y, w, h = r
        def grow(rr):
            rr = list(rr)
            if rr[0] <= 0: rr[0] -= BLEED; rr[2] += BLEED
            if rr[1] <= 0: rr[1] -= BLEED; rr[3] += BLEED
            if rr[0] + rr[2] >= W - 0.5: rr[2] += BLEED
            if rr[1] + rr[3] >= H - 0.5: rr[3] += BLEED
            return rr
        if k == "panel":
            gradient_rect(c, grow(r), H, el["gradient"])
        elif k == "rect":
            rr = grow(r) if not el.get("radius") else r
            c.setFillColor(cm(el["fill"]))
            if el.get("radius"): c.roundRect(rr[0], H - rr[1] - rr[3], rr[2], rr[3], el["radius"] * sc, stroke=0, fill=1)
            else: c.rect(rr[0], H - rr[1] - rr[3], rr[2], rr[3], stroke=0, fill=1)
        elif k == "pattern":
            e2 = dict(el); rr = list(el["r"])
            if rr[1] + rr[3] >= t["size"][1] - 0.5: rr[3] += BLEED / sc
            if rr[0] + rr[2] >= t["size"][0] - 0.5: rr[2] += BLEED / sc
            if rr[1] <= 0: rr[1] -= BLEED / sc; rr[3] += BLEED / sc
            if rr[0] <= 0: rr[0] -= BLEED / sc; rr[2] += BLEED / sc
            e2["r"] = rr
            draw_pattern(c, e2, H, sc)
        elif k in ("lockup", "zoho"):
            f = "creator-lockup-colour.svg" if k == "lockup" else "zoho-logo-colour.svg"
            draw_svg_file(c, A / "logos" / f, r, H, recolour=[0, 0, 0, 0] if el["white"] else None)
            if x < safe[0] - .5 or y < safe[1] - .5 or x + w > safe[2] + .5 or y + h > safe[3] + .5:
                errors.append(f"{label}: {'Creator lockup' if k == 'lockup' else 'Zoho logo'} sits outside the 5 mm safe zone.")
        elif k in ("text", "list", "button"):
            weight, size = el["font"]; font = f"Puvi-{weight}"; size *= sc
            if k == "list":
                items = lst.get(el["slot"]) or el["sample"]
                if el["slot"] not in lst: samples.append(f"{label}: {el['slot']} (sample text)")
                if len(items) > el["max"]: errors.append(f"{label}: {el['slot']} — at most {el['max']} items.")
                c.setFont(font, size); c.setFillColor(cm(el["fill"]))
                for i, it in enumerate(items[:el["max"]]):
                    line = "•  " + it
                    if pdfmetrics.stringWidth(line, font, size) > w: errors.append(f"{label}: {el['slot']} — '{it[:30]}…' is too long for one line.")
                    c.drawString(x, H - y - size - i * el["step"] * sc, line)
                continue
            val = txt.get(el["slot"])
            if val is None:
                val = el["sample"]; samples.append(f"{label}: {el['slot']} (sample text)")
            if k == "button":
                c.setFillColor(cm(el["fill"])); c.roundRect(x, H - y - h, w, h, el["radius"] * sc, stroke=0, fill=1)
                c.setFont(font, size); c.setFillColor(cm(el["text"]))
                if pdfmetrics.stringWidth(val, font, size) > w - 2 * el["pad"] * sc: errors.append(f"{label}: {el['slot']} — too long for the button.")
                c.drawString(x + el["pad"] * sc, H - y - h / 2 - size * 0.35, val)
                continue
            lead = size * 1.3
            lines = wrap(val, font, size, w)
            if len(lines) * lead > h * 1.05 + 0.5:
                errors.append(f"{label}: {el['slot']} — {len(lines)} lines don't fit (room for {max(1, int(h / lead))}). Shorten it; don't change the size.")
            c.setFont(font, size); c.setFillColor(cm(el["fill"]))
            for i, line in enumerate(lines):
                ty = H - y - size - i * lead
                if el.get("align") == "center": c.drawCentredString(x + w / 2, ty, line)
                else: c.drawString(x, ty, line)
        elif k == "qr":
            c.setFillColor(cm(el["fill"])); c.roundRect(x, H - y - h, w, h, el["radius"] * sc, stroke=0, fill=1)
            link = b.get("qr")
            if not link:
                link = el["sample"]; samples.append(f"{label}: QR code link (sample: zoho.com/creator)")
            q = rlqr.QrCodeWidget(link); bx = q.getBounds(); qs = (w * 0.86)
            d = Drawing(qs, qs, transform=[qs / (bx[2] - bx[0]), 0, 0, qs / (bx[3] - bx[1]), 0, 0]); q.barFillColor = cm("base/black"); d.add(q)
            renderPDF.draw(d, c, x + (w - qs) / 2, H - y - h + (h - qs) / 2)
    c.setStrokeColor(cm("base/black")); c.setLineWidth(0.25)
    for (px, py) in ((0, 0), (W, 0), (0, H), (W, H)):
        dx = -1 if px == 0 else 1; dy = -1 if py == 0 else 1
        c.line(px + dx * (BLEED + 1 * MM), py, px + dx * (BLEED + MARK - 1 * MM), py)
        c.line(px, py + dy * (BLEED + 1 * MM), px, py + dy * (BLEED + MARK - 1 * MM))
    c.setDash(2, 2)
    for fx in t.get("folds", []):      # fold marks, outside the bleed, top and bottom
        fx *= sc
        c.line(fx, H + BLEED + 1 * MM, fx, H + BLEED + MARK - 1 * MM); c.line(fx, -BLEED - 1 * MM, fx, -BLEED - MARK + 1 * MM)
    c.setDash()
    c.restoreState(); c.showPage()


def render(brief_path, out_pdf, preview=None):
    b = json.load(open(brief_path))
    key = b["template"]
    pages = SETS.get(key, [key])
    c = canvas.Canvas(str(out_pdf))
    name = T[pages[0]]["name"].split(" · ")[0]
    c.setTitle(f"Zoho Creator · {name}"); c.setAuthor("Zoho Creator · CDS 2.0")
    errors, samples = [], []
    for pk in pages:
        pb = {**b, **b.get("pages", {}).get(pk.split("-", 1)[1], {})} if key in SETS else b
        draw_page(c, pk, pb, errors, samples)
    c.save()
    t = T[pages[0]]
    print(f"Saved {out_pdf} · {name} · {len(pages)} page(s) · trim {t['size_mm'][0]}×{t['size_mm'][1]} mm · 3 mm bleed · CMYK" + (" · fold marks" if t.get("folds") else ""))
    print("PRINT CHECK"); print("Errors: none" if not errors else "Errors:")
    for e in errors: print("  ✗", e)
    print("To replace before printing:" if samples else "To replace: none")
    for s_ in samples: print("  •", s_)
    print("Before it goes to a vendor: a designer approves it and orders one printed proof (Guides · Print).")
    if preview:
        import subprocess
        subprocess.run(["pdftoppm", "-png", "-r", "60" if T[pages[0]]["scale"] == 1 else "8", str(out_pdf), str(Path(preview).with_suffix(""))], check=False)
    return 1 if errors else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "list":
        for k, t in T.items(): print(f"{k:24} {t['size_mm'][0]}×{t['size_mm'][1]} mm   ({t['name']})")
        for k, pg in SETS.items(): print(f"{k:24} set of {len(pg)} pages: {', '.join(pg)}")
    elif a[0] == "slots":
        for pk in SETS.get(a[1], [a[1]]):
            print(f"[{pk}]"); [print(f"  {e['slot']}: {e['t']}") for e in T[pk]["el"] if e.get("slot")]
    else:
        pv = a[a.index("--preview") + 1] if "--preview" in a else None
        sys.exit(render(a[0], a[1], pv))
