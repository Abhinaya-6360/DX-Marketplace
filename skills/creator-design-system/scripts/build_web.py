"""Build a zoho.com/creator page draft from the CDS 2.0 web sections.

Usage:
  python build_web.py page.json out.html [--preview out.png]

page.json:
{
  "title": "AI in Zoho Creator",
  "topic": "ai",                                   # default | ai | partner
  "sections": [
    {"type": "nav"},
    {"type": "hero", "tag": "NEW", "headline": "Describe your app. **AI builds** it.",
     "body": "One or two sentences.", "primary": "Start free trial", "secondary": "Book a demo",
     "screenshot": "/path/screen.png"},
    {"type": "features", "eyebrow": "HOW IT HELPS", "title": "From idea to app, faster",
     "description": "One line.", "cards": [{"icon": "ai-sparkle", "title": "Start from a sentence", "text": "…"}]},
    {"type": "stats", "eyebrow": "RESULTS", "title": "What teams see", "stats": [{"value": "3×", "label": "faster delivery", "source": "Internal survey, 2026"}]},
    {"type": "cta", "headline": "Build your next app today", "body": "Free for 15 days.", "primary": "Start free trial", "secondary": "Talk to sales"},
    {"type": "footer"}
  ]
}

Sections follow Templates · Web (1720 grid, 1320 content). Topic sets the hero, panel, CTA band,
eyebrows and icon tiles (brand-rules.md). One red button per section. Output is a responsive,
self-contained HTML draft for design and dev review — never production code.
"""
import base64, html, json, re, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
A = SKILL / "assets"
TOK = json.load(open(SKILL / "design-system" / "tokens.json"))
C = TOK["colour"]; G = {k: v["css"] for k, v in TOK["gradients"].items()}
ICONS = json.load(open(A / "icons" / "icons.json"))["library"]


def b64(p, mt):
    return f"data:{mt};base64,{base64.b64encode(Path(p).read_bytes()).decode()}"


def logo(name):
    return b64(A / "logos" / name, "image/svg+xml")


def icon(name, colour, size=24):
    if name not in ICONS:
        raise SystemExit(f"Unknown icon '{name}'. Run: python icon.py list")
    i = ICONS[name]["regular"]
    return f"<svg viewBox='{i['viewBox']}' width='{size}' height='{size}' fill='currentColor' style='color:{colour}'>{i['body']}</svg>"


def esc(t):
    return html.escape(t or "")


def rich(t, col):
    return re.sub(r"\*\*(.+?)\*\*", rf"<span style='color:{col}'>\1</span>", esc(t))


def btn(label, kind, size="lg", arrow=False):
    if not label:
        return ""
    a = " →" if arrow else ""
    return f"<a class='btn {kind} {size}' href='#'>{esc(label)}{a}</a>"


def build(page):
    topic = page.get("topic", "default")
    accent = C["violet/100"] if topic in ("ai", "partner") else C["blue/100"]
    tile_bg, tile_fg = (C["violet/20"], C["violet/100"]) if topic == "ai" else (C["blue/20"], C["blue/100"])
    hero_bg = {"default": G["soft-blue"], "ai": G["soft-violet"], "partner": G["mesh-partner"]}[topic]
    tex_bold = b64(A / "patterns" / "connect-tile-bold.svg", "image/svg+xml")
    tex_light = b64(A / "patterns" / "connect-tile-light.svg", "image/svg+xml")
    if topic == "default":
        panel = f"background:{C['blue/100']} url({tex_light}) 0 0/480px;"
        cta_bg = f"background:{C['blue/100']};"
        cta_tex = f"<div class='tex' style='background-image:url({tex_light});opacity:.35'></div>"
    elif topic == "ai":
        panel = f"background:{G['ai']};"; cta_bg = f"background:{G['ai']};"; cta_tex = ""
    else:
        panel = f"background:#fff;border:1px solid {C['grey/40']};box-shadow:0 40px 80px -16px #00000029;"
        cta_bg = f"background:{G['midnight']};"; cta_tex = f"<div class='tex' style='background-image:url({tex_bold});opacity:.12'></div>"
    fonts = "".join(f"@font-face{{font-family:'Zoho Puvi';font-weight:{n};src:url('{b64(A/'fonts'/f'Zoho-Puvi-{w}.ttf','font/ttf')}')}}"
                    for w, n in (("Regular", 400), ("Medium", 500), ("Semibold", 600), ("Bold", 700)))
    css = f"""{fonts}
*{{box-sizing:border-box;margin:0}} body{{font-family:'Zoho Puvi',Arial,sans-serif;color:{C['grey/160']};background:#fff}}
.wrap{{max-width:1320px;margin:0 auto;padding:0 24px}} section{{position:relative;overflow:hidden}}
.tex{{position:absolute;inset:0;background-size:480px 480px;pointer-events:none}}
.btn{{display:inline-flex;align-items:center;gap:12px;border-radius:4px;font-weight:600;text-decoration:none;white-space:nowrap}}
.btn.lg{{height:72px;padding:0 32px;font-size:20px}} .btn.sm{{height:56px;padding:0 24px;font-size:16px}}
.btn.primary{{background:{C['red/90']};color:#fff}} .btn.primary:hover{{background:{C['red/100']}}}
.btn.secondary{{border:2px solid {C['blue/100']};color:{C['blue/100']}}} .btn.inverse{{background:#fff;color:{C['blue/100']}}}
nav{{height:80px;border-bottom:1px solid {C['grey/40']};background:#fff;position:sticky;top:0;z-index:5}}
nav .wrap{{display:flex;align-items:center;height:100%;gap:32px}} nav .links{{display:flex;gap:32px;flex:1}}
nav a.l{{color:{C['grey/160']};text-decoration:none;font-weight:500;font-size:16px}} nav a.l:hover{{color:{C['blue/100']}}}
.hero{{padding:120px 0}} .hero .wrap{{display:grid;grid-template-columns:1fr 640px;gap:64px;align-items:center}}
.tag{{display:inline-block;height:40px;line-height:40px;padding:0 20px;border-radius:4px;font-weight:600;font-size:16px;color:#fff;background:{accent if topic != 'default' else C['blue/100']}}}
h1{{font-size:72px;line-height:80px;letter-spacing:-.03em;font-weight:700;margin:24px 0}} .lead{{font-size:20px;line-height:28px;color:{C['grey/120']};max-width:560px}}
.btns{{display:flex;gap:16px;margin-top:32px;flex-wrap:wrap}}
.panel{{position:relative;height:520px;border-radius:24px;overflow:hidden;{panel}}}
.shot{{position:absolute;left:72px;top:96px;width:620px;height:384px;border-radius:24px;background:#fff;border:1px solid {C['grey/40']};box-shadow:0 40px 80px -16px #00000029;overflow:hidden}}
.shot img{{width:100%;height:100%;object-fit:cover;object-position:top left}}
.sec{{padding:120px 0}} .head{{text-align:center;max-width:900px;margin:0 auto 64px}}
.eyebrow{{font-size:16px;font-weight:600;color:{accent};margin-bottom:8px}} h2{{font-size:48px;line-height:56px;letter-spacing:-.02em;font-weight:700}}
.desc{{font-size:16px;line-height:24px;color:{C['grey/130']};margin-top:8px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}
.card{{background:#fff;border:1px solid {C['grey/40']};border-radius:24px;padding:32px}}
.tile{{width:48px;height:48px;border-radius:4px;background:{tile_bg};display:flex;align-items:center;justify-content:center;margin-bottom:16px}}
.card h3{{font-size:32px;line-height:40px;font-weight:600;letter-spacing:-.01em;margin-bottom:16px}} .card p{{font-size:16px;line-height:24px;color:{C['grey/120']}}}
.stats{{background:{C['blue/10']}}} .statrow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px}}
.stat{{background:{C['blue/10']};border-radius:8px;padding:24px 28px}} .stat .v{{font-size:88px;line-height:96px;font-weight:700;letter-spacing:-.03em;color:{accent if topic=='ai' else C['blue/100']}}}
.stat .lb{{font-size:20px;line-height:28px;color:{C['grey/130']}}} .stat .src{{font-size:12px;color:{C['grey/120']};margin-top:4px}}
.cta{{padding:120px 0;text-align:center;color:#fff;{cta_bg}}} .cta h2{{font-size:56px;line-height:64px;color:#fff}} .cta p{{font-size:20px;line-height:28px;margin-top:24px}}
.cta .btns{{justify-content:center}}
footer{{background:{C['blue/160']};color:#fff;padding:96px 0 48px}} footer .top{{display:flex;gap:120px}} footer .brand{{width:360px}}
footer .brand p{{color:{C['blue/20']};font-size:20px;line-height:28px;margin-top:24px}} footer .cols{{flex:1;display:flex;justify-content:space-between;gap:48px}}
footer h4{{font-size:16px;font-weight:600;margin-bottom:16px}} footer a{{display:block;color:{C['blue/20']};text-decoration:none;font-size:16px;line-height:24px;margin-bottom:16px}}
footer .bot{{display:flex;align-items:center;gap:24px;border-top:1px solid #ffffff1f;margin-top:64px;padding-top:24px;font-size:14px;color:{C['blue/40']}}}
footer .bot a{{display:inline;margin:0 0 0 24px;font-size:14px}} footer .bot .grow{{flex:1}}
.draft{{background:{C['grey/160']};color:#fff;text-align:center;font-size:14px;padding:8px}}
@media (max-width:1100px){{.hero .wrap{{grid-template-columns:1fr}} .panel{{height:420px}} footer .top{{flex-direction:column;gap:48px}} nav .links{{display:none}}}}
@media (max-width:600px){{h1{{font-size:48px;line-height:56px}} h2{{font-size:36px;line-height:44px}} .cta h2{{font-size:40px;line-height:48px}} .sec,.hero,.cta{{padding:72px 0}} .shot{{left:24px;top:48px}} footer .cols{{flex-wrap:wrap}}}}"""
    out, samples, errors = [], [], []
    red_counts = {}
    for i, s in enumerate(page["sections"]):
        t = s["type"]
        if t == "nav":
            links = s.get("links", ["Features", "Solutions", "Pricing", "Resources", "Customers"])
            out.append(f"<nav><div class='wrap'><img src='{logo('creator-lockup-colour.svg')}' alt='Zoho Creator' width='154'>"
                       f"<div class='links'>{''.join(f'<a class=l href=#>{esc(l)}</a>' for l in links)}</div>"
                       f"{btn(s.get('secondary','Sign in'),'secondary','sm')}{btn(s.get('primary','Sign up free'),'primary','sm')}</div></nav>")
        elif t == "hero":
            shot = (f"<img src='{b64(s['screenshot'],'image/png')}' alt=''>" if s.get("screenshot") else
                    f"<div style='height:100%;display:flex;align-items:center;justify-content:center;color:{C['grey/120']};font-size:16px;background:{C['grey/10']}'>Product screenshot (replace)</div>")
            if not s.get("screenshot"): samples.append("Hero: product screenshot")
            tex = f"<div class='tex' style='background-image:url({tex_light});opacity:.35'></div>" if topic == "default" else ""
            out.append(f"<section class='hero' style='background:{hero_bg}'><div class='wrap'><div>"
                       + (f"<span class='tag'>{esc(s['tag'])}</span>" if s.get('tag') else '') +
                       f"<h1>{rich(s.get('headline','Headline'), accent)}</h1><p class='lead'>{esc(s.get('body',''))}</p>"
                       f"<div class='btns'>{btn(s.get('primary'),'primary','lg',True)}{btn(s.get('secondary'),'secondary','lg')}</div></div>"
                       f"<div class='panel'>{tex}<div class='shot'>{shot}</div></div></div></section>")
            if len(s.get("headline", "")) > 60: errors.append("Hero headline is over 60 characters; keep it to two or three lines.")
        elif t == "features":
            cards = s.get("cards", [])
            out.append(f"<section class='sec'><div class='wrap'><div class='head'><div class='eyebrow'>{esc(s.get('eyebrow',''))}</div>"
                       f"<h2>{rich(s.get('title',''), accent)}</h2><p class='desc'>{esc(s.get('description',''))}</p></div><div class='cards'>"
                       + "".join(f"<div class='card'><div class='tile'>{icon(c.get('icon','sparkle'), tile_fg)}</div><h3>{esc(c.get('title',''))}</h3><p>{esc(c.get('text',''))}</p></div>" for c in cards)
                       + "</div></div></section>")
            if not 2 <= len(cards) <= 6: errors.append("Feature grid needs 2–6 cards (3 is the template).")
        elif t == "stats":
            st = s.get("stats", [])
            for x in st:
                if not x.get("source"): errors.append(f"Stat '{x.get('value')}' has no source. Never publish a number without one.")
            out.append(f"<section class='sec stats'><div class='wrap'><div class='head'><div class='eyebrow'>{esc(s.get('eyebrow',''))}</div>"
                       f"<h2>{rich(s.get('title',''), accent)}</h2><p class='desc'>{esc(s.get('description',''))}</p></div><div class='statrow'>"
                       + "".join(f"<div class='stat'><div class='v'>{esc(x.get('value','00%'))}</div><div class='lb'>{esc(x.get('label',''))}</div><div class='src'>{esc(x.get('source','Source: add source'))}</div></div>" for x in st)
                       + "</div></div></section>")
        elif t == "cta":
            out.append(f"<section class='cta'>{cta_tex}<div class='wrap' style='position:relative'><h2>{esc(s.get('headline',''))}</h2><p>{esc(s.get('body',''))}</p>"
                       f"<div class='btns'>{btn(s.get('primary'),'primary','lg',True)}{btn(s.get('secondary'),'inverse','lg')}</div></div></section>")
        elif t == "footer":
            out.append(f"<div style='background:{C['grey/20']};color:{C['grey/120']};text-align:center;padding:40px 24px;font-size:16px;border-top:1px solid {C['grey/40']}'>"
                       "Product footer — added by the development team (common zoho.com footer)</div>")
        else:
            errors.append(f"Unknown section type '{t}'.")
        n = sum(1 for k in ("primary",) if s.get(k)) + (1 if t == "nav" else 0)
        if t in ("hero", "cta", "nav") and n > 1: errors.append(f"Section {i+1} ({t}) has more than one red button.")
    page_html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                 f"<title>{esc(page.get('title','Zoho Creator'))}</title><style>{css}</style></head><body>"
                 f"<div class='draft'>Draft for design and dev review · CDS 2.0 · not production code</div>{''.join(out)}</body></html>")
    return page_html, samples, errors


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    page = json.load(open(a[0]))
    h, samples, errors = build(page)
    Path(a[1]).write_text(h)
    print(f"Saved {a[1]}")
    if "--preview" in a:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1720, "height": 1000})
            pg.goto(Path(a[1]).resolve().as_uri()); pg.wait_for_timeout(400)
            pg.screenshot(path=a[a.index("--preview") + 1], full_page=True); b.close()
        print("Preview", a[a.index("--preview") + 1])
    print("WEB CHECK"); print("Errors: none" if not errors else "Errors:")
    for e in errors: print("  ✗", e)
    print("To replace:" if samples else "To replace: none")
    for s in samples: print("  •", s)
    print("Hand-off: draft for design and dev review.")
    sys.exit(1 if errors else 0)
