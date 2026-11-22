"""Build a zoho.com/creator page draft from the CDS 2.0 web sections.

Usage:
  python build_web.py page.json out.html [--preview out.png]

Start from a recipe in assets/web/recipes/ (landing, ai-product, platform-overview, deployment,
erp-extension, industry, partner-hub, partner-story, event, press) and adapt it.
page.json = {"title": "...", "topic": "default|ai|partner", "sections": [{"type": "nav"}, {"type": "hero", "layout": "split", ...}, ...]}
Section types, layouts and fields: references/web.md (section catalogue). Renderers: web_sections.py.
Output is a responsive, self-contained HTML draft for design and dev review — never production code.
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
    from web_sections import Ctx, RENDER, css as section_css
    topic = page.get("topic", "default")
    if topic not in ("default", "ai", "partner"):
        raise SystemExit("topic must be default, ai or partner")
    c = Ctx(topic, C, G, ICONS)
    fonts = "".join(f"@font-face{{font-family:'Zoho Puvi';font-weight:{n};src:url('{b64(A/'fonts'/f'Zoho-Puvi-{w}.ttf','font/ttf')}')}}"
                    for w, n in (("Regular", 400), ("Medium", 500), ("Semibold", 600), ("Bold", 700)))
    out = []
    for i, s in enumerate(page["sections"]):
        t = s.get("type")
        if t == "nav":
            links = s.get("links", ["Features", "Solutions", "Pricing", "Resources", "Customers"])
            out.append(f"<nav><div class='wrap'><img src='{logo('creator-lockup-colour.svg')}' alt='Zoho Creator' width='154'>"
                       f"<div class='links'>{''.join(f'<a class=l href=#>{esc(l)}</a>' for l in links)}</div>"
                       f"{c.btn(s.get('secondary','Sign in'),'secondary','sm')}{c.btn(s.get('primary','Sign up free'),'primary','sm')}</div></nav>")
        elif t == "footer":
            out.append("<div class='foot'>Product footer — added by the development team (common zoho.com footer)</div>")
        elif t in RENDER:
            out.append(RENDER[t](s, c))
        else:
            c.errors.append(f"Unknown section type '{t}'. See references/web.md for the section list.")
        if t != "nav" and sum(1 for k in ("primary",) if s.get(k)) > 1:
            c.errors.append(f"Section {i+1} ({t}) has more than one red button.")
    css = fonts + section_css(C, G)
    page_html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='cds-kind' content='web'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                 f"<title>{esc(page.get('title','Zoho Creator'))}</title><style>{css}</style></head><body>"
                 f"<div class='draft'>Draft for design and dev review · CDS 2.0 · not production code</div>{''.join(out)}</body></html>")
    return page_html, c.samples, c.errors


if __name__ == "__main__":
    import os; os.environ["CDS_ALLOW_VIOLATION"] = "1" if "--allow-violation" in sys.argv else os.environ.get("CDS_ALLOW_VIOLATION", ""); sys.argv = [x for x in sys.argv if x != "--allow-violation"]
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    page = json.load(open(a[0]))
    from check_system import guard; guard(page, sys.argv, kind="web")
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
