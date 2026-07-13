#!/usr/bin/env python3
"""Generate the Radio-Button selection-frame SVGs into src/ + tags.json.

Two families, one SVG per colour:

  frame-<colour>.svg   Full rounded border hugging the key edge, transparent
                       centre. Sits BEHIND the Stream Deck title text so the
                       text reads inside a coloured frame -> "this key is the
                       selected member of its radio group".

  notch-<colour>.svg   Four L-shaped corner brackets (the "corner notches"),
                       leaving the whole centre free. Subtler than a full
                       frame.

  bevel-left-<colour>.svg / bevel-right-<colour>.svg
                       A single bevelled corner (a "dog-ear" chamfer) in ONE
                       top corner + a dark liseré on the diagonal — the exact
                       trick the funk instrument icons used to flag a key
                       (blue liseré = one group, yellow = another). Left and
                       right variants so two groups can share one panel.

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

BEVEL_LEG = 66        # length of each leg of the corner triangle
BEVEL_LISERE_W = 7    # dark liseré along the diagonal (funk trick)


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


def bevel_svg(hexc: str, side: str) -> str:
    """A single bevelled top corner (dog-ear) + dark liseré on the diagonal.

    The funk instrument icons flagged a key exactly this way: one chamfered
    corner in the group's colour with a darker liseré so it reads on black keys
    AND on lit tiles. `side` is "left" (top-left corner) or "right" (top-right).
    """
    b = BEVEL_LEG
    if side == "left":
        tri = f"M0 0 L{b} 0 L0 {b} Z"          # top-left corner triangle
        dia = f"M{b} 0 L0 {b}"                   # its diagonal (the liseré)
    else:
        tri = f"M144 0 L{144 - b} 0 L144 {b} Z"  # top-right corner triangle
        dia = f"M{144 - b} 0 L144 {b}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 144 144">
  <!-- coloured bevelled corner -->
  <path d="{tri}" fill="{hexc}"/>
  <!-- dark liseré on the diagonal so the bevel reads on any background -->
  <path d="{dia}" fill="none" stroke="#000000" stroke-opacity="0.45"
        stroke-width="{BEVEL_LISERE_W}" stroke-linecap="round"/>
</svg>
'''


def main():
    SRC.mkdir(exist_ok=True)
    tags = {}
    for slug, disp, hexc in COLOURS:
        (SRC / f"frame-{slug}.svg").write_text(frame_svg(hexc))
        (SRC / f"notch-{slug}.svg").write_text(notch_svg(hexc))
        (SRC / f"bevel-left-{slug}.svg").write_text(bevel_svg(hexc, "left"))
        (SRC / f"bevel-right-{slug}.svg").write_text(bevel_svg(hexc, "right"))
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
        tags[f"bevel-left-{slug}"] = {
            "name": f"{disp} · Selected Corner Bevel (Left)",
            "tags": ["radio button", "selected", "corner bevel", "corner",
                     "chamfer", "highlight", slug],
        }
        tags[f"bevel-right-{slug}"] = {
            "name": f"{disp} · Selected Corner Bevel (Right)",
            "tags": ["radio button", "selected", "corner bevel", "corner",
                     "chamfer", "highlight", slug],
        }
    (ROOT / "tags.json").write_text(json.dumps(tags, indent=4, ensure_ascii=False) + "\n")
    print(f"wrote {len(COLOURS) * 4} SVGs + tags.json ({len(COLOURS)} colours x 4 families)")


if __name__ == "__main__":
    main()
