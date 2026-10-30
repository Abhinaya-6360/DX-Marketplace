"""Get a CDS icon as SVG markup or a file.

Usage:
  python icon.py list                        # all icon names
  python icon.py ai-sparkle                  # print Regular SVG
  python icon.py ai-sparkle --fill           # print Fill SVG (selected/active only)
  python icon.py ai-sparkle --size 24 --color "#0d4ef2" --out sparkle.svg

Colour defaults to currentColor, so inline SVG takes the CSS text colour.
Only icons in this library may be used (see assets/icons/icons.json for rules and tile spec).
"""
import json, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "assets" / "icons" / "icons.json"


def svg(name, weight="regular", size=None, color=None):
    data = json.load(open(LIB))["library"]
    if name not in data:
        close = [n for n in data if name.replace("-", "") in n.replace("-", "")][:8]
        sys.exit(f"No icon '{name}'. Close matches: {', '.join(close) or 'none'}. Run: python icon.py list")
    i = data[name][weight]
    attrs = f'xmlns="http://www.w3.org/2000/svg" viewBox="{i["viewBox"]}"'
    if size:
        attrs += f' width="{size}" height="{size}"'
    body = i["body"].replace("currentColor", color) if color else i["body"]
    style = f' style="color:{color}"' if color else ""
    return f"<svg {attrs}{style}>{body}</svg>"


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "list":
        print("\n".join(sorted(json.load(open(LIB))["library"]))); sys.exit()
    weight = "fill" if "--fill" in a else "regular"
    size = a[a.index("--size") + 1] if "--size" in a else None
    color = a[a.index("--color") + 1] if "--color" in a else None
    out = svg(a[0], weight, size, color)
    if "--out" in a:
        Path(a[a.index("--out") + 1]).write_text(out); print("saved", a[a.index("--out") + 1])
    else:
        print(out)
