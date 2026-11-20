"""CDS 2.0 system guard: flag anything that isn't from the system.

Usage:
  python check_system.py <file> [<file> ...] [--topic ai|partner] [--email]
      Checks a brief (.json), web or email page (.html/.css), SVG, deck (.pptx),
      or plain copy (.txt/.md). Prints every SYSTEM VIOLATION; exit code 1 if any.
  python check_system.py contrast "#25272c" "#ffffff" [--large]
      Contrast ratio and WCAG AA verdict for one pair.
  python check_system.py pairs
      The CDS text/background pairs that pass WCAG AA (use these first).
  python check_system.py emoji "<text>"
      Flags emoji and outside symbols in a piece of copy and names the CDS icon to use.

What it checks
  1. Emoji and outside symbols (✅ 🚀 ★ ✓ ❤ …): never in CDS work. Use a CDS icon.
  2. Colours: every hex/rgb value must be a CDS token (colour, role, gradient, elevation).
  3. Fonts: Zoho Puvi only (email: Georgia and Helvetica Neue).
  4. Icons: inline SVG icons must come from assets/icons/icons.json. A new icon drawn because
     none fitted must carry data-cds-new-icon="<name>", use viewBox 0 0 32 32, stroke-width 2
     and currentColor; it is listed as NEW ICON for design review, not as a violation.
  5. Red: only on the main button (or a form error); everything else is flagged.
  6. Violet: only when the topic is AI or partner (--topic ai|partner).
  7. Contrast (WCAG AA): 4.5:1 for normal text, 3:1 for large text (24 px+, or 19 px+
     Semibold/Bold) and for icons and UI shapes.

Other scripts import `text_violations` and `brief_violations` so a brief with emoji or
outside colours fails before anything is rendered.
"""
import html as htmllib, json, os, re, sys, zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
A = SKILL / "assets"
TOK = json.load(open(SKILL / "design-system" / "tokens.json"))
ICONS = json.load(open(A / "icons" / "icons.json"))["library"]

# ---------- palette ----------
COL = {k: v.lower() for k, v in TOK["colour"].items()}
ROLE = {f"role/{k}": v["value"].lower() for k, v in TOK["role"].items()}
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def norm(h):
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h[:6]


ALLOWED = set(COL.values()) | set(ROLE.values())
for g in TOK["gradients"].values():
    ALLOWED |= {norm(h) for h in HEX_RE.findall(g["css"])}
for e in TOK["elevation"].values():
    ALLOWED |= {norm(h) for h in HEX_RE.findall(e)}
NAME = {}
for k, v in COL.items():
    NAME.setdefault(v, k)
def _family(h, fam, lo):
    k = nearest(norm(h))
    return k.startswith(fam + "/") and int(k.split("/")[1]) >= lo


def is_red(h):
    return _family(h, "red", 80)


def is_violet(h):
    return _family(h, "violet", 60)


def rgb(h):
    h = norm(h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def nearest(h):
    r = rgb(h)
    return min(COL, key=lambda k: sum((a - b) ** 2 for a, b in zip(r, rgb(COL[k]))))


def lum(h):
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def aa(fg, bg, large=False):
    r = ratio(fg, bg)
    return r, r >= (3.0 if large else 4.5)


# ---------- emoji and outside symbols ----------
# Arrows (U+2190–21FF), bullets, dashes, quotes, ©®™ and maths are fine in copy.
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF"
    "\U0000FE0F\U0000200D\U000020E3\U00002300-\U000023FF\U000025A0-\U000025FF]"
)
EMOJI_TO_ICON = {
    "✅": "check-circle", "✔": "check", "✓": "check", "☑": "check-square", "❌": "x-circle",
    "✖": "x", "✗": "x", "⚠": "warning", "ℹ": "info", "❓": "question", "❗": "warning-circle",
    "🚀": "rocket-launch", "⭐": "star", "★": "star", "☆": "star", "🌟": "star", "✨": "sparkle",
    "💡": "lightbulb", "📈": "trend-up", "📉": "trend-down", "📊": "chart-bar", "🔒": "lock",
    "🔓": "lock-open", "🔑": "key", "⚡": "lightning", "🤖": "robot", "🧠": "brain",
    "📅": "calendar-blank", "🗓": "calendar-blank", "⏰": "clock", "⏱": "clock", "🕒": "clock",
    "📍": "map-pin", "🌍": "globe", "🌎": "globe", "🌐": "globe", "👥": "users", "👤": "user",
    "🤝": "handshake", "🏆": "trophy", "🥇": "medal", "🎯": "target", "🎁": "gift",
    "🔥": "fire", "❤": "heart", "♥": "heart", "👍": "thumbs-up", "👎": "thumbs-down",
    "📣": "megaphone", "📢": "megaphone", "🔔": "bell", "📧": "envelope-simple",
    "✉": "envelope-simple", "📞": "phone", "☎": "phone", "💬": "chat", "🔗": "link",
    "⚙": "gear", "🛠": "wrench", "🔧": "wrench", "🔍": "magnifying-glass", "📱": "device-mobile",
    "💻": "laptop", "🖥": "monitor", "☁": "cloud", "📦": "package", "🚚": "truck",
    "🛒": "shopping-cart", "💳": "credit-card", "💰": "money", "💵": "currency-dollar",
    "📄": "file-text", "📁": "folder", "📝": "pencil-simple", "✏": "pencil", "🏢": "buildings",
    "🏦": "bank", "🏭": "factory", "🏥": "hospital", "🎓": "graduation-cap", "🎉": "star",
    "👉": "arrow-right", "➡": "arrow-right", "▶": "play", "⏯": "play", "🎥": "video-camera",
    "🎙": "microphone", "🎧": "headphones", "🧩": "puzzle-piece", "🛡": "shield-check",
    "⏳": "spinner", "♾": "infinity", "☀": "sun", "🌙": "moon",
}


def text_violations(s, where=""):
    out = []
    for m in EMOJI_RE.finditer(s or ""):
        ch = m.group()
        if ch in "️‍⃣":
            continue
        icon = EMOJI_TO_ICON.get(ch)
        hint = f"use the CDS icon `{icon}`" if icon and icon in ICONS else "use a CDS icon (python scripts/icon.py list) or drop it"
        out.append(f"{where}emoji/symbol '{ch}' in “{s.strip()[:60]}” — {hint}")
    return out


def _strings(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from _strings(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _strings(v, f"{path}[{i}]")


def colour_violations(s, where=""):
    out = []
    for h in set(HEX_RE.findall(s)):
        n = norm(h)
        if n not in ALLOWED:
            k = nearest(n)
            out.append(f"{where}colour {h} is not a CDS colour — use {k} ({COL[k]})")
    for m in set(re.findall(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)):
        n = "#" + "".join(f"{int(c):02x}" for c in m)
        if n not in ALLOWED:
            k = nearest(n)
            out.append(f"{where}colour rgb({','.join(m)}) is not a CDS colour — use {k} ({COL[k]})")
    return out


def brief_violations(brief, topic=None):
    """For the JSON briefs the render/build scripts take."""
    out = []
    topic = topic or (brief.get("topic") if isinstance(brief, dict) else None)
    for path, s in _strings(brief):
        if re.search(r"icon\d?$", path.split(".")[-1]) and s.strip().lower() == "robot" and topic == "ai":
            out.append(f"{path}: robot icon on an AI piece — use ai-sparkle (robot is only for a literal robot)")
        out += text_violations(s, f"{path}: ")
        if HEX_RE.search(s) and not s.lower().endswith((".png", ".jpg", ".svg")):
            out += colour_violations(s, f"{path}: ")
    return out


# ---------- files ----------
NEW_ICONS = []   # icons drawn because none fitted: reported for design review
ICON_BODIES = set()
for v in ICONS.values():
    for w in ("regular", "fill"):
        ICON_BODIES |= set(re.findall(r'd="([^"]{20,})"', v[w]["body"]))
ASSET_PATHS = set()
for p in list((A / "logos").rglob("*.svg")) + list((A / "shapes").rglob("*.svg")) + list((A / "patterns").rglob("*.svg")):
    ASSET_PATHS |= set(re.findall(r'd="([^"]{20,})"', p.read_text(errors="ignore")))


def css_blocks(src):
    for m in re.finditer(r"style\s*=\s*['\"]([^'\"]+)['\"]", src):
        yield m.group(1)
    for m in re.finditer(r"\{([^{}]+)\}", src):
        yield m.group(1)


def decl(block, prop):
    m = re.search(rf"(?:^|;)\s*{prop}\s*:\s*([^;]+)", block)
    return m.group(1).strip() if m else None


def check_html(src, email=False, topic=None):
    out = []
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", src, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    out += text_violations(re.sub(r"\s+", " ", text))
    body = htmllib.unescape(re.sub(r"data:[^'\")]+", "", src))   # skip embedded fonts/images
    out += colour_violations(body)
    fonts_ok = ["zoho puvi"] + (["georgia", "helvetica neue", "helvetica", "arial", "sans-serif", "serif"] if email else [])
    for fam in set(re.findall(r"font-family\s*:\s*([^;\"'}]+)", body)):
        first = fam.split(",")[0].strip().strip("'\"").lower()
        if first and first not in fonts_ok and not first.startswith("var("):
            out.append(f"font '{first}' is not in the system — use Zoho Puvi" + (" (email: Georgia / Helvetica Neue)" if email else ""))
    for svg in re.findall(r"<svg\b.*?</svg>", body, flags=re.S | re.I):
        new = re.search(r'data-cds-new-icon="([^"]+)"', svg)
        if new:
            ok = ('viewBox="0 0 32 32"' in svg and re.search(r'stroke-width="2"', svg)
                  and "currentColor" in svg and not re.search(r"<text\b", svg, flags=re.I))
            if ok:
                NEW_ICONS.append(new.group(1))
            else:
                out.append(f"new icon '{new.group(1)}' doesn't follow the CDS custom style — viewBox 0 0 32 32, "
                           "stroke-width 2, currentColor, no text (brand-rules.md > Icons)")
            continue
        ds = re.findall(r'\sd="([^"]{20,})"', svg)
        if ds and not all(d in ICON_BODIES or d in ASSET_PATHS for d in ds):
            if re.search(r'viewBox="0 0 (256|32|24|16|20) ', svg):
                out.append("an inline SVG icon is not from the CDS icon set — get it with python scripts/icon.py <name>")
    for b in css_blocks(body):
        fg, bg = decl(b, "color"), decl(b, "background(?:-color)?")
        if fg and bg:
            f, g = HEX_RE.search(fg), [h for h in HEX_RE.findall(bg) if not (len(h) == 9 and h[7:].lower() != 'ff')]  # skip see-through backgrounds
            if f and g:
                size = decl(b, "font-size"); wt = decl(b, "font-weight") or "400"
                px = float(re.match(r"[\d.]+", size).group()) if size and re.match(r"[\d.]+", size) else 16
                large = px >= 24 or (px >= 18.66 and wt.strip()[:1] in "6789")
                worst = min(ratio(f.group(), h) for h in g)
                if worst < (3.0 if large else 4.5):
                    out.append(f"contrast {worst:.1f}:1 for {norm(f.group())} on {', '.join(norm(h) for h in g)} fails WCAG AA "
                               f"({'3' if large else '4.5'}:1 needed) — pick a pair from `python scripts/check_system.py pairs`")
    for m in re.finditer(r"<(?P<tag>\w+)(?P<attrs>[^>]*)>", body):
        attrs = m.group("attrs").lower()
        if any(is_red(h) for h in HEX_RE.findall(attrs)):
            if not (m.group("tag").lower() in ("a", "button", "td", "table") and re.search(r"btn|button|cta|bgcolor|background", attrs)) and "error" not in attrs:
                out.append(f"red on <{m.group('tag')}> that isn't the main button — red is only for the main button or a form error")
    if topic not in ("ai", "partner") and any(is_violet(h) for h in HEX_RE.findall(body)):
        out.append("violet is used, but the topic isn't AI or partner — use blue, or pass --topic ai|partner if it is")
    out += ai_violations(body)
    return out


AI_GRAD_RE = re.compile(r"gradient\([^;'\"]*#0d4ef2[^;'\"]*#5e05ff", re.I)
ROBOT_PATHS = set(re.findall(r'd="([^"]{20,})"', ICONS["robot"]["regular"]["body"] + ICONS["robot"]["fill"]["body"])) if "robot" in ICONS else set()


def ai_violations(body):
    """AI rules (Nov 2026): violet is an accent only; no violet text on the AI gradient; no robot for AI."""
    from html.parser import HTMLParser
    out = []
    rules = {}
    for sel, dec in re.findall(r"([^{}]+)\{([^{}]*)\}", " ".join(re.findall(r"<style[^>]*>(.*?)</style>", body, flags=re.S | re.I))):
        for one in sel.split(","):
            one = one.strip()
            if re.fullmatch(r"\.[\w-]+", one):
                rules[one[1:]] = rules.get(one[1:], "") + ";" + dec
    found = set()

    VOID = ("br", "img", "meta", "link", "input", "hr", "path", "rect", "circle", "line", "polyline", "polygon", "ellipse", "stop", "use")

    class W(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = [(False, False)]   # (inside the AI gradient, inside a CDS 3D tile)
        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            st = ";".join(rules.get(c, "") for c in (a.get("class") or "").split()) + ";" + (a.get("style") or "")
            ai, tile = self.stack[-1]
            tile = tile or (a.get("data-el") or "").strip().lower() == "tile"   # the 3D tile artwork may be violet on AI pieces
            bg = decl(st, "background(?:-color)?")
            if bg:
                if AI_GRAD_RE.search(bg):
                    ai = True
                elif HEX_RE.search(bg) or "gradient" in bg:
                    ai = False
                h = HEX_RE.fullmatch(bg.strip())
                small = re.search(r"(?:^|;)\s*height\s*:\s*(\d+(?:\.\d+)?)px", st)
                if h and is_violet(bg.strip()) and not tile and not (small and float(small.group(1)) <= 64) and tag not in ("span",):
                    found.add("solid violet background on a card, panel or button — on AI pieces violet is an accent only; use blue or the AI gradient")
            col = decl(st, "color")
            if ai and col and HEX_RE.search(col) and is_violet(HEX_RE.search(col).group()):
                found.add("violet text on the AI gradient can't be read — use white text and yellow/100 for highlight words")
            if tag not in VOID:
                self.stack.append((ai, tile))
        def handle_endtag(self, tag):
            if len(self.stack) > 1 and tag not in VOID:
                self.stack.pop()
        def handle_startendtag(self, tag, attrs):
            pass

    W().feed(body)
    out += sorted(found)
    if ROBOT_PATHS and any(d in ROBOT_PATHS for d in re.findall(r'\sd="([^"]{20,})"', body)):
        out.append("robot icon used — ai-sparkle is the AI icon; robot is only for a literal robot")
    return out


def check_pptx(path, topic=None):
    out = []
    z = zipfile.ZipFile(path)
    for n in sorted(x for x in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml", x)):
        x = z.read(n).decode("utf8", "ignore"); where = f"{Path(n).stem}: "
        for t in re.findall(r"<a:t>([^<]*)</a:t>", x):
            out += text_violations(t, where)
        for v in set(re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', x)):
            if norm(v) not in ALLOWED:
                k = nearest(norm(v)); out.append(f"{where}colour #{v} is not a CDS colour — use {k} ({COL[k]})")
        for f in set(re.findall(r'typeface="([^"]+)"', x)):
            if not f.startswith("+") and "zoho puvi" not in f.lower():
                out.append(f"{where}font '{f}' is not in the system — use Zoho Puvi")
        if topic not in ("ai", "partner") and any(is_violet(v) for v in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', x)):
            out.append(f"{where}violet on a slide whose topic isn't AI or partner")
    return out


def check_file(p, topic=None, email=False):
    p = Path(p); s = p.suffix.lower()
    if s == ".pptx":
        return check_pptx(p, topic)
    src = p.read_text(errors="ignore")
    if s == ".json":
        return brief_violations(json.loads(src), topic)
    if s in (".html", ".htm", ".css", ".svg"):
        return check_html(src, email=email or "email" in p.name.lower(), topic=topic)
    return text_violations(src) + colour_violations(src)


def pairs():
    bgs = ["base/white", "grey/10", "blue/10", "blue/20", "violet/20", "yellow/100", "blue/100", "blue/130", "blue/160", "grey/160", "grey/180", "violet/100"]
    fgs = ["grey/160", "grey/120", "blue/100", "blue/130", "violet/100", "base/white", "grey/180", "yellow/100", "blue/40"]
    rows = []
    for b in bgs:
        ok = []
        for f in fgs:
            if f == b or f not in COL or b not in COL:
                continue
            r = ratio(COL[f], COL[b])
            if r >= 3:
                ok.append(f"{f} {r:.1f}{'' if r >= 4.5 else ' (large text and icons only)'}")
        rows.append(f"{b:<12} {COL.get(b,'')}  →  " + " · ".join(ok))
    return "\n".join(rows)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "pairs":
        print("Text (or icon) colour on each background, with contrast; plain numbers pass AA for all text.\n" + pairs()); sys.exit()
    if a[0] == "contrast":
        large = "--large" in a; r, ok = aa(a[1], a[2], large)
        print(f"{r:.2f}:1 — {'passes' if ok else 'FAILS'} WCAG AA for {'large' if large else 'normal'} text"); sys.exit(0 if ok else 1)
    if a[0] == "emoji":
        v = text_violations(" ".join(a[1:])); print("\n".join(v) or "No emoji or outside symbols."); sys.exit(1 if v else 0)
    topic = a[a.index("--topic") + 1] if "--topic" in a else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--topic")]
    bad = 0
    for f in files:
        v = list(dict.fromkeys(check_file(f, topic, "--email" in a)))
        print(f"\n{f}: " + ("passes the CDS 2.0 system check" if not v else f"{len(v)} SYSTEM VIOLATION(S)"))
        for x in v:
            print("  ✗ " + x)
        bad += len(v)
    if NEW_ICONS:
        print("\nNEW ICON(S) for design review (drawn because no CDS icon fitted): " + ", ".join(dict.fromkeys(NEW_ICONS)))
        print("  List each one in the handover so the design team can add it to the CDS 2.0 library.")
    sys.exit(1 if bad else 0)


def guard(brief, argv, what="brief"):
    """Called by the build/render scripts: stop on system violations unless --allow-violation."""
    v = brief_violations(brief)
    if not v:
        return []
    print(f"SYSTEM VIOLATION(S) in the {what}:")
    for x in v:
        print("  ✗ " + x)
    if "--allow-violation" not in argv and os.environ.get("CDS_ALLOW_VIOLATION") != "1":
        print("Fix these (offer the marketer on-system options), or re-run with --allow-violation only if they insist; "
              "then list each one as a System violation in the handover.")
        sys.exit(2)
    print("Continuing because of --allow-violation. List these as System violations in the handover.")
    return v
