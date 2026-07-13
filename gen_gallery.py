#!/usr/bin/env python3
"""Render docs/gallery.svg + docs/gallery.png — the whole pack at a glance.

19 colours across, one family per row (Frame · Corner Notch · Corner Bevel L ·
Corner Bevel R). Reuses the COLOURS list from gen_frames so the gallery can
never drift from the actual pack. Run `python3 gen_gallery.py` after changing
colours or geometry.
"""
from pathlib import Path
from gen_frames import COLOURS

ROOT = Path(__file__).parent
S = 66              # mini-key size
PITCH = 76          # column pitch
LABEL_W = 150       # left label column
X0 = 20 + LABEL_W   # first key x
TOP = 84
ROW_H = 100
BG = "#0d0f14"
KEY = "#181b22"


def frame(x, y, h):
    k = S / 144
    i, s, r = 11 * k, S - 22 * k, 26 * k
    return (
        f'<rect x="{x+i:.1f}" y="{y+i:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{r:.1f}" '
        f'fill="none" stroke="#000" stroke-opacity="0.38" stroke-width="{17*k:.1f}"/>'
        f'<rect x="{x+i:.1f}" y="{y+i:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{r:.1f}" '
        f'fill="none" stroke="{h}" stroke-width="{11*k:.1f}"/>'
    )


def notch(x, y, h):
    k = S / 144
    n, a = 16 * k, 42 * k
    f = S - n
    paths = [
        f"M{x+n:.1f} {y+n+a:.1f} L{x+n:.1f} {y+n:.1f} L{x+n+a:.1f} {y+n:.1f}",
        f"M{x+f-a:.1f} {y+n:.1f} L{x+f:.1f} {y+n:.1f} L{x+f:.1f} {y+n+a:.1f}",
        f"M{x+f:.1f} {y+f-a:.1f} L{x+f:.1f} {y+f:.1f} L{x+f-a:.1f} {y+f:.1f}",
        f"M{x+n+a:.1f} {y+f:.1f} L{x+n:.1f} {y+f:.1f} L{x+n:.1f} {y+f-a:.1f}",
    ]
    return "".join(
        f'<path d="{d}" fill="none" stroke="{h}" stroke-width="{13*k:.1f}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>' for d in paths
    )


def bevel(x, y, h, side, clip_id):
    k = S / 144
    b = 66 * k
    if side == "left":
        tri = f"M{x:.1f} {y:.1f} L{x+b:.1f} {y:.1f} L{x:.1f} {y+b:.1f} Z"
        dia = f"M{x+b:.1f} {y:.1f} L{x:.1f} {y+b:.1f}"
    else:
        tri = f"M{x+S:.1f} {y:.1f} L{x+S-b:.1f} {y:.1f} L{x+S:.1f} {y+b:.1f} Z"
        dia = f"M{x+S-b:.1f} {y:.1f} L{x+S:.1f} {y+b:.1f}"
    r = S * 0.2
    return (
        f'<clipPath id="{clip_id}"><rect x="{x:.1f}" y="{y:.1f}" width="{S}" height="{S}" rx="{r:.1f}"/></clipPath>'
        f'<g clip-path="url(#{clip_id})"><path d="{tri}" fill="{h}"/>'
        f'<path d="{dia}" fill="none" stroke="#000" stroke-opacity="0.45" stroke-width="{7*k:.1f}" stroke-linecap="round"/></g>'
    )


ROWS = [
    ("Frame", lambda x, y, h, i: frame(x, y, h)),
    ("Corner Notch", lambda x, y, h, i: notch(x, y, h)),
    ("Corner Bevel ◤", lambda x, y, h, i: bevel(x, y, h, "left", f"cl{i}")),
    ("Corner Bevel ◥", lambda x, y, h, i: bevel(x, y, h, "right", f"cr{i}")),
]

W = X0 + len(COLOURS) * PITCH + 4
H = TOP + len(ROWS) * ROW_H + 16
r_key = S * 0.2

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
    f'font-family="-apple-system, Segoe UI, Roboto, sans-serif">',
    f'<rect x="0" y="0" width="{W}" height="{H}" rx="20" fill="{BG}"/>',
    f'<text x="{X0}" y="46" fill="#F8FAFC" font-size="26" font-weight="700">'
    f'Radio Button Selection Frames — 76 icons</text>',
    f'<text x="{X0}" y="70" fill="#64748B" font-size="16">'
    f'19 colours × 4 styles · transparent centre for the key title</text>',
]

for ri, (label, draw) in enumerate(ROWS):
    ry = TOP + ri * ROW_H
    cy = ry + (ROW_H - S) / 2
    parts.append(
        f'<text x="{20}" y="{cy + S/2 + 6:.1f}" fill="#CBD5E1" font-size="16" font-weight="600">{label}</text>'
    )
    for ci, (slug, disp, hexc) in enumerate(COLOURS):
        cx = X0 + ci * PITCH
        parts.append(
            f'<rect x="{cx}" y="{cy:.1f}" width="{S}" height="{S}" rx="{r_key:.1f}" fill="{KEY}"/>'
        )
        parts.append(draw(cx, cy, hexc, f"{ri}_{ci}"))

parts.append("</svg>")
docs = ROOT / "docs"
docs.mkdir(exist_ok=True)
(docs / "gallery.svg").write_text("\n".join(parts) + "\n")
print(f"wrote docs/gallery.svg ({W}x{H}, {len(COLOURS)*len(ROWS)} icons)")
