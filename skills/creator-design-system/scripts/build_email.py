"""Build a CDS 2.0 email newsletter: email-safe HTML + images, zipped, with a preview.

Usage:
  python build_email.py email.json out_dir/ [--base-url https://cdn.example.com/newsletter/]

email.json:
{
  "subject": "More ways to build, automate, and connect",
  "preheader": "Creator's AI now covers the entire app lifecycle.",   # inbox preview line
  "title": "More ways to build, automate, and connect.",            # Georgia, 46 px
  "hero_tile": {"icon": "sparkle", "family": "blue"},                 # optional 3D tile beside the title
  "greeting": ["Hi there,", "Hope you're doing well!"],
  "intro": "One or two short paragraphs.",
  "sections": [
    {"type": "band", "tone": "blue", "icon": "lightbulb", "heading": "From idea to app with AI",
     "items": [{"icon": "note-pencil", "title": "Plan", "text": "…"}],
     "link": {"label": "WATCH THE VIDEOS →", "url": "https://…"}},
    {"type": "list", "items": [{"icon": "ai-sparkle", "title": "…", "text": "…", "link": {"label": "READ MORE →", "url": "…"}}]},
    {"type": "story", "heading": "Customer spotlight", "tile": {"icon": "star"}, "image": "/path/photo.png",
     "text": "…", "link": {"label": "READ THE STORY →", "url": "…"}},
    {"type": "cta", "text": "If you're interested…", "label": "REPLY TO THIS EMAIL →", "url": "mailto:…"}
  ],
  "signoff": "The Zoho Creator Team",
  "socials": {"linkedin": "https://…", "x": "https://…", "facebook": "https://…", "instagram": "https://…", "youtube": "https://…"}
}

Band tones: blue (default), violet (AI content only), green, yellow. One red button per email.
Fonts: Georgia for headings, Helvetica Neue for body (Foundations · Typography — email exception).
Images are written to out_dir/images/. If the email tool needs hosted images, upload that folder
and pass --base-url so every <img> points at it. Output: out_dir/index.html, images/, preview.png,
and <out_dir>.zip ready to import into any email tool.
"""
import base64, html, json, re, shutil, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
A = SKILL / "assets"
TOK = json.load(open(SKILL / "design-system" / "tokens.json"))
C = TOK["colour"]
ICONS = json.load(open(A / "icons" / "icons.json"))["library"]
HEAD = "Georgia,&quot;Times New Roman&quot;,serif"           # &quot; keeps the quotes inside style='…'
BODY = "&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif"
TONES = {  # band background, band border, header tile, item tile background
    "blue": ("blue/40", "blue/40", "blue/100", "blue/20"),
    "violet": ("violet/20", "violet/40", "violet/100", "violet/20"),
    "green": ("green/30", "green/50", "green/130", "green/20"),
    "yellow": ("yellow/30", "yellow/100", "yellow/140", "yellow/30"),
}
e = lambda t: html.escape(t or "")


class Images:
    """Collects small HTML snippets and renders each to a transparent PNG at 2x."""
    def __init__(self, out):
        self.dir = out / "images"; self.dir.mkdir(parents=True, exist_ok=True); self.jobs = {}

    def add(self, name, w, h, inner):
        self.jobs[name] = (w, h, inner); return f"images/{name}.png"

    def render(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(device_scale_factor=2)
            for name, (w, h, inner) in self.jobs.items():
                pg.set_viewport_size({"width": w, "height": h})
                pg.set_content(f"<html><body style='margin:0;background:transparent'><div id=r style='width:{w}px;height:{h}px;position:relative'>{inner}</div></body></html>")
                pg.wait_for_timeout(50)
                pg.locator("#r").screenshot(path=str(self.dir / f"{name}.png"), omit_background=True)
            b.close()


def svg_icon(name, colour, size, weight="regular"):
    if name not in ICONS:
        raise SystemExit(f"Unknown icon '{name}'. Run: python icon.py list")
    i = ICONS[name][weight]
    return f"<svg viewBox='{i['viewBox']}' width='{size}' height='{size}' fill='currentColor' style='color:{colour};display:block'>{i['body']}</svg>"


def tile_png(img, icon, size, bg, fg, radius, name):
    inner = (f"<div style='width:{size}px;height:{size}px;border-radius:{radius}px;background:{C[bg]};display:flex;align-items:center;justify-content:center'>"
             f"{svg_icon(icon, C[fg], int(size * 0.5))}</div>")
    return img.add(name, size, size, inner)


def tile3d_png(img, icon, family, size, name):
    sys.path.insert(0, str(Path(__file__).parent))
    import render_social as rs
    pad = int(size * 0.12)
    return img.add(name, size + pad, size + pad, rs.tile3d([0, 0, size, size], family, icon))


def logo_png(img, f, w, name):
    s = (A / "logos" / f).read_text()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    h = round(w * vb[3] / vb[2])
    uri = "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()
    return img.add(name, w, h, f"<img src='{uri}' style='width:{w}px;height:{h}px;display:block'>"), h


def btn(label, url):
    return (f"<table role='presentation' cellpadding='0' cellspacing='0' border='0' style='margin:0 auto'><tr><td bgcolor='{C['red/90']}' style='border-radius:4px'>"
            f"<a href='{e(url)}' style='display:inline-block;padding:14px 24px;font-family:{BODY};font-size:14px;font-weight:bold;letter-spacing:.04em;color:#ffffff;text-decoration:none'>{e(label)}</a></td></tr></table>")


def link(l, colour=None):
    if not l: return ""
    return (f"<a href='{e(l.get('url', '#'))}' style='font-family:{BODY};font-size:14px;font-weight:bold;letter-spacing:.04em;color:{colour or C['blue/100']};text-decoration:none'>{e(l.get('label', 'READ MORE →'))}</a>")


def item_rows(items, tile_bg, tile_fg, img, prefix, divider=True):
    rows = []
    for i, it in enumerate(items):
        src = tile_png(img, it.get("icon", "sparkle"), 40, tile_bg, tile_fg, 8, f"{prefix}-{i}")
        if i and divider:
            rows.append(f"<tr><td colspan='2' style='padding:16px 0'><div style='height:1px;background:{C['grey/30']};line-height:1px;font-size:1px'>&nbsp;</div></td></tr>")
        rows.append(f"<tr><td width='56' valign='top' style='padding-top:2px'><img src='{src}' width='40' height='40' alt='' style='display:block;border:0'></td>"
                    f"<td valign='top' style='font-family:{BODY}'><div style='font-size:18px;line-height:26px;font-weight:500;color:{C['base/black']}'>{e(it.get('title'))}</div>"
                    f"<div style='font-size:16px;line-height:24px;color:{C['bluish-grey/150']};padding-top:4px'>{e(it.get('text'))}</div>"
                    f"{('<div style=padding-top:10px>' + link(it.get('link')) + '</div>') if it.get('link') else ''}</td></tr>")
    return "".join(rows)


def build(spec, out):
    img = Images(out)
    errors, samples = [], []
    reds = sum(1 for s in spec.get("sections", []) if s.get("type") == "cta")
    if reds > 1: errors.append("More than one red button. Keep one CTA per email.")
    lock_src, lock_h = logo_png(img, "creator-lockup-colour.svg", 178, "creator-lockup")
    zoho_src, zoho_h = logo_png(img, "zoho-logo-colour.svg", 90, "zoho-logo")
    rows = []
    # header
    rows.append(f"<tr><td style='padding:36px 28px 28px'><table role='presentation' width='100%' cellpadding='0' cellspacing='0'><tr>"
                f"<td><img src='{lock_src}' width='178' height='{lock_h}' alt='Zoho Creator' style='display:block;border:0'></td>"
                f"<td align='right'><img src='{zoho_src}' width='90' height='{zoho_h}' alt='Zoho' style='display:block;border:0'></td></tr></table></td></tr>"
                f"<tr><td style='padding:0'><div style='height:1px;background:{C['grey/30']};line-height:1px;font-size:1px'>&nbsp;</div></td></tr>")
    # title + hero tile
    ht = spec.get("hero_tile")
    hero = ""
    if ht:
        fam = ht.get("family", "blue")
        if fam == "violet" and not spec.get("ai"): samples.append("Violet 3D tile: keep it only if this newsletter is about AI.")
        hero = f"<td width='140' align='right' valign='middle'><img src='{tile3d_png(img, ht.get('icon', 'sparkle'), fam, 112, 'hero-tile')}' width='125' alt='' style='display:block;border:0'></td>"
    rows.append(f"<tr><td style='padding:32px 64px 0'><table role='presentation' width='100%' cellpadding='0' cellspacing='0'><tr>"
                f"<td valign='middle' style='font-family:{HEAD};font-size:46px;line-height:51px;color:{C['base/black']}'>{e(spec.get('title'))}</td>{hero}</tr></table></td></tr>")
    if len(spec.get("title", "")) > 60: errors.append("Title is over 60 characters; keep it to three lines at most.")
    greet = "".join(f"<div style='font-family:{BODY};font-size:16px;line-height:24px;color:{C['bluish-grey/150'] if i == 0 else C['base/black']};font-weight:{500 if i == 0 else 400};padding-bottom:8px'>{e(g)}</div>" for i, g in enumerate(spec.get("greeting", [])))
    rows.append(f"<tr><td style='padding:24px 64px 32px'>{greet}<div style='font-family:{BODY};font-size:16px;line-height:24px;color:{C['base/black']}'>{e(spec.get('intro'))}</div></td></tr>")
    for si, s in enumerate(spec.get("sections", [])):
        t = s.get("type")
        if t == "band":
            tone = s.get("tone", "blue")
            if tone == "violet" and not s.get("ai", spec.get("ai", False)):
                errors.append(f"Section {si+1}: violet bands are for AI content only (set \"ai\": true if it is).")
            bg, bd, ht_c, it_bg = TONES[tone]
            hsrc = tile_png(img, s.get("icon", "sparkle"), 56, ht_c, "base/white", 14, f"band{si}-head")
            inner = item_rows(s.get("items", []), it_bg, ht_c if tone != "yellow" else "yellow/140", img, f"band{si}")
            rows.append(f"<tr><td style='padding:0 21px 16px'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='background:{C[bg]};border:1px solid {C[bd]};border-radius:16px'>"
                        f"<tr><td style='padding:31px 42px 20px'><table role='presentation' cellpadding='0' cellspacing='0'><tr><td width='70'><img src='{hsrc}' width='56' height='56' alt='' style='display:block;border:0'></td>"
                        f"<td style='font-family:{HEAD};font-size:26px;line-height:34px;color:{C['base/black']}'>{e(s.get('heading'))}</td></tr></table></td></tr>"
                        f"<tr><td style='padding:0 42px 31px'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' style='background:#ffffff;border-radius:16px'><tr><td style='padding:24px'>"
                        f"<table role='presentation' width='100%' cellpadding='0' cellspacing='0'>{inner}</table>"
                        f"{('<div style=padding-top:16px>' + link(s.get('link')) + '</div>') if s.get('link') else ''}</td></tr></table></td></tr></table></td></tr>")
        elif t == "list":
            rows.append(f"<tr><td style='padding:8px 64px 24px'><table role='presentation' width='100%' cellpadding='0' cellspacing='0'>{item_rows(s.get('items', []), 'blue/20', 'blue/100', img, f'list{si}')}</table></td></tr>")
        elif t == "story":
            tile = ""
            if s.get("tile"):
                tile = f"<td width='80' align='right'><img src='{tile3d_png(img, s['tile'].get('icon', 'star'), s['tile'].get('family', 'blue'), 56, f'story{si}-tile')}' width='64' alt='' style='display:block;border:0'></td>"
            pic = ""
            if s.get("image"):
                dst = img.dir / f"story{si}{Path(s['image']).suffix}"; shutil.copy(s["image"], dst)
                pic = f"<div style='padding-top:16px'><img src='images/{dst.name}' width='472' alt='' style='display:block;border:0;border-radius:12px;width:100%;max-width:472px'></div>"
            elif s.get("image_slot", True):
                samples.append(f"Section {si+1} ({s.get('heading')}): add an image if you have one (optional).")
            rows.append(f"<tr><td style='padding:16px 64px 24px'><table role='presentation' width='100%' cellpadding='0' cellspacing='0'><tr>"
                        f"<td style='font-family:{HEAD};font-size:40px;line-height:46px;color:{C['base/black']}'>{e(s.get('heading'))}</td>{tile}</tr></table>{pic}"
                        f"<div style='font-family:{BODY};font-size:18px;line-height:27px;color:{C['base/black']};padding-top:16px'>{e(s.get('text'))}</div>"
                        f"{('<div style=padding-top:12px>' + link(s.get('link')) + '</div>') if s.get('link') else ''}</td></tr>"
                        f"<tr><td style='padding:0 64px'><div style='height:1px;background:{C['grey/30']};line-height:1px;font-size:1px'>&nbsp;</div></td></tr>")
        elif t == "cta":
            rows.append(f"<tr><td align='center' style='padding:32px 64px 40px;font-family:{BODY};font-size:18px;line-height:27px;color:{C['base/black']};text-align:center'>"
                        f"{e(s.get('text'))}<div style='padding-top:24px'>{btn(s.get('label', 'START BUILDING ON CREATOR →'), s.get('url', '#'))}</div></td></tr>")
        else:
            errors.append(f"Unknown section type '{t}'.")
    # sign-off + footer (blue band)
    soc = spec.get("socials", {})
    icons = ""
    for k, nm in (("linkedin", "linkedin-logo"), ("x", "x-logo"), ("facebook", "facebook-logo"), ("instagram", "instagram-logo"), ("youtube", "youtube-logo")):
        if soc.get(k):
            src = img.add(f"social-{k}", 32, 32, f"<div style='width:32px;height:32px;border-radius:6px;background:#fff;display:flex;align-items:center;justify-content:center'>{svg_icon(nm, C['blue/100'], 18, 'fill')}</div>")
            icons += f"<td style='padding:0 6px'><a href='{e(soc[k])}'><img src='{src}' width='32' height='32' alt='{k}' style='display:block;border:0'></a></td>"
    if not soc: samples.append("Footer social links (add the profile URLs).")
    rows.append(f"<tr><td bgcolor='{C['blue/100']}' align='center' style='padding:40px 32px;text-align:center'>"
                f"<div style='font-family:{BODY};font-size:13px;letter-spacing:.12em;color:{C['blue/20']}'>REGARDS,</div>"
                f"<div style='font-family:{HEAD};font-size:30px;line-height:38px;color:#ffffff;padding-top:6px'>{e(spec.get('signoff', 'The Zoho Creator Team'))}</div>"
                f"<div style='height:1px;background:#ffffff33;margin:28px 0;line-height:1px;font-size:1px'>&nbsp;</div>"
                f"<div style='font-family:{BODY};font-size:14px;color:{C['blue/20']};padding-bottom:16px'>Follow us for all the latest updates on low-code.</div>"
                f"<table role='presentation' cellpadding='0' cellspacing='0' style='margin:0 auto'><tr>{icons}</tr></table></td></tr>")
    pre = e(spec.get("preheader", ""))
    page = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<meta name='x-apple-disable-message-reformatting'><title>{e(spec.get('subject', 'Zoho Creator'))}</title>"
            f"<style>@media (max-width:620px){{.wrap{{width:100%!important}} td{{padding-left:20px!important;padding-right:20px!important}}}}</style></head>"
            f"<body style='margin:0;padding:0;background:{C['grey/20']}'>"
            f"<div style='display:none;max-height:0;overflow:hidden;opacity:0'>{pre}</div>"
            f"<table role='presentation' width='100%' cellpadding='0' cellspacing='0' bgcolor='{C['grey/20']}'><tr><td align='center' style='padding:24px 0'>"
            f"<table role='presentation' class='wrap' width='600' cellpadding='0' cellspacing='0' bgcolor='#ffffff' style='width:600px;background:#ffffff'>{''.join(rows)}</table>"
            f"</td></tr></table></body></html>")
    if not spec.get("preheader"): samples.append("Preheader (the grey preview line in the inbox).")
    return page, img, errors, samples


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    spec = json.load(open(a[0])); out = Path(a[1]); out.mkdir(parents=True, exist_ok=True)
    page, img, errors, samples = build(spec, out)
    img.render()
    if "--base-url" in a:
        base = a[a.index("--base-url") + 1].rstrip("/") + "/"
        page = page.replace("src='images/", f"src='{base}images/")
    (out / "index.html").write_text(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 680, "height": 900})
        pg.goto((out / "index.html").resolve().as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / "preview.png"), full_page=True); b.close()
    z = shutil.make_archive(str(out), "zip", out)
    print(f"Saved {out}/index.html, {len(img.jobs)} images, preview.png and {Path(z).name}")
    print("EMAIL CHECK"); print("Errors: none" if not errors else "Errors:")
    for x in errors: print("  ✗", x)
    print("To do before sending:")
    for x in samples + ["Send a test to yourself in Gmail and Outlook before the real send.",
                        "Images: upload the images folder with the HTML, or use --base-url if your email tool needs hosted images."]:
        print("  •", x)
    sys.exit(1 if errors else 0)
