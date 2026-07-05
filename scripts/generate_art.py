"""
Generates low-poly triangle-mesh SVG placeholder art for the portfolio
gallery, using the Veanir brand palette. Run once with `python
scripts/generate_art.py`. Replace the resulting files in
assets/images/work/ with real render screenshots whenever they're ready --
just keep the same filenames (work-01.jpg ... work-06.jpg) or update the
paths in index.html.
"""
import random
import math

PALETTE = {
    "night": "#042442",
    "deep": "#06385D",
    "ocean": "#005075",
    "cyan": "#0AC0C9",
    "electric": "#7DFFF7",
}

W, H = 900, 700

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)

def lerp(a, b, t):
    return a + (b - a) * t

def mix(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((lerp(r1, r2, t), lerp(g1, g2, t), lerp(b1, b2, t)))

def gen_mesh(seed, stops, cols=11, rows=8, jitter=0.42, glow_bias=0.0):
    rnd = random.Random(seed)
    pts = []
    for r in range(rows + 1):
        row = []
        for c in range(cols + 1):
            x = c / cols * W
            y = r / rows * H
            jx = (rnd.random() - 0.5) * (W / cols) * jitter
            jy = (rnd.random() - 0.5) * (H / rows) * jitter
            row.append((x + jx, y + jy))
        pts.append(row)

    tris = []
    for r in range(rows):
        for c in range(cols):
            p00 = pts[r][c]
            p10 = pts[r][c + 1]
            p01 = pts[r + 1][c]
            p11 = pts[r + 1][c + 1]
            if rnd.random() > 0.5:
                tris.append((p00, p10, p01))
                tris.append((p10, p11, p01))
            else:
                tris.append((p00, p10, p11))
                tris.append((p00, p11, p01))

    svg_tris = []
    for tri in tris:
        cx = sum(p[0] for p in tri) / 3
        cy = sum(p[1] for p in tri) / 3
        # diagonal gradient position 0..1
        t = (cx / W) * 0.5 + (cy / H) * 0.5
        t = max(0.0, min(1.0, t + (rnd.random() - 0.5) * 0.12 + glow_bias))
        # pick between multiple stops
        seg = t * (len(stops) - 1)
        i = min(int(seg), len(stops) - 2)
        local_t = seg - i
        color = mix(stops[i], stops[i + 1], local_t)
        opacity = round(0.55 + rnd.random() * 0.45, 2)
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in tri)
        svg_tris.append(f'<polygon points="{pts_str}" fill="{color}" fill-opacity="{opacity}"/>')

    return "\n".join(svg_tris)

def build_svg(seed, stops, glow_bias=0.0):
    body = gen_mesh(seed, stops, glow_bias=glow_bias)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="bg{seed}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PALETTE['night']}"/>
      <stop offset="1" stop-color="{PALETTE['deep']}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg{seed})"/>
  <g>
{body}
  </g>
</svg>'''

pieces = [
    # seed, stop sequence (dark -> light), glow_bias
    (11, [PALETTE["night"], PALETTE["deep"], PALETTE["ocean"], PALETTE["cyan"]], 0.0),
    (22, [PALETTE["deep"], PALETTE["ocean"], PALETTE["cyan"], PALETTE["electric"]], 0.05),
    (33, [PALETTE["night"], PALETTE["ocean"], PALETTE["cyan"]], -0.05),
    (44, [PALETTE["night"], PALETTE["deep"], PALETTE["cyan"], PALETTE["electric"]], 0.1),
    (55, [PALETTE["deep"], PALETTE["ocean"], PALETTE["ocean"], PALETTE["cyan"]], -0.03),
    (66, [PALETTE["night"], PALETTE["ocean"], PALETTE["electric"]], 0.02),
]

import os
out_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "work")
os.makedirs(out_dir, exist_ok=True)

for idx, (seed, stops, glow) in enumerate(pieces, start=1):
    svg = build_svg(seed, stops, glow)
    path = os.path.join(out_dir, f"work-{idx:02d}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", path)

# Portrait placeholder for the About section: soft radial bust silhouette
portrait = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 700">
  <defs>
    <linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{PALETTE['deep']}"/>
      <stop offset="1" stop-color="{PALETTE['night']}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.38" r="0.55">
      <stop offset="0" stop-color="{PALETTE['cyan']}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{PALETTE['cyan']}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="600" height="700" fill="url(#pbg)"/>
  <rect width="600" height="700" fill="url(#glow)"/>
  <g stroke="{PALETTE['cyan']}" stroke-opacity="0.5" stroke-width="1.4" fill="none">
    <circle cx="300" cy="290" r="120"/>
    <path d="M120 640 C120 480 480 480 480 640" />
    <path d="M180 290 a120 120 0 0 1 240 0" stroke-dasharray="6 10"/>
  </g>
  <g fill="{PALETTE['electric']}" fill-opacity="0.9">
    <circle cx="300" cy="290" r="3"/>
    <circle cx="220" cy="240" r="2"/>
    <circle cx="380" cy="250" r="2"/>
    <circle cx="300" cy="180" r="2"/>
  </g>
  <text x="300" y="292" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-size="54" fill="{PALETTE['electric']}" fill-opacity="0.85">V</text>
</svg>'''
with open(os.path.join(out_dir, "..", "misc", "portrait.svg"), "w", encoding="utf-8") as f:
    f.write(portrait)
print("wrote portrait")

# Favicon: faceted diamond mark
favicon = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="{PALETTE['night']}"/>
  <polygon points="32,8 52,26 32,58 12,26" fill="{PALETTE['ocean']}"/>
  <polygon points="32,8 52,26 32,34" fill="{PALETTE['cyan']}"/>
  <polygon points="32,8 12,26 32,34" fill="{PALETTE['deep']}"/>
  <polygon points="12,26 32,34 32,58" fill="{PALETTE['deep']}" fill-opacity="0.9"/>
  <polygon points="52,26 32,34 32,58" fill="{PALETTE['electric']}" fill-opacity="0.85"/>
</svg>'''
with open(os.path.join(out_dir, "..", "misc", "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(favicon)
print("wrote favicon")
