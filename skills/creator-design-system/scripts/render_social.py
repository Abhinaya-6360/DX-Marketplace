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
  "screenshot": "/path/screen.png", # optional: product screenshot for the card
  "photo": "/path/cutout.png",      # optional: Quote speaker (transparent cut-out PNG)
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


def font_css():
    out = []
    for w, n in WEIGHT.items():
        out.append(f"@font-face{{font-family:'Zoho Puvi';font-weight:{n};"
                   f"src:url('{data_uri(A / 'fonts' / f'Zoho-Puvi-{w.capitalize()}.ttf')}');}}")
    return "\n".join(out)


def text_css(el):
    if "px" in el:
        size, weight = el["px"]
        lh = round(size * 1.25)
        ls = "-0.01em"
    else:
        s = TS[el["style"]]
        size, weight, lh = s["size"], WEIGHT[s["weight"]], s["lineHeight"]
        ls = f"{float(s['letterSpacing'][:-1]) / 100}em"
    return f"font-size:{size}px;font-weight:{weight};line-height:{lh}px;letter-spacing:{ls};"


def rich(text, tone_bold, topic):
    t = html.escape(text).replace("\n", "<br>")
    if topic in ("ai", "partner"):
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
        style, texture = ("midnight", 0.12 if texture else 0) if bold else ("mesh-partner", 0)
    g = TOKENS["gradients"][style]["css"]
    tile = A / "patterns" / ("connect-tile-bold.svg" if bold else "connect-tile-light.svg")
    tex = (f"<div style='position:absolute;inset:0;background:url({svg_uri(tile)}) 0 0/480px 480px;"
           f"opacity:{texture}'></div>") if texture else ""
    return f"<div style='position:absolute;inset:0;background:{g}'></div>{tex}", bold


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
            parts.append(f"<div data-el='text' data-slot='speaker {slot}' style='position:absolute;left:{24*s}px;top:{ty*s}px;width:{352*s}px;"
                         f"text-align:center;color:{colour(col)};font-size:{st['size']*s}px;font-weight:{WEIGHT[st['weight']]};line-height:{st['lineHeight']*s}px'>{html.escape(texts.get(slot,''))}</div>")
    return f"<div data-el='card' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px'>{''.join(parts)}</div>", sample


def build(brief):
    t = LAYOUTS[brief["template"]]
    v = t["variants"][brief.get("version", "default")]
    W, H = t["size"]
    topic = brief.get("topic", "default")
    txt = brief.get("text", {})
    samples, html_el, bold = [], [], False
    for el in v["el"]:
        k = el["t"]
        if k == "bg":
            b, bold = background(el["style"], el["texture"], topic)
            html_el.append(b)
        elif k in ("lockup", "zoho"):
            x, y, w, h = el["r"]
            f = ("creator-lockup" if k == "lockup" else "zoho-logo") + ("-white" if el["white"] else "-colour") + ".svg"
            html_el.append(f"<img data-el='{k}' src='{svg_uri(A / 'logos' / f)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px'>")
        elif k == "tag":
            label = brief.get("tag", el["label"])
            if label == "":
                continue
            x, y, w, h = el["r"]
            s = h / 40
            c = el["colour"]
            if topic == "ai" and not bold and c == "blue":
                c = "violet"
            bgc, fg = TAG[c]
            html_el.append(f"<div data-el='tag' style='position:absolute;left:{x}px;top:{y}px;height:{h}px;padding:0 {20*s}px;border-radius:{4*s}px;"
                           f"background:{colour(bgc)};color:{colour(fg)};font-size:{16*s}px;font-weight:600;line-height:{h}px;white-space:nowrap'>{html.escape(label)}</div>")
            if "tag" not in brief:
                samples.append(f"tag '{label}' (sample label)")
        elif k == "text":
            x, y, w, h = el["r"]
            val = txt.get(el["slot"])
            if val is None:
                val = el["sample"]
                samples.append(f"{el['slot']} (sample text)")
            html_el.append(f"<div data-el='text' data-slot='{el['slot']}' data-h='{h}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px;"
                           f"color:{colour(el['fill'])};text-align:{el['align']};{text_css(el)}'>{rich(val, bold, topic)}</div>")
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
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css()}*{{margin:0;box-sizing:border-box}}"
            f"body{{width:{W}px;height:{H}px;overflow:hidden;font-family:'Zoho Puvi',Arial,sans-serif}}"
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
  return out; }"""


def render(brief_path, out_png):
    brief = json.load(open(brief_path))
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
        res = pg.evaluate(CHECK_JS, safe)
        pg.locator("#c").screenshot(path=str(out_png))
        b.close()
    errors = [f"Text too long — {o}. Shorten it; don't change the size." for o in res["overflow"]]
    errors += [f"Collision — {o}." for o in res["overlap"]]
    errors += [f"Outside the safe area — {o}." for o in res["outside"]]
    print(f"Saved {out_png} ({W}×{H}) and {out_html.name}")
    print("BRAND CHECK")
    print("Errors: none" if not errors else "Errors:")
    for e in errors:
        print("  ✗", e)
    print("To replace before publishing:" if samples else "To replace: none")
    for s in samples:
        print("  •", s)
    return 1 if errors else 0


if __name__ == "__main__":
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
