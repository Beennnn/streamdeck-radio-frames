#!/usr/bin/env python3
"""Generate the Radio-Button selection-frame SVGs into src/ + tags.json.

Two families, one SVG per colour:

  frame-<colour>.svg   Full rounded border hugging the key edge, transparent
                       centre. Sits BEHIND the Stream Deck title text so the
                       text reads inside a coloured frame -> "this key is the
                       selected member of its radio group".

  notch-<colour>.svg   Four L-shaped corner brackets (the "corner notches"),
                       leaving the whole centre free. Subtler than a full
                       frame; the funk profile used the same idea with a blue
                       liseré on one group and a yellow one on another.

Why an overlay and not a filled tile: the icon composites over the key's own
background, and the centre stays clear so the WHITE title text keeps maximum
contrast on every colour (yellow included). The bold coloured edge is the
whole selection signal.

Edit COLOURS below then run `python3 gen_frames.py` to regenerate everything.
Rasterise + package with the sdicons toolkit (see bin/build.sh).
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"

# Wide Tailwind-500-ish range, same vocabulary Beennnn already uses on the funk
# deck (#22C55E, #F59E0B, #38BDF8...). Order = rainbow-ish so the contact sheet
# reads like a swatch strip. (slug, Display Name, hex)
COLOURS = [
    ("white",   "White",   "#FFFFFF"),
    ("slate",   "Slate",   "#94A3B8"),
    ("red",     "Red",     "#EF4444"),
    ("orange",  "Orange",  "#F97316"),
    ("amber",   "Amber",   "#F59E0B"),
    ("yellow",  "Yellow",  "#FDE047"),
    ("lime",    "Lime",    "#84CC16"),
    ("green",   "Green",   "#22C55E"),
    ("emerald", "Emerald", "#10B981"),
    ("teal",    "Teal",    "#14B8A6"),
    ("cyan",    "Cyan",    "#22D3EE"),
    ("sky",     "Sky",     "#38BDF8"),
    ("blue",    "Blue",    "#3B82F6"),
    ("indigo",  "Indigo",  "#6366F1"),
    ("violet",  "Violet",  "#8B5CF6"),
    ("purple",  "Purple",  "#A855F7"),
    ("fuchsia", "Fuchsia", "#D946EF"),
    ("pink",    "Pink",    "#EC4899"),
    ("rose",    "Rose",    "#F43F5E"),
]

# --- geometry (144x144 canvas) --------------------------------------------
FRAME_INSET = 11      # px from edge to the frame centre-line
FRAME_R = 26          # corner radius of the frame
FRAME_W = 11          # coloured stroke width
HALO_W = 17           # dark under-stroke width (legibility on light keys)
HILITE_W = 2          # thin inner white highlight

NOTCH_INSET = 16      # px from edge to the bracket centre-line
NOTCH_ARM = 42        # bracket arm length
NOTCH_W = 13          # coloured stroke width
NOTCH_HALO = 18


def frame_svg(hexc: str) -> str:
    """Full coloured border, transparent centre, dark halo + inner highlight."""
    i = FRAME_INSET
    s = 144 - 2 * i
    inner = i + FRAME_W / 2 + HILITE_W + 1
    si = 144 - 2 * inner
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 144 144">
  <!-- dark halo so the frame stays visible on light key backgrounds -->
  <rect x="{i}" y="{i}" width="{s}" height="{s}" rx="{FRAME_R}"
        fill="none" stroke="#000000" stroke-opacity="0.38" stroke-width="{HALO_W}"/>
  <!-- coloured selection frame -->
  <rect x="{i}" y="{i}" width="{s}" height="{s}" rx="{FRAME_R}"
        fill="none" stroke="{hexc}" stroke-width="{FRAME_W}"/>
  <!-- faint inner highlight for a lit-edge feel -->
  <rect x="{inner}" y="{inner}" width="{si}" height="{si}" rx="{FRAME_R - 4}"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="{HILITE_W}"/>
</svg>
'''


def notch_svg(hexc: str) -> str:
    """Four L-shaped corner brackets ("corner notches"), centre fully clear."""
    n = NOTCH_INSET
    a = NOTCH_ARM
    f = 144 - n           # far edge
    brackets = [
        f"M{n} {n + a} L{n} {n} L{n + a} {n}",          # top-left
        f"M{f - a} {n} L{f} {n} L{f} {n + a}",          # top-right
        f"M{f} {f - a} L{f} {f} L{f - a} {f}",          # bottom-right
        f"M{n + a} {f} L{n} {f} L{n} {f - a}",          # bottom-left
    ]
    halo = "\n  ".join(
        f'<path d="{d}" fill="none" stroke="#000000" stroke-opacity="0.38" '
        f'stroke-width="{NOTCH_HALO}" stroke-linecap="round" stroke-linejoin="round"/>'
        for d in brackets
    )
    colour = "\n  ".join(
        f'<path d="{d}" fill="none" stroke="{hexc}" stroke-width="{NOTCH_W}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        for d in brackets
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 144 144">
  {halo}
  {colour}
</svg>
'''


def main():
    SRC.mkdir(exist_ok=True)
    tags = {}
    for slug, disp, hexc in COLOURS:
        (SRC / f"frame-{slug}.svg").write_text(frame_svg(hexc))
        (SRC / f"notch-{slug}.svg").write_text(notch_svg(hexc))
        tags[f"frame-{slug}"] = {
            "name": f"{disp} · Selected Frame",
            "tags": ["radio button", "selected", "frame", "border",
                     "highlight", slug],
        }
        tags[f"notch-{slug}"] = {
            "name": f"{disp} · Selected Corner Notch",
            "tags": ["radio button", "selected", "corner notch", "bracket",
                     "highlight", slug],
        }
    (ROOT / "tags.json").write_text(json.dumps(tags, indent=4, ensure_ascii=False) + "\n")
    print(f"wrote {len(COLOURS) * 2} SVGs + tags.json ({len(COLOURS)} colours x 2 families)")


if __name__ == "__main__":
    main()
