"""CDS 2.0 web section library, used by build_web.py.

Every section mirrors a template on Templates · Web in the CDS-2.0 Figma file
(1720 grid, 1320 content, 120 px section padding, Zoho Puvi text styles, CDS colours only).
Each renderer takes the section dict from page.json and a Ctx (topic, colours, helpers) and
returns HTML. Fields are documented in references/web.md. Never add colours, sizes or
fonts here that are not CDS tokens.
"""
import base64, html, re
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
A = SKILL / "assets"


def esc(t):
    return html.escape(t or "")


def b64(p, mt):
    return f"data:{mt};base64,{base64.b64encode(Path(p).read_bytes()).decode()}"


class Ctx:
    """Page context: topic colours, helpers, samples and errors collected while rendering."""

    def __init__(self, topic, C, G, ICONS):
        self.topic, self.C, self.G, self.ICONS = topic, C, G, ICONS
        self.samples, self.errors = [], []
        ai = topic == "ai"
        self.accent = C["violet/100"] if topic in ("ai", "partner") else C["blue/100"]   # light backgrounds only
        self.tile_bg, self.tile_fg = (C["violet/20"], C["violet/100"]) if ai else (C["blue/20"], C["blue/100"])
        self.bold_bg = G["ai"] if ai else (G["midnight"] if topic == "partner" else G["brand-depth"])
        self.soft_bg = G["soft-violet"] if ai else G["soft-blue"]
        self.mesh_bg = G["mesh-soft-ai"] if ai else (G["mesh-partner"] if topic == "partner" else G["mesh-soft-blue"])
        self.tex_light = b64(A / "patterns" / "connect-tile-light.svg", "image/svg+xml")
        self.tex_bold = b64(A / "patterns" / "connect-tile-bold.svg", "image/svg+xml")

    # text with **highlight**; on dark/gradient backgrounds highlights are yellow, on light the accent
    def rich(self, t, dark=False):
        col = self.C["yellow/100"] if dark else self.accent
        return re.sub(r"\*\*(.+?)\*\*", rf"<span style='color:{col}'>\1</span>", esc(t))

    def icon(self, name, colour, size=24, fill=False):
        if name not in self.ICONS:
            self.errors.append(f"Unknown icon '{name}'. Run: python scripts/icon.py list")
            name = "sparkle"
        if self.topic != "ai" and name in ("ai-sparkle", "llm", "ai-app-builder", "ai-code"):
            self.errors.append(f"Icon '{name}' is AI-only; this page's topic isn't AI.")
        if self.topic == "ai" and name == "robot":
            self.errors.append("Robot icon on an AI page: use ai-sparkle (the robot is only for a literal robot).")
        i = self.ICONS[name]["fill" if fill else "regular"]
        return f"<svg viewBox='{i['viewBox']}' width='{size}' height='{size}' fill='currentColor' style='color:{colour};flex:none'>{i['body']}</svg>"

    def tile(self, name, size=48, dark=False):
        bg, fg = (("#ffffff1f", "#fff") if dark else (self.tile_bg, self.tile_fg))
        return f"<span class='itile' style='width:{size}px;height:{size}px;background:{bg}'>{self.icon(name, fg, size // 2)}</span>"

    def img(self, path, label, cls="ph", style=""):
        if path:
            mt = "image/png" if str(path).lower().endswith(".png") else "image/jpeg"
            return f"<img class='{cls}' src='{b64(path, mt)}' alt='' style='object-fit:cover;{style}'>"
        self.samples.append(label)
        return f"<div class='{cls} phbox' style='{style}'><span>{esc(label)} (replace)</span></div>"

    def btn(self, label, kind, size="lg", arrow=False):
        if not label:
            return ""
        return f"<a class='btn {kind} {size}' href='#'>{esc(label)}{' →' if arrow else ''}</a>"

    def head(self, s, dark=False, align="center"):
        eb = f"<div class='eyebrow' style='color:{('#fff' if dark else self.accent)}'><span class='dot' style='background:{self.C['yellow/100'] if dark else self.accent}'></span>{esc(s.get('eyebrow'))}</div>" if s.get("eyebrow") else ""
        lead = f"<p class='lead'>{esc(s.get('lead') or s.get('description'))}</p>" if (s.get("lead") or s.get("description")) else ""
        if len(s.get("title", "")) > 90:
            self.errors.append(f"Section title is over 90 characters: '{s['title'][:40]}…'. Shorten it.")
        return f"<div class='head {align}'>{eb}<h2>{self.rich(s.get('title',''), dark)}</h2>{lead}</div>"


def css(C, G):
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}} body{{font-family:'Zoho Puvi',Arial,sans-serif;color:{C['grey/160']};background:#fff;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1368px;margin:0 auto;padding:0 24px}} section{{position:relative;overflow:hidden}} .sec{{padding:120px 0}}
.tex{{position:absolute;inset:0;background-size:480px 480px;pointer-events:none}}
h1{{font-size:72px;line-height:80px;letter-spacing:-.03em;font-weight:600}} h2{{font-size:56px;line-height:64px;letter-spacing:-.03em;font-weight:600}}
h3{{font-size:24px;line-height:32px;letter-spacing:-.01em;font-weight:600}} h4{{font-size:20px;line-height:28px;font-weight:600}}
p{{font-size:16px;line-height:24px}} .muted{{color:{C['grey/120']}}}
.head{{max-width:920px;margin:0 auto 64px}} .head.center{{text-align:center}} .head.left{{margin-left:0}}
.head .lead{{font-size:20px;line-height:28px;color:{C['grey/120']};margin-top:20px}}
.dark .head .lead,.dark .muted,.on-dark .muted{{color:{C['blue/20']}}}
.eyebrow{{display:inline-flex;align-items:center;gap:10px;font-size:14px;line-height:20px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin-bottom:16px}}
.eyebrow .dot{{width:8px;height:8px;border-radius:999px}}
.btn{{display:inline-flex;align-items:center;gap:12px;border-radius:4px;font-weight:600;text-decoration:none;white-space:nowrap}}
.btn.lg{{height:64px;padding:0 32px;font-size:18px}} .btn.sm{{height:48px;padding:0 20px;font-size:16px}}
.btn.primary{{background:{C['red/90']};color:#fff}} .btn.primary:hover{{background:{C['red/100']}}}
.btn.secondary{{box-shadow:inset 0 0 0 2px {C['blue/100']};color:{C['blue/100']};background:#fff}} .btn.inverse{{background:#fff;color:{C['blue/100']}}}
.btn.ghost{{box-shadow:inset 0 0 0 2px #ffffff66;color:#fff}}
.btns{{display:flex;gap:16px;margin-top:40px;flex-wrap:wrap}} .center .btns,.btns.center{{justify-content:center}}
.itile{{display:inline-flex;align-items:center;justify-content:center;border-radius:4px;flex:none}}
.tagp{{display:inline-block;height:36px;line-height:36px;padding:0 16px;border-radius:4px;font-weight:600;font-size:14px;letter-spacing:.04em;text-transform:uppercase}}
/* helpers for inline lists */ .pill2{{background:#ffffff1f;border-radius:999px;padding:6px 14px;font-size:13px;font-weight:600}} .stag{{display:inline-block;margin:12px 8px 0 0;background:{C['blue/10']};color:{C['blue/100']};border-radius:4px;padding:4px 10px;font-size:13px;font-weight:600}} .colrow{{display:flex;gap:12px;padding:12px 0;border-top:1px solid {C['grey/40']}}}
.card{{color:{C['grey/160']};background:#fff;border:1px solid {C['grey/40']};border-radius:24px;padding:32px;box-shadow:0 2px 4px 0 #0000000d}}
.ph{{display:block;width:100%;border-radius:16px}} .phbox{{background:{C['grey/10']};border:1px dashed {C['grey/60']};display:flex;align-items:center;justify-content:center;color:{C['grey/120']};font-size:14px;text-align:center;padding:16px}}
.dark .phbox,.on-dark .phbox{{background:#ffffff0f;border-color:#ffffff33;color:{C['blue/40']}}}
.shot{{border-radius:24px;background:#fff;border:1px solid {C['grey/40']};box-shadow:0 40px 80px -16px #00000029;overflow:hidden}}
.dark{{color:#fff}} .dark h2,.dark h3,.dark h4{{color:#fff}} .dark .card:not(.dark) h3,.dark .card:not(.dark) h4{{color:{C['grey/160']}}} .card.dark{{color:#fff}} .dark .card:not(.dark) .list li,.dark .card:not(.dark) .muted{{color:{C['grey/120']}}}
.grid{{display:grid;gap:24px}} .g2{{grid-template-columns:repeat(2,1fr)}} .g3{{grid-template-columns:repeat(3,1fr)}} .g4{{grid-template-columns:repeat(4,1fr)}}
.list{{list-style:none;display:grid;gap:12px;margin-top:16px}} .list li{{display:flex;gap:10px;font-size:16px;line-height:24px;color:{C['grey/130']}}}
.dark .list li{{color:{C['blue/20']}}}
nav{{height:80px;border-bottom:1px solid {C['grey/40']};background:#fff;position:sticky;top:0;z-index:5}}
nav .wrap{{display:flex;align-items:center;height:100%;gap:32px}} nav .links{{display:flex;gap:32px;flex:1}}
nav a.l{{color:{C['grey/160']};text-decoration:none;font-weight:500;font-size:16px}} nav a.l:hover{{color:{C['blue/100']}}}
.draft{{background:{C['grey/160']};color:#fff;text-align:center;font-size:14px;padding:8px}}
.foot{{background:{C['grey/20']};color:{C['grey/120']};text-align:center;padding:40px 24px;font-size:16px;border-top:1px solid {C['grey/40']}}}
/* heroes */
.hero{{padding:112px 0}} .hero .split{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
.hero .lead{{font-size:20px;line-height:28px;color:{C['grey/120']};margin-top:24px;max-width:600px}} .hero.dark .lead{{color:{C['blue/20']}}}
.hero .center{{text-align:center;max-width:1040px;margin:0 auto}} .hero .center .lead{{margin-left:auto;margin-right:auto}}
.panel{{position:relative;height:520px;border-radius:24px;overflow:hidden}}
.statline{{display:flex;gap:40px;justify-content:center;margin-top:40px;flex-wrap:wrap}} .statline b{{font-size:20px;font-weight:600}} .statline span{{color:{C['grey/120']};margin-left:6px}}
.chip{{white-space:nowrap;color:{C['grey/160']};display:inline-flex;align-items:center;gap:10px;background:#fff;border:1px solid {C['grey/40']};border-radius:999px;padding:8px 16px 8px 8px;font-size:14px;font-weight:600;box-shadow:0 16px 24px -4px #00000026}}
.uicard{{color:{C['grey/160']};background:#fff;border-radius:16px;padding:16px;box-shadow:0 24px 48px -8px #00000040;font-size:14px}}
.form{{background:#fff;border-radius:24px;padding:40px;box-shadow:0 40px 80px -16px #00000029;color:{C['grey/160']}}}
.form label{{display:block;font-size:14px;font-weight:600;margin:16px 0 8px}} .form .in{{height:48px;border:1px solid {C['grey/60']};border-radius:8px;background:#fff}}
.countdown{{display:flex;align-items:center;justify-content:space-between;padding:40px 0}} .countdown .n{{text-align:center;padding:0 48px;border-left:1px solid {C['grey/40']}}} .countdown .n:first-child{{border:0}}
.countdown b{{font-size:56px;line-height:64px;font-weight:600;color:{C['grey/170']}}} .countdown small{{display:block;font-size:12px;font-weight:600;letter-spacing:.08em;color:{C['grey/120']}}}
.corner{{position:absolute;width:28px;height:28px;border-color:{C['blue/40']};border-style:solid;border-width:0}}
/* tabs, accordions, steps */
.tabs-side{{display:grid;grid-template-columns:400px 1fr;gap:48px;align-items:start}} .tablist{{display:grid;gap:12px}}
.tab{{display:flex;align-items:center;gap:12px;padding:16px 20px;border-radius:12px;border:1px solid {C['grey/40']};background:#fff;font-weight:600}}
.tab.on{{border-color:{C['blue/100']};box-shadow:0 16px 24px -4px #00000026}}
.dark .tab{{background:#ffffff0a;border-color:#ffffff1f;color:#fff}} .dark .tab.on{{background:#fff;color:{C['grey/160']}}}
.bigtabs{{display:grid;gap:8px}} .bigtabs div{{font-size:40px;line-height:48px;letter-spacing:-.02em;color:{C['grey/100']};font-weight:500}} .bigtabs .on{{color:{C['blue/100']}}}
.toptabs{{display:flex;justify-content:center;gap:40px;border-bottom:1px solid {C['grey/40']};margin-bottom:40px}} .toptabs div{{padding:16px 0;font-weight:600;color:{C['grey/120']}}} .toptabs .on{{color:{C['blue/100']};box-shadow:inset 0 -2px 0 {C['blue/100']}}}
.acc{{border-radius:24px;background:#fff;border:1px solid {C['grey/40']};margin-bottom:16px;overflow:hidden}} .acc .ah{{display:flex;align-items:center;gap:16px;padding:24px 32px}}
.acc .ah .t{{flex:1}} .acc .ab{{padding:0 32px 32px}} .dark .acc{{background:#ffffff0a;border-color:#ffffff1f}}
.steps{{display:grid;grid-template-columns:480px 1fr;gap:80px}} .step{{position:relative;padding:0 0 40px 72px}}
.step .num{{position:absolute;left:0;top:0;width:44px;height:44px;border-radius:999px;background:{C['blue/20']};color:{C['blue/100']};font-weight:600;display:flex;align-items:center;justify-content:center}}
.step:before{{content:'';position:absolute;left:21px;top:52px;bottom:8px;width:2px;background:{C['blue/30']}}} .step:last-child:before{{display:none}}
.timeline{{display:grid;gap:24px}} .tl{{display:grid;grid-template-columns:160px 1fr;gap:32px;align-items:start}} .tl .when{{font-size:14px;font-weight:600;color:{C['blue/100']};padding-top:6px}}
/* misc */
.logos{{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}} .logo{{width:180px;height:72px;border-radius:8px;border:1px dashed {C['grey/60']};display:flex;align-items:center;justify-content:center;color:{C['grey/120']};font-size:13px}}
.stats4{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;text-align:center}} .stats4 b{{display:block;font-size:56px;line-height:64px;font-weight:600;letter-spacing:-.03em;color:{C['blue/100']}}}
.stats4 span{{font-size:16px;color:{C['grey/120']}}} .stats4 small{{display:block;font-size:12px;color:{C['grey/100']};margin-top:4px}}
.quote{{font-size:40px;line-height:48px;letter-spacing:-.02em;font-weight:500}} .person{{display:flex;align-items:center;gap:16px;margin-top:32px}} .avatar{{width:56px;height:56px;border-radius:999px;background:{C['grey/30']};flex:none}}
.faq{{display:grid;grid-template-columns:400px 1fr;gap:80px}} .qa{{border-radius:16px;padding:24px 28px;margin-bottom:12px;background:{C['grey/10']}}} .qa .q{{display:flex;gap:16px;align-items:center;font-weight:600;font-size:18px}} .qa .q span{{flex:1}} .qa .a{{margin-top:12px;color:{C['grey/120']}}}
.dark .qa{{background:#ffffff0f}} .dark .qa .a{{color:{C['blue/20']}}}
.res{{border-radius:16px;padding:28px;min-height:220px;color:#fff;display:flex;flex-direction:column;justify-content:space-between}}
.res h3{{font-size:22px;line-height:30px}}
.vs{{display:grid;grid-template-columns:1fr 1.4fr;gap:24px}} .vs .col{{border-radius:24px;padding:40px}}
.layers{{display:grid;gap:12px;perspective:1200px}} .layer{{height:72px;border-radius:16px;display:flex;align-items:center;padding:0 24px;gap:12px;font-weight:600;transform:rotateX(18deg)}}
.orbit{{position:relative;width:560px;height:560px;margin:0 auto}} .ring{{position:absolute;border-radius:999px;border:1px dashed #ffffff33}}
.node{{position:absolute;display:flex;flex-direction:column;align-items:center;gap:8px;font-size:14px;color:{C['blue/20']};transform:translate(-50%,-50%)}} .node .itile{{border-radius:999px;background:{C['blue/160']};border:1px solid #ffffff29}}
.sphere{{position:absolute;left:50%;top:50%;width:240px;height:240px;transform:translate(-50%,-50%);border-radius:999px;background:radial-gradient(circle at 35% 30%, {C['blue/60']}, {C['blue/100']} 45%, {C['blue/160']});box-shadow:0 0 120px {C['blue/100']}80;display:flex;align-items:center;justify-content:center}}
@media (max-width:1100px){{.hero .split,.tabs-side,.steps,.faq,.vs,.g3,.g4{{grid-template-columns:1fr}} .g2{{grid-template-columns:1fr}} nav .links{{display:none}} .panel{{height:400px}} .orbit{{transform:scale(.8)}}}}
@media (max-width:600px){{h1{{font-size:44px;line-height:52px}} h2{{font-size:36px;line-height:44px}} .sec,.hero{{padding:72px 0}} .quote{{font-size:28px;line-height:36px}} .countdown{{flex-wrap:wrap}} .countdown .n{{padding:0 16px}}}}
"""


# ---------------------------------------------------------------- heroes
def hero(s, c):
    C, G = c.C, c.G
    lay = s.get("layout", "split")
    tag = s.get("tag")
    tagh = f"<span class='tagp' style='background:{c.tile_bg};color:{c.tile_fg}'>{esc(tag)}</span>" if tag else ""
    if len(s.get("headline", "")) > 70:
        c.errors.append("Hero headline is over 70 characters; keep it to two or three lines.")
    btns = f"<div class='btns'>{c.btn(s.get('primary'),'primary','lg',True)}{c.btn(s.get('secondary'),'secondary','lg')}</div>"
    if lay == "split":
        tex = f"<div class='tex' style='background-image:url({c.tex_light});opacity:.08'></div>" if c.topic == "default" else ""
        panel_bg = C["blue/100"] if c.topic == "default" else c.bold_bg
        shot = c.img(s.get("screenshot"), "Hero: product screenshot", "ph", "position:absolute;left:64px;top:88px;width:620px;height:400px;border-radius:24px;box-shadow:0 40px 80px -16px #00000029")
        return (f"<section class='hero' style='background:{c.soft_bg}'><div class='wrap split'><div>{tagh}<h1 style='margin-top:24px'>{c.rich(s.get('headline','Headline'))}</h1>"
                f"<p class='lead'>{esc(s.get('body'))}</p>{btns}</div><div class='panel' style='background:{panel_bg}'>{tex}{shot}</div></div></section>")
    if lay == "centred":
        stats = "".join(f"<div><b>{esc(x.get('value'))}</b><span>{esc(x.get('label'))}</span></div>" for x in s.get("stats", [])[:3])
        return (f"<section class='hero' style='background:{c.mesh_bg}'><div class='wrap center'>{tagh}<h1 style='margin-top:24px'>{c.rich(s.get('headline','Headline'))}</h1>"
                f"<p class='lead'>{esc(s.get('body'))}</p>{btns if s.get('primary') else ''}{f'<div class=statline>{stats}</div>' if stats else ''}</div></section>")
    if lay == "screenshot":
        shot = c.img(s.get("screenshot"), "Hero: product screenshot (dashboard)", "ph shot", "max-width:1200px;height:640px;margin:72px auto 0")
        return (f"<section class='hero' style='background:{c.soft_bg};padding-bottom:0'><div class='wrap center'>{tagh}<h1 style='margin-top:24px'>{c.rich(s.get('headline','Headline'))}</h1>"
                f"<p class='lead'>{esc(s.get('body'))}</p><div class='btns center'>{c.btn(s.get('primary'),'primary','lg',True)}{c.btn(s.get('secondary'),'secondary','lg')}</div></div>"
                f"<div class='wrap'>{shot}</div></section>")
    if lay == "diagram":
        nodes = s.get("nodes", [])[:4]; pos = [(22, 12), (12, 52), (34, 90), (86, 52)]
        nh = "".join(f"<div class='chip' style='position:absolute;left:{p[0]}%;top:{p[1]}%;transform:translate(-50%,-50%)'>{c.tile(n.get('icon','sparkle'),32)}{esc(n.get('label'))}</div>" for n, p in zip(nodes, pos))
        core = (f"<div style='position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:200px;height:184px;background:#fff;border-radius:24px;box-shadow:0 40px 80px -16px #00000029;"
                f"display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px'><img src='{b64(A/'logos'/'creator-lockup-colour.svg','image/svg+xml')}' width='132' alt='Zoho Creator'>"
                f"<span style='font-size:13px;color:{C['grey/120']}'>{'AI that builds with you' if c.topic=='ai' else 'One platform for your apps'}</span></div>")
        rings = "".join(f"<div style='position:absolute;left:50%;top:50%;width:{r}px;height:{r}px;transform:translate(-50%,-50%);border-radius:999px;border:1px {d} {c.accent}33'></div>" for r, d in ((260, 'solid'), (430, 'dashed'), (590, 'solid')))
        cards = "".join(f"<div class='uicard' style='position:absolute;{pos_}width:240px'><b>{esc(k.get('title'))}</b><div class='muted' style='margin-top:6px'>{esc(k.get('text'))}</div></div>"
                        for k, pos_ in zip(s.get("cards", [])[:2], ("right:0;top:6%;", "right:2%;bottom:6%;")))
        return (f"<section class='hero' style='background:{c.soft_bg}'><div class='wrap split'><div>{tagh}<h1 style='margin-top:24px;font-size:64px;line-height:72px'>{c.rich(s.get('headline','Headline'))}</h1>"
                f"<p class='lead'>{esc(s.get('body'))}</p>{btns}</div><div style='position:relative;height:600px'>{rings}{core}{nh}{cards}</div></div></section>")
    if lay == "form":
        fields = s.get("fields", ["Name", "Email address", "Phone number", "Tell us your requirement"])
        fh = "".join(f"<label>{esc(f)}</label><div class='in' style='{'height:96px' if 'requirement' in f.lower() or 'message' in f.lower() else ''}'></div>" for f in fields)
        return (f"<section class='hero dark' style='background:{C['blue/100']}'><div class='tex' style='background-image:url({c.tex_light});opacity:.08'></div><div class='wrap split' style='position:relative'>"
                f"<div>{f'<span class=tagp style=background:#ffffff1f;color:#fff>{esc(tag)}</span>' if tag else ''}<h1 style='margin-top:24px'>{c.rich(s.get('headline','Headline'), True)}</h1>"
                f"<p class='lead'>{esc(s.get('body'))}</p></div><div class='form'><h3>{esc(s.get('form_title','Get started'))}</h3>{fh}"
                f"<div class='btns' style='margin-top:24px'>{c.btn(s.get('primary','Submit'),'primary','lg')}</div><p class='muted' style='font-size:12px;margin-top:16px'>{esc(s.get('consent','By submitting, you agree to the Terms of Service and Privacy Policy.'))}</p></div></div></section>")
    if lay == "event":
        year = esc(s.get("year", "2027")); digits = "".join(
            f"<span style='display:inline-flex;width:72px;height:88px;align-items:center;justify-content:center;font-size:56px;font-weight:600;{('background:'+C['yellow/100']+';color:'+C['grey/180']) if i==len(year)-1 else 'box-shadow:inset 0 0 0 1px #ffffff33;background:#ffffff0a'}'>{d}</span>" for i, d in enumerate(year))
        cnt = s.get("countdown", [["114", "DAYS"], ["08", "HOURS"], ["42", "MIN"], ["16", "SEC"]])
        cd = "".join(f"<div class='n'><b>{esc(a)}</b><small>{esc(b)}</small></div>" for a, b in cnt)
        corners = "".join(f"<div class='corner' style='{p}'></div>" for p in ("left:20px;top:20px;border-left-width:2px;border-top-width:2px", "right:20px;top:20px;border-right-width:2px;border-top-width:2px", "left:20px;bottom:20px;border-left-width:2px;border-bottom-width:2px", "right:20px;bottom:20px;border-right-width:2px;border-bottom-width:2px"))
        visual = c.img(s.get("visual"), "Event key art (trophy, venue or speaker)", "ph", "height:480px;border-radius:24px;background:#ffffff0a")
        return (f"<section class='hero dark' style='background:{C['grey/170']};padding:48px 0 96px'>{corners}"
                f"<div style='position:absolute;left:20%;top:20%;width:720px;height:520px;border-radius:999px;background:{C['blue/100']};opacity:.35;filter:blur(160px)'></div>"
                f"<div class='wrap' style='position:relative'><div style='display:flex;justify-content:space-between;border-bottom:1px solid #ffffff1f;padding-bottom:20px;font-size:13px;font-weight:600;letter-spacing:.06em;color:#ffffffd9'>"
                f"<span>{esc(s.get('meta','ZOHO CREATOR · EVENT'))}</span>{f'<span class=tagp style=background:{C[chr(121)+chr(101)+chr(108)+chr(108)+chr(111)+chr(119)+chr(47)+chr(49)+chr(48)+chr(48)]};color:{C[chr(103)+chr(114)+chr(101)+chr(121)+chr(47)+chr(49)+chr(56)+chr(48)]};height:28px;line-height:28px>{esc(s.get(chr(98)+chr(97)+chr(100)+chr(103)+chr(101)))}</span>' if s.get('badge') else ''}</div>"
                f"<div class='split' style='margin-top:64px'><div><h1 style='font-size:88px;line-height:96px'>{c.rich(s.get('headline','Event name'), True)}</h1><div style='display:flex;margin-top:16px'>{digits}</div>"
                f"<p class='lead' style='font-weight:600;color:#fff'>{esc(s.get('body'))}</p><div class='btns'>{c.btn(s.get('primary','Register now'),'primary','lg',True)}</div>"
                f"<div style='display:flex;gap:24px;margin-top:32px;padding-top:24px;border-top:1px solid #ffffff1f;align-items:center'>{c.icon('calendar-blank',C['blue/50'],22)}<span>{esc(s.get('date','Date'))}</span>{c.icon('globe',C['blue/50'],22)}<span>{esc(s.get('place','Place'))}</span></div></div>"
                f"<div>{visual}</div></div></div></section>"
                f"<section style='background:#fff;border-bottom:1px solid {C['grey/40']}'><div class='wrap countdown'><div style='display:flex;align-items:center;gap:12px;font-size:13px;font-weight:600;letter-spacing:.06em'><span class='dot' style='width:10px;height:10px;border-radius:999px;background:{C['blue/100']}'></span>{esc(s.get('countdown_label','REGISTRATIONS CLOSE IN'))}</div><div style='display:flex'>{cd}</div></div></section>")
    if lay == "video":
        vid = (f"<div class='shot' style='max-width:1080px;height:608px;margin:56px auto 0;background:{C['grey/180']};display:flex;align-items:center;justify-content:center;position:relative'>"
               + (c.img(s.get('video_still'), 'Video still (16:9)', 'ph', 'position:absolute;inset:0;height:100%;border-radius:0') if s.get('video_still') else (c.samples.append('Video still (16:9)') or ''))
               + f"<span style='position:relative;width:88px;height:88px;border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center'>{c.icon('play', C['blue/100'], 32, True)}</span></div>")
        logo = c.img(s.get("logo"), "Customer logo", "ph", "width:200px;height:64px;margin:0 auto 24px;border-radius:8px")
        return (f"<section class='hero' style='background:{c.mesh_bg}'><div class='wrap center'>{logo}<div class='eyebrow' style='color:{c.accent}'>{esc(s.get('eyebrow','Customer story'))}</div>"
                f"<h1 style='font-size:56px;line-height:64px'>{c.rich(s.get('headline','Headline'))}</h1>{vid}</div></section>")
    if lay == "cards":   # AI app builder hero: bold background, fanned app cards
        cards = s.get("cards", [{"title": "Order management"}, {"title": "Admission management"}, {"title": "Expense management"}])[:3]
        rot = (-8, 0, 8); off = (-200, 0, 200); tint = (C["violet/100"], C["blue/100"], C["yellow/100"])
        ch = "".join(f"<div class='uicard' style='position:absolute;left:50%;top:{60 if i!=1 else 20}px;width:230px;height:300px;transform:translateX(calc(-50% + {off[i]}px)) rotate({rot[i]}deg);z-index:{2 if i==1 else 1}'>"
                     f"<span class='itile' style='width:56px;height:56px;background:{tint[i]}'>{c.icon(k.get('icon','stack'),'#fff' if i!=2 else C['grey/170'],28)}</span><h3 style='margin-top:24px'>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:8px'>{esc(k.get('text','Built with AI in minutes'))}</p></div>" for i, k in enumerate(cards))
        return (f"<section class='hero dark' style='background:{c.bold_bg}'><div class='wrap split'><div><h1>{c.rich(s.get('headline','Headline'), True)}</h1><p class='lead'>{esc(s.get('body'))}</p>"
                f"<div class='btns'>{c.btn(s.get('primary'),'primary','lg',True)}</div>{f'<p style=margin-top:32px;color:{C[chr(98)+chr(108)+chr(117)+chr(101)+chr(47)+chr(50)+chr(48)]};font-size:14px>{esc(s.get(chr(110)+chr(111)+chr(116)+chr(101)))}</p>' if s.get('note') else ''}</div>"
                f"<div style='position:relative;height:440px'>{ch}</div></div></section>")
    if lay == "chips":   # centred hero with floating feature chips
        chips = s.get("chips", [])[:6]; pos = [(6, 18), (4, 58), (14, 86), (94, 16), (96, 56), (86, 86)]
        chh = "".join(f"<div class='chip' style='position:absolute;left:{p[0]}%;top:{p[1]}%;transform:translate(-50%,-50%)'>{c.tile(k.get('icon','sparkle'),32)}<span>{esc(k.get('label'))}</span></div>" for k, p in zip(chips, pos))
        return (f"<section class='hero' style='background:{c.mesh_bg};min-height:760px'><div class='wrap' style='position:relative;min-height:560px'>{chh}<div class='center' style='padding-top:80px'>{tagh}"
                f"<h1 style='margin-top:24px'>{c.rich(s.get('headline','Headline'))}</h1><p class='lead'>{esc(s.get('body'))}</p><div class='btns center'>{c.btn(s.get('primary'),'primary','lg',True)}{c.btn(s.get('secondary'),'secondary','lg')}</div></div></div></section>")
    if lay == "photo":   # story with photo
        photo = c.img(s.get("photo"), "Hero: photo of the customer or partner", "ph", "height:480px;border-radius:24px")
        return (f"<section class='hero' style='background:{c.soft_bg}'><div class='wrap split'><div>{photo}</div><div><div class='eyebrow' style='color:{c.accent}'>{esc(s.get('eyebrow','Partner story'))}</div>"
                f"<h1 style='font-size:56px;line-height:64px'>{c.rich(s.get('headline','Headline'))}</h1><p class='lead'>{esc(s.get('body'))}</p>"
                + "".join(f"<div style='display:flex;gap:16px;margin-top:24px'><b>{esc(k)}</b><span class='muted'>{esc(v)}</span></div>" for k, v in s.get("facts", {}).items()) + "</div></div></section>")
    c.errors.append(f"Unknown hero layout '{lay}'. Use split, centred, screenshot, diagram, form, event, video, cards, chips or photo.")
    return ""


# ---------------------------------------------------------------- content sections
def features(s, c):
    cards = s.get("cards", [])
    if not 2 <= len(cards) <= 6: c.errors.append("Feature cards: use 2–6 cards (3 is the template).")
    cols = "g3" if len(cards) in (3, 5, 6) else "g2" if len(cards) in (2, 4) else "g3"
    ch = "".join(f"<div class='card'>{c.tile(k.get('icon','sparkle'))}<h3 style='margin-top:20px'>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:12px'>{esc(k.get('text'))}</p></div>" for k in cards)
    return f"<section class='sec'><div class='wrap'>{c.head(s)}<div class='grid {cols}'>{ch}</div></div></section>"


def benefits(s, c):   # Why choose: cards with a short list, on a blue band
    C = c.C; cards = s.get("cards", [])
    ch = "".join(f"<div class='card' style='border-radius:16px'>{c.tile(k.get('icon','check-circle'),40)}<h3 style='margin-top:20px'>{esc(k.get('title'))}</h3>"
                 f"<ul class='list'>{''.join(f'<li>{c.icon(chr(99)+chr(104)+chr(101)+chr(99)+chr(107), C[chr(98)+chr(108)+chr(117)+chr(101)+chr(47)+chr(49)+chr(48)+chr(48)], 20)}<span>{esc(p)}</span></li>' for p in k.get('points', []))}</ul></div>" for k in cards)
    return (f"<section class='sec dark' style='background:{C['blue/100']}'><div class='wrap'>{c.head(s, True)}"
            f"<div class='grid g3' style='background:{C['blue/150']};padding:12px;border-radius:24px'>{ch}</div></div></section>")


def bento(s, c):   # cards with a small product-screen slot
    cards = s.get("cards", [])
    ch = "".join(f"<div class='card' style='padding:28px;display:flex;flex-direction:column'><div class='muted' style='font-size:13px'>{i+1:02d}</div><h3 style='margin-top:8px'>{esc(k.get('title'))}</h3>"
                 f"<p class='muted' style='margin-top:10px;flex:1'>{esc(k.get('text'))}</p>{c.img(k.get('image'), 'Card: small product screen', 'ph', 'height:140px;margin-top:20px;border-radius:12px')}</div>" for i, k in enumerate(cards))
    return f"<section class='sec' style='background:{c.C['grey/10']}'><div class='wrap'>{c.head(s, align=s.get('align','left'))}<div class='grid g3'>{ch}</div></div></section>"


def options(s, c):   # one highlighted option + the rest
    C = c.C; items = s.get("options", [])
    if not items: return ""
    first, rest = items[0], items[1:]
    fh = (f"<div class='card dark' style='grid-column:span 2;background:{G_(c,'brand-depth')};border:0;padding:40px'>{c.tile(first.get('icon','cloud'),48,True)}<h3 style='margin-top:20px;font-size:32px;line-height:40px'>{esc(first.get('title'))}</h3>"
          f"<p style='margin-top:12px;color:{C['blue/20']}'>{esc(first.get('text'))}</p><div class='grid g4' style='margin-top:24px'>{''.join(f'<div style=background:#ffffff1f;border-radius:8px;padding:12px;font-size:14px;font-weight:600>{esc(x)}</div>' for x in first.get('points', []))}</div></div>")
    rh = "".join(f"<div class='card'>{c.tile(k.get('icon','stack'))}<h3 style='margin-top:20px'>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:12px'>{esc(k.get('text'))}</p></div>" for k in rest)
    note = f"<p class='muted' style='text-align:center;margin-top:40px'>{esc(s.get('note'))}</p>" if s.get("note") else ""
    return f"<section class='sec'><div class='wrap'>{c.head(s)}<div class='grid g3'>{fh}{rh}</div>{note}</div></section>"


def G_(c, name):
    return c.G[name]


def stacked(s, c):   # stacked feature cards on gradients
    C = c.C; grads = ["brand-depth", "midnight", "glow"]
    ch = "".join(f"<div class='dark' style='background:{c.G[grads[i%3]]};border-radius:24px;padding:48px;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;margin-bottom:24px'>"
                 f"<div><h3 style='font-size:32px;line-height:40px'>{esc(k.get('title'))}</h3><p style='margin-top:16px;color:{C['blue/20']}'>{esc(k.get('text'))}</p>"
                 f"<div style='display:flex;gap:8px;flex-wrap:wrap;margin-top:24px'>{''.join(f'<span class=pill2>{esc(x)}</span>' for x in k.get('points', []))}</div></div>"
                 f"<div class='uicard' style='color:{C['grey/160']}'>{f'<b style=font-size:48px;line-height:56px;color:{C[chr(98)+chr(108)+chr(117)+chr(101)+chr(47)+chr(49)+chr(48)+chr(48)]}>{esc(k[chr(115)+chr(116)+chr(97)+chr(116)])}</b>' if k.get('stat') else ''}"
                 f"<div class='muted'>{esc(k.get('stat_label','Product screen (replace)'))}</div></div></div>" for i, k in enumerate(s.get("cards", [])))
    return f"<section class='sec'><div class='wrap'>{c.head(s)}{ch}</div></section>"


def resources(s, c):   # link cards on CDS gradients
    grads = ["brand-depth", "midnight", "ai" if c.topic == "ai" else "glow", "glow" if c.topic == "ai" else "brand-depth"]
    ch = "".join(f"<a class='res' href='#' style='background:{c.G[grads[i%4]]};text-decoration:none'><h3>{esc(k.get('title'))}</h3><span style='align-self:flex-end'>{c.icon('arrow-right','#fff',24)}</span></a>" for i, k in enumerate(s.get("cards", [])))
    return f"<section class='sec'><div class='wrap'>{c.head(s)}<div class='grid g4'>{ch}</div></div></section>"


def tabs(s, c):
    C = c.C; lay = s.get("layout", "side"); dark = s.get("tone") == "dark"; items = s.get("tabs", [])
    if not items: return ""
    a = items[0]
    bg = f"background:{C['grey/170']}" if dark else ""
    body = (f"<div><h3 style='font-size:32px;line-height:40px'>{esc(a.get('title') or a.get('label'))}</h3><p class='muted' style='margin-top:12px'>{esc(a.get('text'))}</p>"
            f"<ul class='list'>{''.join(f'<li>{c.icon(chr(99)+chr(104)+chr(101)+chr(99)+chr(107)+chr(45)+chr(99)+chr(105)+chr(114)+chr(99)+chr(108)+chr(101), C[chr(98)+chr(108)+chr(117)+chr(101)+chr(47)+chr(49)+chr(48)+chr(48)], 20)}<span>{esc(p)}</span></li>' for p in a.get('points', []))}</ul></div>")
    pic = c.img(a.get("image"), "Tab: photo or product screen", "ph", "height:380px;border-radius:16px")
    panel = f"<div class='card' style='display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center;{'color:'+C['grey/160'] if dark else ''}'>{body}{pic}</div>"
    if lay == "top":
        tl = "".join(f"<div class='{'on' if i==0 else ''}'>{esc(t.get('label'))}</div>" for i, t in enumerate(items))
        return f"<section class='sec' style='{bg or 'background:'+C['grey/10']}'><div class='wrap'>{c.head(s, dark)}<div class='toptabs'>{tl}</div>{panel}</div></section>"
    if lay == "bigtext":
        tl = "".join(f"<div class='{'on' if i==0 else ''}'>{'› ' if i==0 else ''}{esc(t.get('label'))}</div>" for i, t in enumerate(items))
        return f"<section class='sec {'dark' if dark else ''}' style='{bg}'><div class='wrap'>{c.head(s, dark)}<div class='tabs-side' style='grid-template-columns:1fr 1fr'><div class='bigtabs'>{tl}</div>{panel}</div></div></section>"
    tl = "".join(f"<div class='tab {'on' if i==0 else ''}'>{c.tile(t.get('icon','circle'),32, dark and i!=0)}<span style='flex:1'>{esc(t.get('label'))}</span>{c.icon('caret-right', C['grey/100'], 18)}</div>" for i, t in enumerate(items))
    return f"<section class='sec {'dark' if dark else ''}' style='{bg}'><div class='wrap'>{c.head(s, dark) if s.get('title') else ''}<div class='tabs-side'><div class='tablist'>{tl}</div>{panel}</div></div></section>"


def accordion(s, c):
    C = c.C; lay = s.get("layout", "steps"); items = s.get("items", [])
    if lay == "photos":
        ph = "".join(f"<div style='flex:{3 if i==0 else 1};position:relative'>{c.img(k.get('photo'), 'Photo: '+(k.get('label') or 'role'), 'ph', 'height:420px;border-radius:16px')}"
                     f"<span class='chip' style='position:absolute;left:16px;bottom:16px'>{esc(k.get('label'))}</span></div>" for i, k in enumerate(items))
        a = items[0] if items else {}
        return (f"<section class='sec'><div class='wrap'>{c.head(s)}<div style='display:flex;gap:16px'>{ph}</div>"
                f"<div class='center' style='text-align:center;max-width:720px;margin:40px auto 0'><h3>{esc(a.get('label'))}</h3><p class='muted' style='margin-top:8px'>{esc(a.get('text'))}</p></div></div></section>")
    if lay == "side":
        a = items[0] if items else {}
        rest = "".join(f"<div style='width:96px;border-left:1px solid {C['blue/30']};background:{C['blue/10']};display:flex;flex-direction:column;justify-content:space-between;align-items:center;padding:24px 0'>"
                       f"<span style='writing-mode:vertical-rl;transform:rotate(180deg);font-weight:600'>{esc(k.get('label'))}</span><b style='color:{C['blue/100']}'>{i+2:02d}</b></div>" for i, k in enumerate(items[1:]))
        return (f"<section class='sec' style='background:{C['grey/20']}'><div class='wrap'>{c.head(s)}<div class='card' style='display:flex;padding:0;overflow:hidden'>"
                f"<div style='flex:1;padding:48px'><b style='font-size:88px;line-height:96px;color:{C['blue/30']}'>01</b><h3 style='font-size:32px;line-height:40px;margin-top:16px'>{esc(a.get('label'))}</h3>"
                f"<p class='muted' style='margin-top:12px'>{esc(a.get('text'))}</p></div>{rest}</div></div></section>")
    # steps: first item open with 3 columns
    out = []
    for i, k in enumerate(items):
        cols = "".join(f"<div><div class='muted' style='font-size:13px'>{j+1:02d}</div><h4 style='margin-top:4px'>{esc(st.get('title'))}</h4><ul class='list'>{''.join(f'<li>{c.icon(chr(99)+chr(104)+chr(101)+chr(99)+chr(107), c.tile_fg, 18)}<span>{esc(p)}</span></li>' for p in st.get('points', []))}</ul></div>" for j, st in enumerate(k.get("steps", []))) if i == 0 else ""
        out.append(f"<div class='acc'><div class='ah'>{c.tile(k.get('icon','stack'),48)}<div class='t'><h3>{esc(k.get('title'))}</h3><p class='muted'>{esc(k.get('text'))}</p></div>{c.icon('minus' if i==0 else 'plus', C['grey/120'], 24)}</div>"
                   + (f"<div class='ab'><div class='grid g3'>{cols}</div></div>" if cols else "") + "</div>")
    return f"<section class='sec dark' style='background:{C['grey/180']}'><div class='wrap'>{c.head(s, True)}<div style='color:{C['grey/160']}'>{''.join(out)}</div></div></section>"


def steps(s, c):
    C = c.C
    if s.get("layout") == "timeline":
        tl = "".join(f"<div class='tl'><div class='when'>{esc(k.get('when'))}</div><div class='card' style='padding:24px'><h3>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:8px'>{esc(k.get('text'))}</p></div></div>" for k in s.get("items", []))
        return f"<section class='sec'><div class='wrap'>{c.head(s, align='left')}<div class='timeline'>{tl}</div></div></section>"
    st = "".join(f"<div class='step'><span class='num'>{i+1:02d}</span><div class='card' style='padding:28px'><h3>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:8px'>{esc(k.get('text'))}</p>"
                 f"{''.join(f'<span class=stag>{esc(x)}</span>' for x in k.get('tags', []))}</div></div>" for i, k in enumerate(s.get("items", [])))
    return f"<section class='sec'><div class='wrap steps'><div style='position:sticky;top:120px;align-self:start'>{c.head(s, align='left')}</div><div>{st}</div></div></section>"


def comparison(s, c):
    C = c.C; them, us = s.get("them", {}), s.get("us", {})
    th = "".join(f"<li>{c.icon('x', C['grey/100'], 20)}<span>{esc(x)}</span></li>" for x in them.get("points", []))
    uh = "".join(f"<li>{c.icon('check-circle', C['blue/100'], 20)}<span>{esc(x)}</span></li>" for x in us.get("points", []))
    return (f"<section class='sec'><div class='wrap'>{c.head(s)}<div class='vs'><div class='col' style='background:{C['grey/10']}'><div class='eyebrow muted'>{esc(them.get('label','Other tools'))}</div><ul class='list'>{th}</ul></div>"
            f"<div class='col' style='background:{c.soft_bg};border:1px solid {C['blue/30']}'><div class='eyebrow' style='color:{c.accent}'>{esc(us.get('label','Zoho Creator'))}</div><ul class='list'>{uh}</ul>"
            f"{c.img(us.get('image'), 'Comparison: product diagram or screen', 'ph', 'height:260px;margin-top:24px')}</div></div></div></section>")


def darklist(s, c):   # two-column list or benefit grid on a dark background
    C = c.C; items = s.get("items", [])
    if s.get("layout") == "cards":
        ih = "".join(f"<div class='card dark' style='background:#ffffff0a;border-color:#ffffff1f;box-shadow:none'>{c.tile(k.get('icon','sparkle'),48,True)}<h3 style='margin-top:20px'>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:10px'>{esc(k.get('text'))}</p></div>" for k in items)
        return f"<section class='sec dark' style='background:{C['grey/180']}'><div class='wrap'>{c.head(s, True, 'left')}<div class='grid g3'>{ih}</div></div></section>"
    ih = "".join(f"<div style='display:flex;gap:16px;padding:24px 0;border-top:1px solid #ffffff1f'>{c.icon(k.get('icon','check-circle'), C['blue/50'], 24)}<div><h4>{esc(k.get('title'))}</h4><p class='muted' style='margin-top:6px'>{esc(k.get('text'))}</p></div></div>" for k in items)
    return f"<section class='sec dark' style='background:{c.G['midnight']}'><div class='wrap'>{c.head(s, True)}<div class='grid g2' style='column-gap:64px'>{ih}</div></div></section>"


def columns(s, c):   # three columns of lists + dark banner
    C = c.C
    ch = "".join(f"<div><h3 style='margin-bottom:16px'>{esc(col.get('title'))}</h3>{''.join(f'<div class=colrow>{c.tile(it.get(chr(105)+chr(99)+chr(111)+chr(110), chr(115)+chr(116)+chr(97)+chr(99)+chr(107)), 32)}<div><b>{esc(it.get(chr(116)+chr(105)+chr(116)+chr(108)+chr(101)))}</b><p class=muted style=font-size:14px>{esc(it.get(chr(116)+chr(101)+chr(120)+chr(116)))}</p></div></div>' for it in col.get('items', []))}</div>" for col in s.get("columns", []))
    b = s.get("banner")
    bh = (f"<div class='dark' style='margin-top:48px;background:{C['grey/180']};border-radius:24px;padding:40px;display:flex;gap:24px;align-items:center'>{c.tile(b.get('icon','cloud'),56,True)}"
          f"<div style='flex:1'><h3>{esc(b.get('title'))}</h3><p class='muted' style='margin-top:6px'>{esc(b.get('text'))}</p></div>{c.btn(b.get('button'),'inverse','sm')}</div>") if b else ""
    return f"<section class='sec'><div class='wrap'>{c.head(s)}<div class='grid g3' style='column-gap:48px'>{ch}</div>{bh}</div></section>"


def logos(s, c):
    lg = "".join(c.img(p, "Customer logo", "logo") if p else "<div class='logo'>Customer logo</div>" for p in (s.get("logos") or [None] * 6))
    if not s.get("logos"): c.samples.append("Logo wall: customer logos")
    stats = "".join(f"<div><b>{esc(x.get('value'))}</b><span>{esc(x.get('label'))}</span>{f'<small>{esc(x.get(chr(115)+chr(111)+chr(117)+chr(114)+chr(99)+chr(101)))}</small>' if x.get('source') else ''}</div>" for x in s.get("stats", []))
    for x in s.get("stats", []):
        if not x.get("source"): c.errors.append(f"Stat '{x.get('value')}' has no source. Never publish a number without one.")
    eb = f"<p class='muted' style='text-align:center;margin-bottom:24px'>{esc(s.get('eyebrow') or s.get('title','Trusted by teams worldwide'))}</p>"
    return f"<section style='padding:64px 0;border-bottom:1px solid {c.C['grey/40']}'><div class='wrap'>{eb}{f'<div class=stats4 style=margin-bottom:40px>{stats}</div>' if stats else ''}<div class='logos'>{lg}</div></div></section>"


def stats(s, c):
    st = s.get("stats", [])
    for x in st:
        if not x.get("source"): c.errors.append(f"Stat '{x.get('value')}' has no source. Never publish a number without one.")
    sh = "".join(f"<div class='card' style='padding:32px'><b>{esc(x.get('value','00%'))}</b><span>{esc(x.get('label'))}</span><small>{esc(x.get('source','Source: add source'))}</small></div>" for x in st)
    return f"<section class='sec' style='background:{c.C['blue/10']}'><div class='wrap'>{c.head(s)}<div class='stats4'>{sh}</div></div></section>"


def story_cards(s, c):
    ch = "".join(f"<div class='card' style='padding:28px'>{c.img(k.get('logo'), 'Story card: customer logo', 'ph', 'height:56px;width:160px;border-radius:8px')}"
                 f"<div class='eyebrow' style='color:{c.accent};margin-top:20px'>{esc(k.get('tag'))}</div><h3>{esc(k.get('title'))}</h3><p class='muted' style='margin-top:8px'>{esc(k.get('text'))}</p>"
                 f"<a href='#' style='display:inline-flex;gap:8px;margin-top:16px;color:{c.C['blue/100']};font-weight:600;text-decoration:none'>Read the story {c.icon('arrow-right', c.C['blue/100'], 18)}</a></div>" for k in s.get("cards", []))
    return f"<section class='sec'><div class='wrap'>{c.head(s) if s.get('title') else ''}<div class='grid g3'>{ch}</div></div></section>"


def platform(s, c):   # layered platform visual + text blocks
    C = c.C; layers = s.get("layers", [])
    lh = "".join(f"<div class='layer' style='background:{['#fff', C['blue/10'], C['blue/20'], C['blue/30']][i%4]};border:1px solid {C['blue/30']};margin-left:{i*16}px;margin-right:{i*16}px'>{c.tile(l.get('icon','stack'),32)}{esc(l.get('label'))}</div>" for i, l in enumerate(layers))
    bl = "".join(f"<div style='padding:20px 0;border-top:1px solid {C['grey/40']}'><h4>{esc(b.get('title'))}</h4><p class='muted' style='margin-top:6px'>{esc(b.get('text'))}</p></div>" for b in s.get("blocks", []))
    return f"<section class='sec' style='background:{C['grey/10']}'><div class='wrap'>{c.head(s, align='left')}<div class='grid g2' style='gap:80px;align-items:center'><div>{bl}</div><div class='layers'>{lh}</div></div></div></section>"


def orbit(s, c):   # agent lifecycle: sphere with the AI agent bot, stage nodes, step panels
    C = c.C; nodes = s.get("nodes", [])[:6]
    bot = b64(A / "illustrations" / "ai-agent-bot.svg", "image/svg+xml")
    import math
    nh = "".join(f"<div class='node' style='left:{50+42*math.cos(math.radians(-90+i*360/max(1,len(nodes))))}%;top:{50+42*math.sin(math.radians(-90+i*360/max(1,len(nodes))))}%'>"
                 f"<span class='itile' style='width:56px;height:56px;border-radius:999px;background:{C['blue/160']};box-shadow:inset 0 0 0 1px #ffffff29'>{c.icon(n.get('icon','sparkle'), C['blue/50'], 24)}</span>{esc(n.get('label'))}</div>" for i, n in enumerate(nodes))
    rings = "".join(f"<div class='ring' style='left:{50-r/2}%;top:{50-r/2}%;width:{r}%;height:{r}%'></div>" for r in (84, 60))
    st = "".join(f"<div style='margin-bottom:56px'><div class='muted' style='font-size:13px'>{i+1:02d}</div><h3 style='font-size:40px;line-height:48px;margin-top:4px'>{esc(k.get('title'))}</h3>"
                 f"<p class='muted' style='margin-top:12px;max-width:520px'>{esc(k.get('text'))}</p>{c.img(k.get('image'), 'Step: product screen', 'ph', 'height:220px;max-width:520px;margin-top:20px;border-radius:16px')}</div>" for i, k in enumerate(s.get("steps", [])))
    return (f"<section class='sec dark' style='background:{C['grey/180']}'><div class='wrap'>{c.head(s, True)}<div class='grid g2' style='align-items:start;gap:64px'>"
            f"<div style='position:sticky;top:96px'><div class='orbit'>{rings}<div class='sphere'><img src='{bot}' width='190' alt='AI agent'></div>{nh}</div></div><div>{st}</div></div></div></section>")


def faq(s, c):
    C = c.C; dark = s.get("tone") == "dark"; items = s.get("items", [])
    qa = "".join(f"<div class='qa'><div class='q'><span>{esc(k.get('q'))}</span>{c.icon('minus' if i==0 else 'plus', C['blue/50'] if dark else C['blue/100'], 22)}</div>{f'<p class=a>{esc(k.get(chr(97)))}</p>' if i==0 and k.get('a') else ''}</div>" for i, k in enumerate(items))
    return f"<section class='sec {'dark' if dark else ''}' style='background:{C['grey/180'] if dark else '#fff'}'><div class='wrap faq'><div><h2>{c.rich(s.get('title','Frequently asked questions'), dark)}</h2></div><div>{qa}</div></div></section>"


def testimonial(s, c):
    C = c.C; lay = s.get("layout", "card")
    who = (f"<div class='person'>{c.img(s.get('photo'), 'Testimonial: photo', 'avatar') if s.get('photo') else '<span class=avatar></span>'}"
           f"<div><b>{esc(s.get('name','Name'))}</b><div class='muted' style='font-size:14px'>{esc(s.get('role','Role, Company'))}</div></div></div>")
    if not s.get("photo"): c.samples.append("Testimonial: photo")
    if lay == "large":
        return (f"<section class='sec' style='background:{c.soft_bg}'><div class='wrap' style='max-width:1100px;text-align:center'><div class='quote' style='font-size:48px;line-height:56px'>“{c.rich(s.get('quote',''))}”</div>"
                f"<div style='display:flex;justify-content:center'>{who}</div></div></section>")
    return (f"<section class='sec' style='background:{c.mesh_bg}'><div class='wrap' style='max-width:1100px'><div class='card' style='padding:56px'><div class='eyebrow' style='color:{c.accent}'>{esc(s.get('eyebrow','Customer story'))}</div>"
            f"<div class='quote'>“{c.rich(s.get('quote',''))}”</div><div style='display:flex;justify-content:space-between;align-items:end'>{who}"
            f"{c.img(s.get('logo'), 'Testimonial: customer logo', 'logo')}</div></div></div></section>")


def cta(s, c):
    C = c.C; lay = s.get("layout", "band")
    if lay == "light":
        return (f"<section class='sec' style='background:{c.mesh_bg};text-align:center'><div class='wrap center' style='max-width:900px'><h2>{c.rich(s.get('headline',''))}</h2>"
                f"<p class='lead muted' style='margin-top:20px;font-size:20px;line-height:28px'>{esc(s.get('body'))}</p><div class='btns center'>{c.btn(s.get('primary'),'primary','lg',True)}{c.btn(s.get('secondary'),'secondary','lg')}</div></div></section>")
    if lay == "dark":
        return (f"<section class='sec dark' style='background:{C['blue/160']};text-align:center'><div style='position:absolute;left:50%;bottom:-200px;width:720px;height:400px;transform:translateX(-50%);border-radius:999px;background:{C['yellow/100']};opacity:.18;filter:blur(140px)'></div>"
                f"<div class='wrap center' style='max-width:900px;position:relative'><h2>{c.rich(s.get('headline',''), True)}</h2><div class='btns center'>{c.btn(s.get('primary'),'primary','lg',True)}</div></div></section>")
    tex = "" if c.topic == "ai" else f"<div class='tex' style='background-image:url({c.tex_light if c.topic=='default' else c.tex_bold});opacity:.08'></div>"
    bg = C["blue/100"] if c.topic == "default" else (c.G["ai"] if c.topic == "ai" else c.G["midnight"])
    return (f"<section class='sec dark' style='background:{bg};text-align:center'>{tex}<div class='wrap center' style='max-width:960px;position:relative'><h2>{c.rich(s.get('headline',''), True)}</h2>"
            f"{f'<p style=margin-top:20px;font-size:20px;line-height:28px>{esc(s.get(chr(98)+chr(111)+chr(100)+chr(121)))}</p>' if s.get('body') else ''}"
            f"<div class='btns center'>{c.btn(s.get('primary'),'primary','lg',True)}{c.btn(s.get('secondary'),'inverse','lg')}</div></div></section>")


RENDER = {"hero": hero, "features": features, "benefits": benefits, "bento": bento, "options": options, "stacked": stacked,
          "resources": resources, "tabs": tabs, "accordion": accordion, "steps": steps, "comparison": comparison,
          "darklist": darklist, "columns": columns, "logos": logos, "stats": stats, "stories": story_cards, "platform": platform,
          "orbit": orbit, "faq": faq, "testimonial": testimonial, "cta": cta}
