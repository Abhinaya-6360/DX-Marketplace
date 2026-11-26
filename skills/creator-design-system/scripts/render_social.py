"""Render a CDS 2.0 social, video or email template to an exact-size PNG.

Usage:
  python render_social.py list                      # templates and their versions
  python render_social.py slots feature             # the text slots a template has
  python render_social.py brief.json out.png        # render + brand check

brief.json:
{
  "template": "feature",            # see `list`
  "version": "product-light",       # see `list`
  "topic": "default",               # default | ai | partner  (changes background and highlights)
  "text": {"Headline": "Approvals, **automated** in minutes",
           "Supporting text": "Send every request to the right approver."},
  "tag": "NEW",                     # tag label; "" hides the tag
  "tag_style": "chip",              # optional: chip | outline | eyebrow (chosen for you when left out)
  "screenshot": "/path/screen.png", # optional: product screenshot for the card
  "illustration": "/path/art.svg",  # or, in the same slot: a CDS-style illustration (SVG, scripts/illustration.py)
                                    # or a stock illustration (PNG) recoloured to CDS; both go to design review
  "photo": "/path/cutout.png",      # optional: Quote speaker (transparent cut-out PNG)
  "partner_logo": "/path/logo.png", # partner topic: Creator | partner co-branded lockup
  "speakers": [{"name": "Priya Raman", "role": "Product Marketing", "company": "Zoho Creator",
                "photo": "/path/priya.png"}]          # Webinar
}

Highlight one or two words with **double asterisks**: yellow box on Bold, blue text on
Light, violet text on AI and partner topics.

The template layouts come from assets/social/layouts.json (exported from the CDS-2.0
Figma file). Never move elements; change only text, tag, images and topic.
Writes out.png and out.html, then prints the brand check. Exit code 1 if it fails.
"""
import base64, html, json, mimetypes, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
A = SKILL / "assets"
LAYOUTS = json.load(open(A / "social" / "layouts.json"))["templates"]
TOKENS = json.load(open(SKILL / "design-system" / "tokens.json"))
COL = TOKENS["colour"]
ROLE = {f"role/{k}": v["value"] for k, v in TOKENS["role"].items()}
TS = TOKENS["textStyles"]
WEIGHT = {"regular": 400, "medium": 500, "semibold": 600, "bold": 700}
TAG = {"blue": ("blue/100", "base/white"), "yellow": ("yellow/100", "grey/160"),
       "violet": ("violet/100", "base/white"), "navy": ("blue/160", "base/white")}
BOLD_BG = {"midnight", "glow", "brand-depth", "ai"}


def colour(tok):
    return COL.get(tok) or ROLE.get(tok) or tok


def data_uri(path):
    p = Path(path)
    mt = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mt};base64,{base64.b64encode(p.read_bytes()).decode()}"


def svg_uri(path, recolour=None):
    s = Path(path).read_text()
    if recolour:
        s = s.replace("currentColor", recolour).replace('color="#0D4EF2"', "")
    return "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()


# Zoho Puvi covers Latin. Other languages fall back to Noto Sans (bundled: Tamil, Devanagari, Arabic;
# installed: Noto Sans CJK for Japanese, Chinese and Korean) and are flagged for design review.
FONT_STACK = "'Zoho Puvi','Noto Sans Tamil','Noto Sans Devanagari','Noto Sans Arabic','Noto Sans CJK JP','Noto Sans CJK KR',sans-serif"
RTL_RE = __import__("re").compile("[\u0590-\u08ff\ufb1d-\ufdff\ufe70-\ufeff]")


def font_css():
    out = []
    for w, n in WEIGHT.items():
        out.append(f"@font-face{{font-family:'Zoho Puvi';font-weight:{n};"
                   f"src:url('{data_uri(A / 'fonts' / f'Zoho-Puvi-{w.capitalize()}.ttf')}');}}")
    noto = A / "fonts" / "noto"
    if noto.exists():
        for fam in ("Tamil", "Devanagari", "Arabic"):
            for n, w in ((400, "Regular"), (500, "Regular"), (600, "SemiBold"), (700, "SemiBold")):
                f = noto / f"NotoSans{fam}-{w}.ttf"
                if f.exists():
                    out.append(f"@font-face{{font-family:'Noto Sans {fam}';font-weight:{n};src:url('{data_uri(f)}');}}")
    return "\n".join(out)


def rtl_css(text):
    return "direction:rtl;unicode-bidi:plaintext;" if RTL_RE.search(text or "") else ""


def text_css(el):
    if "px" in el:
        size, weight = el["px"]
        lh = round(size * el.get("lh", 1.25))
        ls = "-0.01em"
    else:
        s = TS[el["style"]]
        size, weight, lh = s["size"], WEIGHT[s["weight"]], s["lineHeight"]
        ls = f"{float(s['letterSpacing'][:-1]) / 100}em"
    return f"font-size:{size}px;font-weight:{weight};line-height:{lh}px;letter-spacing:{ls};"


def smaller_styles(el, n=2):
    """The next CDS text styles down (same weight), for when the content is longer than the template expects."""
    if "px" in el:
        size, weight = el["px"]
        return [f"font-size:{round(size * f)}px;line-height:{round(size * f * el.get('lh', 1.25))}px" for f in (0.9, 0.8)][:n]
    cur = TS[el["style"]]
    weight = cur["weight"]
    down = sorted({v["size"]: v for k, v in TS.items() if v["weight"] == weight and v["size"] < cur["size"]
                   and k.split("/")[0].startswith(("h", "text-large"))}.values(), key=lambda v: -v["size"])[:n]
    return [f"font-size:{v['size']}px;line-height:{v['lineHeight']}px;letter-spacing:{float(v['letterSpacing'][:-1]) / 100}em" for v in down]


def rich(text, tone_bold, topic, hl=None):
    t = html.escape(text).replace("\n", "<br>")
    if hl:
        span = f"<span style='color:{colour(hl)}'>\\1</span>"
    elif topic == "ai" and tone_bold:
        # AI gradient: white text, highlight words in yellow/100 (never violet on the gradient)
        span = f"<span style='color:{COL['yellow/100']}'>\\1</span>"
    elif topic in ("ai", "partner") and not tone_bold:
        span = f"<span style='color:{COL['violet/100']}'>\\1</span>"
    elif tone_bold:
        span = (f"<span style='background:{COL['yellow/100']};color:{COL['grey/160']};"
                "padding:0 0.12em;box-decoration-break:clone;-webkit-box-decoration-break:clone'>\\1</span>")
    else:
        span = f"<span style='color:{COL['blue/100']}'>\\1</span>"
    return re.sub(r"\*\*(.+?)\*\*", span, t)


def background(style, texture, topic):
    bold = style in BOLD_BG
    if topic == "ai":
        style, texture = ("ai", 0) if bold else ("mesh-soft-ai", 0)
    elif topic == "partner":
        style, texture = ("midnight", 0.08 if texture else 0) if bold else ("mesh-partner", 0)
    g = TOKENS["gradients"][style]["css"]
    tile = A / "patterns" / ("connect-tile-bold.svg" if bold else "connect-tile-light.svg")
    tex = (f"<div style='position:absolute;inset:0;background:url({svg_uri(tile)}) 0 0/480px 480px;"
           f"opacity:{texture}'></div>") if texture else ""
    return f"<div style='position:absolute;inset:0;background:{g}'></div>{tex}", bold


def illustration_zone(r, v, W, H):
    """An illustration has no frame, so it may use more room than the screenshot card: the full width
    between the text margins, from the slot's top to the slot's bottom, stopping above the logos."""
    x, y, w, h = r
    texts = [e for e in v["el"] if e["t"] in ("text", "tag", "lockup")]
    margin = min([e["r"][0] for e in texts] + [x])
    left, right, bottom = margin, W - margin, y + h
    for e in v["el"]:                        # text beside the picture (landscape, X): stay clear of it
        if e["t"] in ("text", "tag", "lockup", "zoho") and "r" in e:
            ex, ey, ew, eh = e["r"]
            if ey < y + h and ey + eh > y + 10:
                if ex + ew <= x + 10: left = max(left, ex + ew + 40)
                elif ex >= x + w - 10: right = min(right, ex - 40)
    for e in v["el"]:
        if e["t"] in ("zoho", "lockup", "text") and "r" in e:
            ex, ey, ew, eh = e["r"]
            if ey > y + h * 0.5 and ex < right and ex + ew > left and ey < y + h + 40:   # a logo or line below the picture
                bottom = min(bottom, ey - 24)
    return [left, y, right - left, max(int(h * 0.75), bottom - y)]


FIT_JS = """<script>for(const s of document.querySelectorAll('svg[data-cds-illustration]')){const b=s.getBBox(),p=Math.max(b.width,b.height)*0.02;
s.setAttribute('viewBox',`${b.x-p} ${b.y-p} ${b.width+2*p} ${b.height+2*p}`);}</script>"""


def illustration_slot(r, path, bold=False):
    """A CDS illustration (SVG, drawn in the style) or a stock illustration (PNG/JPG) in the picture zone:
    no card frame, cropped to the drawing, scaled up to fill the zone, sitting on its bottom edge."""
    x, y, w, h = r
    p = Path(path)
    base = f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:flex-end;justify-content:center"
    if p.suffix.lower() == ".svg":
        svg = re.sub(r"<\?xml[^>]*>", "", p.read_text())
        svg = re.sub(r"\swidth=[\"']\d+[\"']\s+height=[\"']\d+[\"']", "", svg, count=1)
        svg = re.sub(r"<svg\b", "<svg style='width:100%;height:100%' preserveAspectRatio='xMidYMax meet'", svg, count=1)
        if "data-cds-illustration" in svg:
            svg = svg.replace("data-cds-illustration", f"data-name='{p.stem}' data-cds-illustration", 1)
        if bold:   # on blue or Midnight the light ground shadow reads as a white bar: make it a faint glow
            svg = re.sub(r'(<ellipse\b[^>]*fill=")#e7edfe(")', r'\1#ffffff\2 fill-opacity="0.12"', svg, flags=re.I)
        return f"<div data-el='screenshot' style='{base}'>{svg}{FIT_JS}</div>"
    return f"<div data-el='screenshot' style='{base}'><img src='{data_uri(p)}' style='max-width:100%;max-height:100%;object-fit:contain;object-position:bottom'></div>"


def screenshot_card(r, img):
    x, y, w, h = r
    base = (f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:24px;"
            f"background:#fff;border:1px solid {COL['grey/40']};box-shadow:0 40px 80px -16px #00000029;overflow:hidden;")
    if img:
        return f"<div data-el='screenshot' style='{base}'><img src='{data_uri(img)}' style='width:100%;height:100%;object-fit:cover;object-position:top left'></div>", False
    s = w / 1000
    rows = "".join(f"<div style='height:{28*s}px;margin:{10*s}px 0;border-radius:{4*s}px;background:{COL['blue/20'] if i == 1 else COL['grey/20']}'></div>" for i in range(6))
    side = "".join(f"<div style='height:{8*s}px;width:{120*s}px;margin:{22*s}px 0;border-radius:{4*s}px;background:{COL['blue/100'] if i == 1 else COL['grey/50']}'></div>" for i in range(6))
    mock = (f"<div style='display:flex;height:100%'><div style='width:{220*s}px;background:{COL['grey/10']};padding:{40*s}px {36*s}px'>{side}</div>"
            f"<div style='flex:1;padding:{40*s}px {44*s}px'><div style='display:flex;justify-content:space-between'>"
            f"<div style='height:{14*s}px;width:{330*s}px;background:{COL['grey/160']};border-radius:{4*s}px'></div>"
            f"<div style='height:{28*s}px;width:{110*s}px;background:{COL['blue/100']};border-radius:{4*s}px'></div></div>"
            f"<div style='margin-top:{24*s}px'>{rows}</div></div></div>")
    return f"<div data-el='screenshot' data-sample='1' style='{base}'>{mock}</div>", True


CARD = {"soft-blue": ("blue/100", 1, "grey/160", "blue/100", "grey/120"),
        "brand-depth": ("base/white", 0.16, "base/white", "blue/40", "blue/20")}


def card(r, variant, photo, texts=None):
    x, y, w, h = r
    s = w / 400
    stage, op, cn, cr, cc = CARD[variant]
    diamond = svg_uri(A / "shapes" / "shape-diamond-solid.svg", colour(stage))
    parts = [f"<img src='{diamond}' style='position:absolute;left:{6*s}px;top:{88*s}px;width:{388*s}px;height:{388*s}px;opacity:{op}'>"]
    sample = not photo
    if photo:
        parts.append(f"<img src='{data_uri(photo)}' style='position:absolute;left:0;top:0;width:{400*s}px;height:{469*s}px;object-fit:contain;object-position:bottom center'>")
    else:
        sil = colour("grey/60") if variant == "soft-blue" else "#ffffff55"
        parts.append(f"<div style='position:absolute;left:{130*s}px;top:{150*s}px;width:{140*s}px;height:{140*s}px;border-radius:50%;background:{sil}'></div>"
                     f"<div style='position:absolute;left:{80*s}px;top:{310*s}px;width:{240*s}px;height:{159*s}px;border-radius:{120*s}px {120*s}px 0 0;background:{sil}'></div>")
    if texts:
        for (slot, ty, style, col) in (("name", 497, "h6/bold", cn), ("role", 543, "text-large/medium", cr), ("company", 573, "text-large/regular", cc)):
            st = TS[style]
            parts.append(f"<div data-el='stext' data-slot='speaker {slot}' style='position:absolute;left:{24*s}px;top:{ty*s}px;width:{352*s}px;white-space:nowrap;"
                         f"text-align:center;color:{colour(col)};font-size:{st['size']*s}px;font-weight:{WEIGHT[st['weight']]};line-height:{st['lineHeight']*s}px'>{html.escape(texts.get(slot,''))}</div>")
    return f"<div data-el='card' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px'>{''.join(parts)}</div>", sample



ICONLIB = json.load(open(A / "icons" / "icons.json"))["library"]


def icon_svg(name, col, size, weight="regular"):
    if name not in ICONLIB:
        raise SystemExit(f"Unknown icon '{name}'. Run: python icon.py list")
    i = ICONLIB[name][weight]
    return f"<svg viewBox='{i['viewBox']}' width='{size}' height='{size}' fill='currentColor' style='color:{col};display:block'>{i['body']}</svg>"


TILE = {"blue": ("blue/50", "blue/100", "blue/130", "blue/150"), "violet": ("violet/50", "violet/100", "violet/130", "violet/150")}


def tile3d(r, family, icon, alpha=1):
    """The CDS 3D tile: two bevels, gradient face, inner shade, gloss, hairline and rim light."""
    x, y, s, _ = r
    c50, c100, c130, c150 = (colour(t) for t in TILE[family])
    rad = s * 0.22
    face = (f"position:absolute;left:0;top:0;width:{s}px;height:{s}px;border-radius:{rad}px;"
            f"background:radial-gradient(64% 64% at 50% 56%, {c150}75, {c150}00 100%), linear-gradient(135deg, {c50} 0%, {c100} 34%, {c130} 100%);"
            f"box-shadow:inset {s*.011}px {s*.011}px 0 #ffffffd0, inset -{s*.004}px -{s*.004}px 0 #ffffff1a;overflow:hidden")
    gloss = f"position:absolute;left:-30%;top:-20%;width:125%;height:70%;background:linear-gradient(160deg,#ffffff4d 0%,#ffffff00 62%);transform:rotate(-8deg)"
    hair = f"position:absolute;left:{s*.055}px;top:{s*.055}px;width:{s*.89}px;height:{s*.89}px;border-radius:{rad*.8}px;border:{max(1.5, s/127)}px solid {c50}"
    ic = f"<div style='position:absolute;left:{s*.27}px;top:{s*.26}px'>{icon_svg(icon, '#ffffff', s*.46)}</div>" if icon else ""
    return (f"<div data-el='tile' style='position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{alpha}'>"
            f"<div style='position:absolute;left:{s*.075}px;top:{s*.075}px;width:{s}px;height:{s}px;border-radius:{rad}px;background:{c150}'></div>"
            f"<div style='position:absolute;left:{s*.039}px;top:{s*.039}px;width:{s}px;height:{s}px;border-radius:{rad}px;background:{c130}'></div>"
            f"<div style='{face}'><div style='{gloss}'></div></div><div style='{hair}'></div>{ic}</div>")


CENTRE_KEEP = {"Page counter", "Swipe cue", "Name", "Role"}   # slots that keep their place


def tag_style(brief, el, bold):
    """Social labels (Figma Tag › Chip, Outline, Eyebrow). A solid block reads as a button, so posts use:
    eyebrow on text-led layouts (statement versions: the headline carries the post), outline over photos
    and busy backgrounds (webinar speakers, Reels covers), and the soft chip everywhere else.
    `"tag_style": "chip" | "outline" | "eyebrow"` in the brief overrides it."""
    if brief.get("tag_style") in ("chip", "outline", "eyebrow"):
        return brief["tag_style"]
    ver, tpl = brief.get("version", ""), brief.get("template", "")
    if ver.startswith("statement"):
        return "eyebrow"
    if tpl in ("webinar", "reels-cover") or brief.get("photo"):
        return "outline"
    return "chip"


def centre_over_picture(v, W):
    """Design-lead alignment: when a picture is centred below the text (an illustration, not a framed
    screenshot), the tag, slide number, headline and supporting text above it are centred too, on a
    comfortable measure. Text beside a picture (Landscape, X) stays left-aligned. Content never changes."""
    shot = next((e for e in v["el"] if e["t"] == "screenshot"), None)
    if not shot:
        return v
    sx, sy, sw, sh = shot["r"]
    above = [e for e in v["el"] if e["t"] in ("text", "tag") and "r" in e and e.get("slot") not in CENTRE_KEEP
             and e["r"][1] + e["r"][3] <= sy + 10]
    beside = [e for e in v["el"] if e["t"] == "text" and "r" in e and e["r"][1] < sy + sh and e["r"][1] + e["r"][3] > sy + 10]
    if not above or beside:
        return v
    v = json.loads(json.dumps(v))
    margin = min(e["r"][0] for e in v["el"] if e["t"] in ("text", "tag", "lockup") and "r" in e)
    for e in v["el"]:
        if e["t"] not in ("text", "tag") or "r" not in e or e.get("slot") in CENTRE_KEEP or e["r"][1] + e["r"][3] > sy + 10:
            continue
        x, y, w, h = e["r"]
        if e["t"] == "tag":
            e["centre"] = W / 2
        else:
            full = W - 2 * margin
            ww = full if e.get("slot") in ("Headline", "Slide number") else min(w, full - 120)   # body on a shorter measure
            e["r"] = [round((W - ww) / 2), y, ww, h]
            e["align"] = "center"
    return v


def build(brief):
    t = LAYOUTS[brief["template"]]
    ver0 = brief.get("version", "default")
    if brief.get("illustration") and f"illustration-{ver0.split('-')[-1]}" in t["variants"] and ver0.startswith("product"):
        brief = dict(brief, version=f"illustration-{ver0.split('-')[-1]}")   # Feature: the Illustration layout (Figma Layout=Illustration)
    v = t["variants"][brief.get("version", "default")]
    if brief.get("illustration"):
        v = centre_over_picture(v, t["size"][0])
    W, H = t["size"]
    ver = brief.get("version", "default")
    implied = "ai" if ver.endswith("ai") else "partner" if ver.endswith("partner") else "default"
    topic = implied if implied != "default" else (brief.get("topic") or "default")   # an AI or partner version is that topic
    txt = brief.get("text", {})
    samples, html_el, bold = [], [], False
    for el in v["el"]:
        k = el["t"]
        if k == "bg":
            b, bold = background(el["style"], el["texture"], topic)
            html_el.append(b)
        elif k in ("lockup", "zoho"):
            x, y, w, h = el["r"]
            if k == "zoho" and topic == "partner" and (brief.get("partner_logo") or brief.get("logo")):
                continue  # Brand · Logo: no Zoho logo on pieces with the co-branded lockup
            f = ("creator-lockup" if k == "lockup" else "zoho-logo") + ("-white" if el["white"] else "-colour") + ".svg"
            html_el.append(f"<img data-el='{k}' src='{svg_uri(A / 'logos' / f)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px'>")
            plogo = brief.get("partner_logo") or brief.get("logo")
            if k == "lockup" and (el.get("cobrand") or (topic == "partner" and plogo)):
                # Brand · Logo 06: Creator first, thin divider, partner ~0.85x the lockup height, 0.3x gaps, one line
                gap, dh, ph = h * 0.30, h * 0.82, h * 0.85
                dx = x + w + gap
                divc = COL['grey/140'] if not el["white"] else "#ffffff66"   # grey/140 on light, white 40% on dark
                html_el.append(f"<div style='position:absolute;left:{dx}px;top:{y + (h - dh)/2}px;width:2px;height:{dh}px;background:{divc}'></div>")
                if plogo:
                    html_el.append(f"<img data-el='partnerlogo' src='{data_uri(plogo)}' style='position:absolute;left:{dx + 2 + gap}px;top:{y + (h - ph)/2}px;height:{ph}px;max-width:{w * 1.1}px;object-fit:contain;object-position:left center'>")
                else:
                    samples.append("partner logo (supply the partner's own logo file; keep its colours)")
                    html_el.append(f"<div style='position:absolute;left:{dx + 2 + gap}px;top:{y + (h - ph)/2}px;height:{ph}px;width:{w*0.9}px;border:2px dashed {COL['grey/60']};border-radius:6px;color:{COL['grey/120']};font-size:{ph*0.3}px;display:flex;align-items:center;justify-content:center'>Partner logo</div>")
        elif k == "tag":
            label = brief.get("tag", el["label"])
            if label == "":
                continue
            x, y, w, h = el["r"]
            style = tag_style(brief, el, bold)
            light_fg = COL["violet/100"] if topic in ("ai", "partner") else COL["blue/100"]
            light_bg = COL["violet/20"] if topic in ("ai", "partner") else COL["blue/20"]
            fg = "#ffffff" if bold else light_fg
            if style == "eyebrow":
                hh = round(max(h * 0.55, W * 0.026)); fs = round(hh * 0.66)
                box = f"height:{hh}px;line-height:{hh}px;font-size:{fs}px;letter-spacing:.14em;color:{fg}"
            else:
                hh = round(min(h, max(h * 0.8, W * 0.038))); fs = round(hh * 0.4)   # readable in the feed, never a big block
                fill = (f"background:{'rgba(255,255,255,.14)' if bold else light_bg}" if style == "chip"
                        else f"border:{max(1.5, h / 37):.1f}px solid {'rgba(255,255,255,.5)' if bold else light_fg}")
                box = (f"height:{hh}px;line-height:{hh - (3 if style == 'outline' else 0)}px;padding:0 {round(hh * 0.4)}px;"
                       f"border-radius:{hh}px;{fill};font-size:{fs}px;letter-spacing:.08em;color:{fg}")
            ty = y + (h - hh) / 2
            pos = f"left:{el['centre']}px;transform:translateX(-50%)" if el.get("centre") else f"left:{x}px"
            html_el.append(f"<div data-el='tag' data-style='{style}' style='position:absolute;{pos};top:{ty}px;box-sizing:border-box;{box};"
                           f"font-weight:600;text-transform:uppercase;white-space:nowrap'>{html.escape(label)}</div>")
            if "tag" not in brief:
                samples.append(f"tag '{label}' (sample label)")
        elif k == "text":
            x, y, w, h = el["r"]
            val = txt.get(el["slot"])
            if val is None:
                val = el["sample"]
                samples.append(f"{el['slot']} (sample text)")
            align = "right" if (RTL_RE.search(val) and el["align"] == "left") else el["align"]
            wrap = "text-wrap:balance;" if (el["slot"] in ("Headline", "Quote") or align == "center") else "text-wrap:pretty;"   # no lone last word
            steps = html.escape(json.dumps(smaller_styles(el)), quote=True)
            html_el.append(f"<div data-el='text' data-slot='{el['slot']}' data-h='{h}' data-steps=\"{steps}\" style='position:absolute;left:{x}px;top:{y}px;width:{w}px;{wrap}"
                           f"color:{colour(el['fill'])};text-align:{align};{rtl_css(val)}{text_css(el)}'>{rich(val, bold, topic, el.get('hl'))}</div>")
        elif k == "screenshot" and brief.get("illustration"):
            zone = el["r"] if brief.get("version", "").startswith("illustration") else illustration_zone(el["r"], v, W, H)
            html_el.append(illustration_slot(zone, brief["illustration"], bold))
            ip = Path(brief["illustration"])
            if ip.suffix.lower() != ".svg":
                samples.append(f"stock illustration {ip.name}: design review (licence, flat style, recoloured to CDS; run check_system.py on it)")
            elif 'data-cds-illustration="reference"' not in ip.read_text():
                samples.append(f"illustration {ip.name}: drawn in the CDS style, design review before publishing")
        elif k == "screenshot":
            c, s = screenshot_card(el["r"], brief.get("screenshot"))
            html_el.append(c)
            if s:
                samples.append("product screenshot (drawn sample: supply a real screenshot)")
        elif k == "card":
            c, s = card(el["r"], el["variant"], brief.get("photo"))
            html_el.append(c)
            if s:
                samples.append("speaker photo (supply a transparent cut-out PNG)")
        elif k == "speakers":
            sp = brief.get("speakers") or [{}] * len(el["cards"])
            for i, cd in enumerate(el["cards"][:len(sp)]):
                info = sp[i] if i < len(sp) else {}
                c, s = card(cd["r"], cd["variant"], info.get("photo"),
                            {"name": info.get("name", "Full Name"), "role": info.get("role", "Designation"), "company": info.get("company", "Zoho Creator")})
                html_el.append(c)
                if s:
                    samples.append(f"speaker {i+1} photo")
                if not info.get("name"):
                    samples.append(f"speaker {i+1} name and role")
        elif k == "glow":
            x, y, w, h = el["r"]; c = colour(el["colour"]); a = int(el["alpha"] * 255)
            html_el.append(f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:radial-gradient(closest-side,{c}{a:02x},{c}00)'></div>")
        elif k == "sparkle":
            x, y, w, h = el["r"]
            html_el.append(f"<div style='position:absolute;left:{x}px;top:{y}px;opacity:{el['alpha']}'>{icon_svg('sparkle', '#ffffff', w, 'fill')}</div>")
        elif k == "shadow":
            x, y, w, h = el["r"]
            html_el.append(f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:50%;background:radial-gradient(closest-side,#01030a99,#01030a00)'></div>")
        elif k == "tile":
            ic = brief.get(el.get("iconSlot") or "_", el.get("icon")) if el.get("iconSlot") else el.get("icon")
            if el.get("iconSlot") and el["iconSlot"] not in brief and el.get("icon"):
                samples.append(f"tile icon '{el['icon']}' (sample: pick an icon that fits the topic)")
            fam = el["family"]
            if topic == "ai" and fam == "blue" and el.get("iconSlot") == "icon" and brief["template"] != "youtube":
                fam = "violet"
            html_el.append(tile3d(el["r"], fam, ic, el.get("alpha", 1)))
        elif k == "eyebrow":
            x, y, w, h = el["r"]; size, weight = el["px"]
            val = txt.get(el["slot"]) or el["sample"]
            if el["slot"] not in txt: samples.append(f"{el['slot']} (sample text)")
            dia = svg_uri(A / "shapes" / "shape-diamond-solid.svg", colour(el["diamond"]))
            html_el.append(f"<div data-el='text' data-slot='{el['slot']}' data-h='{h+4}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;display:flex;align-items:center;gap:{size*0.4}px;"
                           f"color:{colour(el['fill'])};font-size:{size}px;font-weight:{weight};line-height:{h}px;letter-spacing:.06em;white-space:nowrap'>"
                           f"<img src='{dia}' style='width:{size*0.7}px;height:{size*0.7}px'>{html.escape(val.upper())}</div>")
        elif k == "highlightbox":
            x, y, w, h = el["r"]; size, weight = el["px"]
            val = txt.get(el["slot"])
            if val is None:
                val = el["sample"]; samples.append(f"{el['slot']} (sample text)")
            if val:
                html_el.append(f"<div data-el='text' data-slot='{el['slot']}' data-h='{h}' style='position:absolute;left:{x}px;top:{y}px;max-width:{w}px;background:{colour(el['bg'])};"
                               f"color:{colour(el['fill'])};font-size:{size}px;font-weight:{weight};line-height:{h - 9.5}px;padding:4.7px 9.5px;border-radius:6.3px;white-space:nowrap'>{html.escape(val)}</div>")
        elif k == "bubble":
            x, y, w, h = el["r"]; size, weight = el["px"]
            val = txt.get(el["slot"]) or el["sample"]
            if el["slot"] not in txt: samples.append(f"{el['slot']} (sample text)")
            html_el.append(f"<div data-el='text' data-slot='{el['slot']}' data-h='{h}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#fff;border-radius:{h*0.22}px;"
                           f"border:1px solid {COL['grey/40']};box-shadow:0 24px 48px -8px #00000040;display:flex;align-items:center;gap:14px;padding:0 22px;"
                           f"font-size:{size}px;font-weight:{weight};color:{COL['bluish-grey/180']};white-space:nowrap;overflow:hidden'>"
                           f"{icon_svg('ai-sparkle', COL['violet/100'], 26, 'fill')}<span style='flex:1;overflow:hidden;text-overflow:ellipsis'>{html.escape(val)}</span>"
                           f"<span style='width:2px;height:30px;background:{COL['blue/100']}'></span></div>")
        elif k == "photo":
            x, y, w, h = el["r"]; img = brief.get("photo")
            if img:
                outl = "filter:" + " ".join(f"drop-shadow({dx}px {dy}px 0 #fff)" for dx, dy in ((5,0),(-5,0),(0,5),(0,-5))) + ";" if el.get("outline") else ""
                html_el.append(f"<img data-el='photo' src='{data_uri(img)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:contain;object-position:bottom center;{outl}'>")
            else:
                samples.append("customer photo (supply a transparent cut-out PNG)")
                sil = "#ffffff99"
                html_el.append(f"<div style='position:absolute;left:{x+w*0.3}px;top:{y+h*0.1}px;width:{w*0.4}px;height:{w*0.4}px;border-radius:50%;background:{sil}'></div>"
                               f"<div style='position:absolute;left:{x+w*0.12}px;top:{y+h*0.55}px;width:{w*0.76}px;height:{h*0.45}px;border-radius:{w*0.38}px {w*0.38}px 0 0;background:{sil}'></div>")
        elif k == "customerlogo":
            x, y, w, h = el["r"]; img = brief.get("logo")
            if img:
                html_el.append(f"<img data-el='logo' src='{data_uri(img)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:contain;object-position:right center'>")
            else:
                samples.append("customer logo (supply the customer's own logo file; keep its colours)")
                html_el.append(f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:2px dashed {COL['grey/60']};border-radius:6px;color:{COL['grey/120']};font-size:18px;display:flex;align-items:center;justify-content:center'>Customer logo</div>")
        elif k == "rule":
            x, y, w, h = el["r"]
            html_el.append(f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{colour(el['fill'])}'></div>")
        elif k == "lowerthird":
            x, y, w, h = el["r"]
            html_el.append(f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{colour(el['fill'])};border-radius:{el['radius']}px'></div>")
            for tt in el["texts"]:
                tx, ty, tw, th = tt["r"]
                val = txt.get(tt["slot"]) or tt["sample"]
                if tt["slot"] not in txt:
                    samples.append(f"{tt['slot']} (sample text)")
                html_el.append(f"<div data-el='text' data-slot='{tt['slot']}' data-h='{th}' data-zone='lowerthird' style='position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;"
                               f"color:{colour(tt['fill'])};{text_css(tt)}'>{html.escape(val)}</div>")
    page = (f"<!doctype html><html><head><meta charset='utf-8'><meta name='cds-kind' content='social'><meta name='cds-topic' content='{topic}'><style>{font_css()}*{{margin:0;box-sizing:border-box}}"
            f"body{{width:{W}px;height:{H}px;overflow:hidden;font-family:{FONT_STACK}}}"
            f"#c{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}</style></head>"
            f"<body><div id='c'>{''.join(html_el)}</div></body></html>")
    return page, (W, H), v.get("safe"), samples


CHECK_JS = """(safe) => {
  const els=[...document.querySelectorAll('[data-el]')].filter(e=>!e.closest('[data-el=card]')||e.dataset.el==='card');
  const box=e=>{const r=e.getBoundingClientRect();return {zone:e.dataset.zone||'',el:e.dataset.el,slot:e.dataset.slot||'',x:r.x,y:r.y,w:r.width,h:r.height,max:+(e.dataset.h||0)}};
  const b=els.map(box); const out={overflow:[],overlap:[],outside:[]};
  for(const x of b){ if(x.el==='text' && x.max && x.h>x.max*1.02) out.overflow.push(`${x.slot}: ${Math.round(x.h)}px tall, the slot holds ${x.max}px`);
    if(safe && !x.zone && ['text','tag','lockup','zoho'].includes(x.el) && (x.x<safe[0]-1||x.y<safe[1]-1||x.x+x.w>safe[0]+safe[2]+1||x.y+x.h>safe[1]+safe[3]+1)) out.outside.push(x.slot||x.el); }
  const hit=(a,c)=>a.x<c.x+c.w-1&&c.x<a.x+a.w-1&&a.y<c.y+c.h-1&&c.y<a.y+a.h-1;
  for(let i=0;i<b.length;i++) for(let j=i+1;j<b.length;j++){ const a=b[i],c=b[j];
    if(a.el==='text'&&c.el==='text'&&hit(a,c)) out.overlap.push(`${a.slot} overlaps ${c.slot}`);
    if(((a.el==='text'&&['screenshot','tag','zoho','lockup'].includes(c.el))||(c.el==='text'&&['screenshot','tag','zoho','lockup'].includes(a.el)))&&hit(a,c)) out.overlap.push(`${a.slot||a.el} overlaps ${c.slot||c.el}`); }
  out.speaker=[...document.querySelectorAll('[data-el=stext]')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.dataset.slot);
  return out; }"""


FLOW_JS = r"""([G, safe]) => {
  // Design-lead layout: the template is a starting point, not a fixed grid. Text takes the height its content
  // needs; when it is longer, the picture below moves down and gets shorter; when it is shorter, the picture moves
  // up and gets taller. If the picture would get too small, the headline (then the body) steps down to the next
  // CDS text style, at most two steps. Nothing is cut and the words never change.
  const out = {fixed: [], tooLong: []};
  const R = e => e.getBoundingClientRect();
  const pic = document.querySelector("[data-el='screenshot']");
  const KEEP = ['Page counter', 'Swipe cue', 'Name', 'Role', 'Prompt'];
  const all = [...document.querySelectorAll("[data-el='text'],[data-el='tag']")].filter(t => !KEEP.includes(t.dataset.slot));
  const stepDown = t => { const st = JSON.parse(t.dataset.steps || '[]'); const i = +(t.dataset.step || 0);
    if (i >= st.length) return false; t.style.cssText += ';' + st[i]; t.dataset.step = i + 1; return true; };
  if (pic) {
    const p0 = R(pic), isIll = !!pic.querySelector('svg[data-cds-illustration]') || !!pic.querySelector('img') && !pic.style.borderRadius;
    const stack = all.filter(t => R(t).top < p0.top && R(t).left < p0.right && R(t).right > p0.left).sort((a, b) => R(a).top - R(b).top);
    if (stack.length) {
      const slotH = t => t.dataset.el === 'tag' ? R(t).height : +t.dataset.h;
      const tops = stack.map(t => parseFloat(t.style.top));
      const gaps = stack.map((t, i) => (i + 1 < stack.length ? tops[i + 1] : p0.top) - (tops[i] + slotH(t)));
      const bottom = p0.bottom, minH = p0.height * 0.6, maxH = p0.height * (isIll ? 1.35 : 1.2);
      // text to picture: at least G, at most 6% of the width, so the text and the picture read together
      const PICGAP = Math.max(G, Math.round(R(document.querySelector('#c')).width * 0.06));
      const layout = () => { let y = tops[0];
        stack.forEach((t, i) => { t.style.top = y + 'px'; const h = R(t).height; if (t.dataset.el === 'text') t.dataset.h = Math.ceil(h);
          y += h + (i + 1 < stack.length ? Math.max(gaps[i], 12) : Math.min(Math.max(gaps[i], G), PICGAP)); });
        return y; };
      let top = layout();
      const big = [...stack].filter(t => t.dataset.el === 'text').sort((a, b) => parseFloat(getComputedStyle(b).fontSize) - parseFloat(getComputedStyle(a).fontSize));
      while (bottom - top < minH) {
        const t = big.find(x => +(x.dataset.step || 0) < JSON.parse(x.dataset.steps || '[]').length && (x === big[0] || +(big[0].dataset.step || 0) >= 1));
        if (!t || !stepDown(t)) break;
        out.fixed.push(`${t.dataset.slot}: one CDS size smaller to fit the content`); top = layout();
      }
      let h = bottom - top;
      if (h < minH) { out.tooLong.push(`${stack.map(t => t.dataset.slot || 'tag').join(' + ')} leave only ${Math.round(h)}px for the picture`); h = minH; }
      if (h > maxH) { top += (h - maxH) / 2; h = maxH; }   // short text: the picture grows to its limit, then sits centred in the room left
      const r = R(pic); const dTop = top - r.top;
      if (Math.abs(dTop) > 2 || Math.abs(h - r.height) > 2) {
        pic.style.top = (parseFloat(pic.style.top) + dTop) + 'px'; pic.style.height = h + 'px';
        if (!isIll && pic.style.width) { const w0 = parseFloat(pic.style.width), w1 = Math.min(w0 * h / r.height, w0 * 1.15);
          pic.style.left = (parseFloat(pic.style.left) + (w0 - w1) / 2) + 'px'; pic.style.width = w1 + 'px'; }
        if (Math.abs(dTop) > 2) out.fixed.push(`picture ${dTop > 0 ? 'moved down' : 'moved up'} ${Math.round(Math.abs(dTop))}px to sit close to the text`);
      }
    }
  }
  // text beside a picture or with no picture (Landscape, X, statement layouts): a column that grows downward.
  // Blocks keep their template place unless the one above needs the room; the last may grow to the safe area.
  const done = new Set(pic ? all.filter(t => { const a = R(t), b = R(pic); return a.top < b.top && a.left < b.right && a.right > b.left; }) : []);
  const col = all.filter(t => !done.has(t) && t.dataset.el === 'text').sort((a, b) => parseFloat(a.style.top) - parseFloat(b.style.top));
  if (col.length) {
    const tops = col.map(t => parseFloat(t.style.top)), slots = col.map(t => +t.dataset.h);
    // a block the template already places below the safe area (a video lower third) keeps its own floor
    const limit = Math.max(safe ? safe[1] + safe[3] : 1e9, tops[col.length - 1] + slots[col.length - 1]);
    const blockers = [...document.querySelectorAll("[data-el='zoho'],[data-el='lockup'],[data-el='screenshot'],[data-el='tile']")].map(R);
    // text beside a picture keeps G px clear of it: set the measure first, then flow, so the wrap is final
    if (pic) col.forEach(t => { const a = R(t), b = R(pic);
      if (a.left < b.left && a.right > b.left - G) { t.style.width = Math.max(200, b.left - G - a.left) + 'px'; } });
    const flowCol = () => { let prevBottom = -1e9, last = 0;
      col.forEach((t, i) => { const gap = i ? Math.max(tops[i] - (tops[i - 1] + slots[i - 1]), 16) : 0;
        const y = i ? Math.max(tops[i], prevBottom + gap) : tops[i]; t.style.top = y + 'px';
        prevBottom = y + R(t).height; last = prevBottom; });
      const a = R(col[col.length - 1]);
      const hitsLogo = blockers.some(b => a.left < b.right && a.right > b.left && a.bottom > b.top && a.top < b.bottom);
      return last <= limit && !hitsLogo; };
    const order = [...col].sort((a, b) => parseFloat(getComputedStyle(b).fontSize) - parseFloat(getComputedStyle(a).fontSize));
    let ok = flowCol(), guard = 0;
    while (!ok && guard++ < 4) { const t = order.find(x => +(x.dataset.step || 0) < Math.min(2, JSON.parse(x.dataset.steps || '[]').length));
      if (!t) break; stepDown(t); out.fixed.push(`${t.dataset.slot}: one CDS size smaller to fit the content`); ok = flowCol(); }
    // short copy beside a picture: don't leave the template's gaps half empty; set the tag and text as one
    // compact group, centred on the picture
    const besidePic = pic && col.every(t => R(t).right <= R(pic).left + 4);
    if (ok && besidePic) {
      const tag = all.find(t => t.dataset.el === 'tag' && R(t).right <= R(pic).left + 4);
      const group = (tag ? [tag] : []).concat(col);
      const hs = group.map(t => R(t).height), lh = parseFloat(getComputedStyle(col[0]).lineHeight) || 60;
      const gaps = group.map((t, i) => i === 0 ? 0 : (group[i - 1] === tag ? Math.max(20, lh * 0.3) : Math.max(24, lh * 0.4)));
      const total = hs.reduce((a, b) => a + b, 0) + gaps.reduce((a, b) => a + b, 0);
      const span = R(group[group.length - 1]).bottom - R(group[0]).top;
      if (total < span - 40) {
        const lock = document.querySelector("[data-el='lockup']"), p = R(pic);
        const minTop = lock ? R(lock).bottom + 40 : R(group[0]).top;
        let y = Math.max(minTop, Math.min(p.top + p.height / 2 - total / 2, (safe ? safe[1] + safe[3] : 1e9) - total));
        group.forEach((t, i) => { y += gaps[i]; t.style.top = y + 'px'; y += hs[i]; });
        out.fixed.push('short text: set as one group, centred on the picture');
      }
    }
    if (ok) col.forEach(t => { t.dataset.h = Math.ceil(R(t).height); });
    else out.tooLong.push(`${col.map(t => t.dataset.slot).join(' + ')} run past the safe area`);
  }
  return out;
}"""


RHYTHM_JS = r"""(safe) => {
  // Design-lead rhythm: the gap from the tag (or eyebrow) to the headline, and from the headline to the line under
  // it (supporting text, date), is 0.4 x the headline size, never under 16px, in every template and tone. Measured
  // on the letters, not the boxes. Blocks below move with it; a picture under them gives up (or takes back) the room.
  const out = {fixed: []};
  const H = document.querySelector("[data-slot='Headline']");
  if (!H || !H.textContent.trim()) return out;
  const glyph = el => { const r = document.createRange(); r.selectNodeContents(el); const rs = [...r.getClientRects()].filter(x => x.width && x.height);
    return rs.length ? {top: Math.min(...rs.map(x => x.top)), bottom: Math.max(...rs.map(x => x.bottom))} : el.getBoundingClientRect(); };
  const R = e => e.getBoundingClientRect();
  const fs = parseFloat(getComputedStyle(H).fontSize), V = Math.max(16, Math.round(fs * 0.4));
  const cols = (a, b) => R(a).left < R(b).right - 2 && R(a).right > R(b).left + 2;
  const texts = [...document.querySelectorAll("[data-el='text'],[data-el='tag']")].filter(t => t.textContent.trim());
  const pic = document.querySelector("[data-el='screenshot']");
  const limit = safe ? safe[1] + safe[3] : 1e9;
  const shiftBelow = (from, d, label) => {
    const y0 = R(from).top - 2;
    const CH = R(document.querySelector('#c')).height, FOOT = ['Page counter', 'Swipe cue', 'Prompt', 'Name', 'Role'];
    const movers = texts.filter(t => R(t).top >= y0 && cols(t, from) && !FOOT.includes(t.dataset.slot) && R(t).top < CH * 0.85);
    const lastBottom = Math.max(...movers.map(t => glyph(t).bottom));
    const picBelow = pic && R(pic).top >= y0 && cols(pic, from);
    if (d > 0 && !picBelow && lastBottom + d > limit) d = Math.max(0, limit - lastBottom);
    if (Math.abs(d) < 2) return;
    movers.forEach(t => { t.style.top = (parseFloat(t.style.top) + d) + 'px'; });
    if (picBelow && pic.style.height) { pic.style.top = (parseFloat(pic.style.top) + d) + 'px'; pic.style.height = (parseFloat(pic.style.height) - d) + 'px'; }
    out.fixed.push(`${label}: gap set to ${V}px (0.4 x the headline size)`);
  };
  // above: tag or eyebrow -> headline (the headline and everything under it move)
  const above = texts.filter(t => t !== H && cols(t, H) && glyph(t).bottom <= glyph(H).top + 2 && (t.dataset.el === 'tag' || t.dataset.slot === 'Eyebrow'))
    .sort((a, b) => glyph(b).bottom - glyph(a).bottom)[0];
  if (above) shiftBelow(H, V - (glyph(H).top - glyph(above).bottom), `${above.dataset.slot || 'tag'} to Headline`);
  // below: headline -> supporting text / date
  const NEXT = ['Supporting text', 'Date and time', 'Date', 'Subline', 'Body'];
  const below = texts.filter(t => t !== H && cols(t, H) && NEXT.includes(t.dataset.slot) && glyph(t).top >= glyph(H).bottom - 2)
    .sort((a, b) => glyph(a).top - glyph(b).top)[0];
  if (below) shiftBelow(below, V - (glyph(below).top - glyph(H).bottom), `Headline to ${below.dataset.slot}`);
  return out;
}"""


SPACE_JS = r"""(G) => {
  // Design-lead spacing: text never sits close to a picture. Keep at least G px between any text block and a
  // screenshot, illustration, tile, photo or card: move or shrink the picture, or narrow text beside it.
  const H = document.querySelector('#c').getBoundingClientRect().height;
  const txt = el => { const r = document.createRange(); r.selectNodeContents(el); const rs = [...r.getClientRects()].filter(x => x.width && x.height);
    if (!rs.length) return el.getBoundingClientRect();
    return {left: Math.min(...rs.map(x => x.left)), right: Math.max(...rs.map(x => x.right)), top: Math.min(...rs.map(x => x.top)), bottom: Math.max(...rs.map(x => x.bottom))}; };
  const pic = el => { const s = el.querySelector('svg[data-cds-illustration]');
    if (!s) return el.getBoundingClientRect();
    const rs = [...s.children].filter(c => c.tagName !== 'script').map(c => c.getBoundingClientRect()).filter(x => x.width && x.height);
    return {left: Math.min(...rs.map(x => x.left)), right: Math.max(...rs.map(x => x.right)), top: Math.min(...rs.map(x => x.top)), bottom: Math.max(...rs.map(x => x.bottom))}; };
  const out = {fixed: [], close: []};
  // speaker cards, cut-out photos and the chat bubble on a tile are layered on purpose in the templates
  const pics = [...document.querySelectorAll("[data-el='screenshot'],[data-el='tile']")];
  const texts = [...document.querySelectorAll("[data-el='text'],[data-el='tag']")].filter(t => t.textContent.trim() && !['Prompt', 'Name', 'Role'].includes(t.dataset.slot));
  for (let pass = 0; pass < 3; pass++) for (const p of pics) for (const t of texts) {
    const a = txt(t), b = pic(p), name = t.dataset.slot || 'tag';
    const overlapX = a.left < b.right && a.right > b.left, overlapY = a.top < b.bottom && a.bottom > b.top;
    if (overlapX && a.bottom <= b.top + 4 && b.top - a.bottom < G) {             // text above the picture
      const need = Math.ceil(G - (b.top - a.bottom)), r = p.getBoundingClientRect();
      if (p.querySelector('svg[data-cds-illustration]') || p.querySelector('img') && p.dataset.el === 'screenshot' && !p.style.borderRadius) {
        p.style.top = (parseFloat(p.style.top) + need) + 'px'; p.style.height = (r.height - need) + 'px';   // the illustration refits
      } else if (r.bottom + need <= H - 40) { p.style.top = (parseFloat(p.style.top) + need) + 'px'; }
      else { out.close.push(`${name} is ${Math.round(b.top - a.bottom)}px from the picture (needs ${G})`); continue; }
      out.fixed.push(`${name}: picture moved ${need}px further away`);
    } else if (overlapY && a.right <= b.left + 4 && b.left - a.right < G) {     // text left of the picture
      const need = Math.ceil(G - (b.left - a.right)), w = t.getBoundingClientRect().width;
      t.style.width = (w - need) + 'px'; t.style.maxWidth = (w - need) + 'px';
      out.fixed.push(`${name}: text measure narrowed ${need}px to keep clear of the picture`);
    } else if (overlapX && overlapY) {
      out.close.push(`${name} touches the picture`);
    }
  }
  return out;
}"""


def render(brief_path, out_png):
    brief = json.load(open(brief_path))
    from check_system import guard; guard(brief, sys.argv)
    page, (W, H), safe, samples = build(brief)
    out_png = Path(out_png)
    out_html = out_png.with_suffix(".html")
    out_html.write_text(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(out_html.resolve().as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(250)
        flow = pg.evaluate(FLOW_JS, [max(40, round(W * 0.04)), safe])
        pg.wait_for_timeout(80)
        rhythm = pg.evaluate(RHYTHM_JS, safe)
        flow["fixed"] += rhythm["fixed"]
        space = pg.evaluate(SPACE_JS, max(40, round(W * 0.04)))   # minimum gap between text and any picture
        pg.wait_for_timeout(100)
        res = pg.evaluate(CHECK_JS, safe)
        pg.locator("#c").screenshot(path=str(out_png))
        b.close()
    errors = [f"Text too long — {o}. Even two CDS sizes smaller it doesn't fit; shorten it (ask the person first)." for o in res["overflow"]]
    errors += [f"Text too long — {o}. Shorten it (ask the person first) or use a version with more room." for o in flow["tooLong"]]
    errors += [f"Collision — {o}." for o in res["overlap"]]
    errors += [f"Outside the safe area — {o}." for o in res["outside"]]
    errors += [f"Too close — {o}. Shorten the text or use a version with more room." for o in dict.fromkeys(space["close"])]
    errors += [f"Too long for the speaker card — {o}. Shorten it (e.g. first and last name, a shorter job title)." for o in res.get("speaker", [])]
    print(f"Saved {out_png} ({W}×{H}) and {out_html.name}")
    for f in dict.fromkeys(flow["fixed"]):
        print("  layout:", f)
    for f in dict.fromkeys(space["fixed"]):
        print("  spacing:", f)
    print("BRAND CHECK")
    print("Errors: none" if not errors else "Errors:")
    for e in errors:
        print("  ✗", e)
    print("To replace before publishing:" if samples else "To replace: none")
    for s in samples:
        print("  •", s)
    return 1 if errors else 0


if __name__ == "__main__":
    import os; os.environ["CDS_ALLOW_VIOLATION"] = "1" if "--allow-violation" in sys.argv else os.environ.get("CDS_ALLOW_VIOLATION", ""); sys.argv = [x for x in sys.argv if x != "--allow-violation"]
    a = sys.argv[1:]
    if not a or a[0] == "list":
        for k, t in LAYOUTS.items():
            print(f"{k:18} {t['size'][0]}×{t['size'][1]:<5} versions: {', '.join(t['variants'])}   ({t['name']})")
    elif a[0] == "slots":
        t = LAYOUTS[a[1]]
        for vk, v in t["variants"].items():
            slots = [f"{e['slot']} (≈{e['r'][3]}px tall)" for e in v["el"] if e["t"] == "text"]
            extra = [e["t"] for e in v["el"] if e["t"] in ("tag", "screenshot", "card", "speakers", "lowerthird")]
            print(f"{vk}: text slots: {', '.join(slots) or '—'}; also: {', '.join(extra) or '—'}")
    else:
        sys.exit(render(a[0], a[1]))
