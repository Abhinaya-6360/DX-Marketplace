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


def font_css():
    out = []
    for w, n in WEIGHT.items():
        out.append(f"@font-face{{font-family:'Zoho Puvi';font-weight:{n};"
                   f"src:url('{data_uri(A / 'fonts' / f'Zoho-Puvi-{w.capitalize()}.ttf')}');}}")
    return "\n".join(out)


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


def rich(text, tone_bold, topic, hl=None):
    t = html.escape(text).replace("\n", "<br>")
    if hl:
        span = f"<span style='color:{colour(hl)}'>\\1</span>"
    elif topic in ("ai", "partner"):
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
            if k == "zoho" and topic == "partner" and (brief.get("partner_logo") or brief.get("logo")):
                continue  # Brand · Logo: no Zoho logo on pieces with the co-branded lockup
            f = ("creator-lockup" if k == "lockup" else "zoho-logo") + ("-white" if el["white"] else "-colour") + ".svg"
            html_el.append(f"<img data-el='{k}' src='{svg_uri(A / 'logos' / f)}' style='position:absolute;left:{x}px;top:{y}px;width:{w}px'>")
            plogo = brief.get("partner_logo") or brief.get("logo")
            if k == "lockup" and (el.get("cobrand") or (topic == "partner" and plogo)):
                # Brand · Logo 06: Creator first, thin divider, partner ~0.78x the lockup height, 0.23x gaps, one line
                gap, dh, ph = h * 0.23, h * 0.77, h * 0.78
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
                           f"color:{colour(el['fill'])};text-align:{el['align']};{text_css(el)}'>{rich(val, bold, topic, el.get('hl'))}</div>")
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
