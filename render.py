#!/usr/bin/env python3
"""Render THE WORLD front page, 24 November 2026 (1024x1024 PNG).
Fresh code written in the r2 fix session from the r2 brief.
All art is flat PIL vector drawing (no external images, no network).
Stories come from stories.json.
Layout: masthead 0-144 | hero 148-344 | grid 5x2 352-716 |
bottom band 724-990 | footer 996-1022.
Date convention (printed in DATE CHECK + footer): dates are the local
date where each event happened (any time zone, per the rules);
times shown local + UTC.
"""
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 30, 36)
NAVY = (27, 58, 92)
GOLD = (176, 124, 22)
CARD = (255, 255, 255)
RULE = (120, 110, 95)
GREY = (110, 100, 85)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, lh=None):
    lh = lh or int(fnt.size * 1.18)
    lines = wrap(d, text, fnt, max_w)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def chip(d, x, y, label, bg, fg=(255, 255, 255)):
    f = font(SANS_B, 13)
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 19], radius=9, fill=bg)
    d.text((x + 7, y + 3), label, font=f, fill=fg)
    return w


# ---------------- illustrations (flat, one subject each) ----------------
def ill_hero_jets(d, x, y, w, h):
    """Hero art, sized for the wide hero slot: jets over the East Sea,
    Ulleung Island below, warning beacon. No airspace violation."""
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(64, 116, 172))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(38, 96, 130))
    d.ellipse([x + w * 0.80, y + 8, x + w * 0.92, y + 8 + 34], fill=(250, 222, 120))
    for cx, cy, cw in ((0.10, 0.18, 90), (0.55, 0.10, 70), (0.30, 0.38, 80)):
        d.ellipse([x + w * cx, y + h * cy, x + w * cx + cw, y + h * cy + 16],
                  fill=(235, 240, 245))
    # Ulleung Island: green hill + lighthouse on the sea
    ix = x + w * 0.42
    d.polygon([(ix - 90, y + h), (ix - 30, y + h * 0.66), (ix + 40, y + h * 0.62),
               (ix + 110, y + h)], fill=(34, 110, 60))
    d.rectangle([ix - 4, y + h * 0.50, ix + 6, y + h * 0.66], fill=(240, 240, 235))
    d.rectangle([ix - 8, y + h * 0.46, ix + 10, y + h * 0.50], fill=(200, 60, 40))
    d.ellipse([ix - 3, y + h * 0.40, ix + 9, y + h * 0.40 + 8], fill=(250, 220, 90))
    # warning rays above the island
    for k in range(3):
        d.line([ix + 2, y + h * 0.38, ix - 34 + k * 34, y + h * 0.22],
               fill=(250, 220, 90), width=3)

    def jet(jx, jy, s, col):
        # side-profile fighter: long fuselage, pointed nose, swept wings,
        # tail fin, and a short contrail
        d.line([jx - 34 * s, jy + 8 * s, jx, jy + 8 * s], fill=(255, 255, 255),
               width=2)
        d.polygon([(jx, jy), (jx + 62 * s, jy + 8 * s), (jx, jy + 16 * s)],
                  fill=col)
        d.polygon([(jx + 34 * s, jy + 3 * s), (jx + 46 * s, jy - 12 * s),
                   (jx + 52 * s, jy + 4 * s)], fill=col)
        d.polygon([(jx + 34 * s, jy + 13 * s), (jx + 46 * s, jy + 28 * s),
                   (jx + 52 * s, jy + 12 * s)], fill=col)
        d.polygon([(jx + 4 * s, jy + 2 * s), (jx + 12 * s, jy - 10 * s),
                   (jx + 18 * s, jy + 2 * s)], fill=col)
    jet(x + w * 0.06, y + h * 0.12, 1.0, (28, 32, 38))
    jet(x + w * 0.32, y + h * 0.30, 0.8, (20, 24, 30))
    jet(x + w * 0.68, y + h * 0.40, 0.9, (90, 96, 104))  # scrambling F-15K
    d.text((x + 10, y + h - 22), "ULLEUNG ISLAND", font=font(SANS_B, 13),
           fill=(255, 255, 255))


def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 164, 120))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(120, 88, 58))
    pts = [(x + w * 0.45, y), (x + w * 0.53, y + h * 0.25),
           (x + w * 0.42, y + h * 0.45), (x + w * 0.56, y + h * 0.68),
           (x + w * 0.48, y + h)]
    d.line(pts, fill=(40, 26, 16), width=5)
    d.polygon([(x + w * 0.08, y + h * 0.32), (x + w * 0.32, y + h * 0.32),
               (x + w * 0.32, y + h * 0.68), (x + w * 0.08, y + h * 0.68)],
              fill=(90, 70, 50))
    d.polygon([(x + w * 0.06, y + h * 0.32), (x + w * 0.20, y + h * 0.18),
               (x + w * 0.34, y + h * 0.32)], fill=(70, 54, 38))
    tr = [(x + w * 0.58, y + h * 0.42), (x + w * 0.64, y + h * 0.42),
          (x + w * 0.67, y + h * 0.16), (x + w * 0.70, y + h * 0.64),
          (x + w * 0.73, y + h * 0.30), (x + w * 0.78, y + h * 0.42),
          (x + w * 0.92, y + h * 0.42)]
    d.line(tr, fill=(176, 30, 36), width=3)


def ill_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 107, 107))
    d.ellipse([x + w * 0.72, y + 8, x + w * 0.88, y + 24], fill=(250, 220, 120))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(28, 84, 110))
    # ferry / naval ship
    d.polygon([(x + w * 0.10, y + h * 0.60), (x + w * 0.88, y + h * 0.60),
               (x + w * 0.78, y + h * 0.78), (x + w * 0.20, y + h * 0.78)],
              fill=(240, 240, 235))
    d.rectangle([x + w * 0.30, y + h * 0.40, x + w * 0.62, y + h * 0.60],
                fill=(200, 60, 40))
    for i in range(3):
        d.rectangle([x + w * (0.34 + i * 0.10), y + h * 0.46,
                     x + w * (0.40 + i * 0.10), y + h * 0.54],
                    fill=(255, 255, 255))
    d.line([x + w * 0.46, y + h * 0.40, x + w * 0.46, y + h * 0.24],
           fill=(240, 240, 235), width=3)
    d.polygon([(x + w * 0.46, y + h * 0.24), (x + w * 0.62, y + h * 0.30),
               (x + w * 0.46, y + h * 0.34)], fill=(200, 60, 40))


def ill_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 58, 92))
    cx, cy, s = x + w * 0.5, y + h * 0.52, 26
    for i in range(4):
        yy = cy - s + 8 + i * 12
        d.line([cx - s - 12, yy, cx - s, yy], fill=(120, 180, 200), width=3)
        d.line([cx + s, yy, cx + s + 12, yy], fill=(120, 180, 200), width=3)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(20, 20, 20))
    d.rectangle([cx - s + 7, cy - s + 7, cx + s - 7, cy + s - 7],
                outline=(232, 190, 90), width=3)
    d.text((cx - 8, cy - 11), "AI", font=font(SANS_B, 18), fill=(232, 190, 90))


def ill_office(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 96, 110))
    d.rectangle([x + w * 0.20, y + h * 0.26, x + w * 0.80, y + h * 0.86],
                fill=(210, 205, 190))
    d.rectangle([x + w * 0.20, y + h * 0.26, x + w * 0.80, y + h * 0.38],
                fill=(70, 76, 90))
    for c in range(3):
        wx = x + w * (0.27 + c * 0.22)
        d.rectangle([wx, y + h * 0.46, wx + w * 0.12, y + h * 0.64],
                    fill=(60, 90, 130))
    d.rectangle([x + w * 0.46, y + h * 0.46, x + w * 0.54, y + h * 0.86],
                fill=(40, 40, 44))
    d.line([x + w * 0.50, y + h * 0.08, x + w * 0.50, y + h * 0.26],
           fill=(240, 240, 235), width=3)
    d.polygon([(x + w * 0.50, y + h * 0.08), (x + w * 0.64, y + h * 0.13),
               (x + w * 0.50, y + h * 0.18)], fill=(200, 60, 40))


def ill_islands(d, x, y, w, h):
    """Solomon Islands: Pacific islets in a blue sea, plus a torn pact
    document with a red seal in the foreground."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 96, 130))
    d.polygon([(x + w * 0.06, y + h * 0.66), (x + w * 0.16, y + h * 0.48),
               (x + w * 0.30, y + h * 0.52), (x + w * 0.40, y + h * 0.66),
               (x + w * 0.38, y + h * 0.84), (x + w * 0.10, y + h * 0.84)],
              fill=(34, 110, 60))
    d.polygon([(x + w * 0.58, y + h * 0.56), (x + w * 0.68, y + h * 0.40),
               (x + w * 0.82, y + h * 0.44), (x + w * 0.92, y + h * 0.60),
               (x + w * 0.88, y + h * 0.84), (x + w * 0.62, y + h * 0.84)],
              fill=(46, 130, 70))
    # palm on the left islet
    d.line([x + w * 0.22, y + h * 0.50, x + w * 0.22, y + h * 0.34],
           fill=(90, 70, 50), width=3)
    for dx, dy in ((-16, -4), (14, -6), (-10, -12), (10, -12)):
        d.line([x + w * 0.22, y + h * 0.34,
                x + w * 0.22 + dx, y + h * 0.34 + dy], fill=(46, 130, 70),
               width=3)
    # pact document, bottom centre
    d.polygon([(x + w * 0.36, y + h * 0.62), (x + w * 0.66, y + h * 0.62),
               (x + w * 0.66, y + h * 0.94), (x + w * 0.51, y + h * 0.86),
               (x + w * 0.36, y + h * 0.94)], fill=(245, 240, 225))
    d.line([x + w * 0.41, y + h * 0.70, x + w * 0.61, y + h * 0.70],
           fill=(60, 60, 60), width=2)
    d.line([x + w * 0.41, y + h * 0.76, x + w * 0.61, y + h * 0.76],
           fill=(60, 60, 60), width=2)
    d.ellipse([x + w * 0.47, y + h * 0.80, x + w * 0.55, y + h * 0.80 + 8],
              fill=(176, 30, 36))


def ill_chart(d, x, y, w, h):
    """Kospi: rising market chart, green arrow, candlesticks."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 66))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(18, 34, 52))
    bars = [0.30, 0.22, 0.38, 0.30, 0.52, 0.44, 0.66]
    for i, bh in enumerate(bars):
        bx = x + w * (0.08 + i * 0.13)
        d.rectangle([bx, y + h * (0.72 - bh), bx + 12, y + h * 0.72],
                    fill=(46, 160, 90) if i >= 4 else (120, 150, 170))
    pts = [(x + w * 0.08, y + h * 0.55), (x + w * 0.28, y + h * 0.44),
           (x + w * 0.48, y + h * 0.48), (x + w * 0.68, y + h * 0.30),
           (x + w * 0.90, y + h * 0.16)]
    d.line(pts, fill=(250, 220, 90), width=4)
    d.polygon([(x + w * 0.90, y + h * 0.16), (x + w * 0.82, y + h * 0.14),
               (x + w * 0.88, y + h * 0.26)], fill=(250, 220, 90))
    d.text((x + 8, y + 6), "+7%", font=font(SANS_B, 20), fill=(250, 220, 90))


def ill_ucl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 110, 60))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(12, 84, 46))
    cx = x + w * 0.70
    d.polygon([(cx - 14, y + h * 0.16), (cx + 14, y + h * 0.16),
               (cx + 9, y + h * 0.46), (cx - 9, y + h * 0.46)], fill=(232, 190, 90))
    d.ellipse([cx - 20, y + h * 0.12, cx - 7, y + h * 0.28],
              outline=(232, 190, 90), width=3)
    d.ellipse([cx + 7, y + h * 0.12, cx + 20, y + h * 0.28],
              outline=(232, 190, 90), width=3)
    d.rectangle([cx - 3, y + h * 0.46, cx + 3, y + h * 0.64], fill=(232, 190, 90))
    d.rectangle([cx - 12, y + h * 0.64, cx + 12, y + h * 0.72], fill=(232, 190, 90))
    bx, by, r = x + w * 0.22, y + h * 0.48, 20
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(255, 255, 255))
    d.polygon([(bx, by - 8), (bx + 7, by - 2), (bx + 4, by + 6),
               (bx - 4, by + 6), (bx - 7, by - 2)], fill=(20, 20, 20))


def ill_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 120, 70))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(200, 90, 40))
    d.line([x, y + h * 0.70, x + w, y + h * 0.70], fill=(255, 255, 255), width=3)
    d.ellipse([x + w * 0.56, y + h * 0.10, x + w * 0.92, y + h * 0.52],
              outline=(240, 240, 235), width=5)
    d.line([x + w * 0.66, y + h * 0.46, x + w * 0.50, y + h * 0.86],
           fill=(150, 105, 55), width=5)
    bx, by, r = x + w * 0.26, y + h * 0.40, 22
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(200, 220, 60))
    d.arc([bx - r, by - r, bx + r, by + r], 300, 60, fill=(255, 255, 255), width=3)
    d.arc([bx - r, by - r, bx + r, by + r], 120, 240, fill=(255, 255, 255), width=3)


def ill_basket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 90, 30))
    d.rectangle([x + w * 0.62, y + h * 0.14, x + w * 0.94, y + h * 0.60],
                fill=(240, 240, 235))
    d.ellipse([x + w * 0.68, y + h * 0.32, x + w * 0.88, y + h * 0.46],
              outline=(200, 60, 40), width=4)
    d.line([x + w * 0.70, y + h * 0.46, x + w * 0.68, y + h * 0.64],
           fill=(255, 255, 255), width=2)
    d.line([x + w * 0.86, y + h * 0.46, x + w * 0.88, y + h * 0.64],
           fill=(255, 255, 255), width=2)
    bx, by, r = x + w * 0.28, y + h * 0.50, 24
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(230, 120, 40))
    d.line([bx - r, by, bx + r, by], fill=(20, 20, 20), width=3)
    d.line([bx, by - r, bx, by + r], fill=(20, 20, 20), width=3)


def ill_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 90, 50))
    d.line([x + w * 0.78, y + h * 0.10, x + w * 0.78, y + h * 0.62],
           fill=(250, 220, 120), width=5)
    d.line([x + w * 0.68, y + h * 0.10, x + w * 0.88, y + h * 0.10],
           fill=(250, 220, 120), width=5)
    cx, cy = x + w * 0.34, y + h * 0.52
    d.ellipse([cx - 48, cy - 20, cx + 48, cy + 20], fill=(120, 72, 32))
    d.line([cx - 16, cy, cx + 16, cy], fill=(255, 255, 255), width=3)
    for i in range(-2, 3):
        d.line([cx + i * 8, cy - 5, cx + i * 8, cy + 5], fill=(255, 255, 255), width=2)


ILL = {1: ill_hero_jets, 2: ill_quake, 3: ill_ship, 4: ill_chip, 5: ill_office,
       6: ill_islands, 7: ill_chart, 8: ill_ucl, 9: ill_tennis, 10: ill_basket,
       11: ill_football}

# short display labels (grid cards are narrow; keep <= ~20 chars at 14px)
LABELS = {1: "ASIA · SECURITY", 2: "ASIA · DISASTER", 3: "ASIA · MIGRATION",
          4: "ASIA · TECH", 5: "ASIA · DIPLOMACY", 6: "PACIFIC · PACT",
          7: "ASIA · MARKETS", 8: "EUROPE · FOOTBALL", 9: "ITALY · TENNIS",
          10: "US · BASKETBALL", 11: "US · CFB"}

# pin positions on the schematic map (fractions of map box), 1:1 with panels
PINS = {1: (0.90, 0.26), 2: (0.78, 0.44), 3: (0.85, 0.62), 4: (0.88, 0.68),
        5: (0.93, 0.19), 6: (0.97, 0.74), 7: (0.94, 0.32), 8: (0.50, 0.26),
        9: (0.53, 0.33), 10: (0.13, 0.36), 11: (0.19, 0.43)}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    land = (168, 190, 150)
    d.polygon([(x + w * 0.05, y + h * 0.12), (x + w * 0.28, y + h * 0.08),
               (x + w * 0.33, y + h * 0.22), (x + w * 0.28, y + h * 0.40),
               (x + w * 0.18, y + h * 0.42), (x + w * 0.10, y + h * 0.36),
               (x + w * 0.04, y + h * 0.24)], fill=land)
    d.polygon([(x + w * 0.22, y + h * 0.48), (x + w * 0.31, y + h * 0.46),
               (x + w * 0.34, y + h * 0.62), (x + w * 0.28, y + h * 0.88),
               (x + w * 0.23, y + h * 0.72), (x + w * 0.20, y + h * 0.58)], fill=land)
    d.polygon([(x + w * 0.44, y + h * 0.10), (x + w * 0.55, y + h * 0.07),
               (x + w * 0.58, y + h * 0.22), (x + w * 0.52, y + h * 0.32),
               (x + w * 0.45, y + h * 0.28), (x + w * 0.43, y + h * 0.18)], fill=land)
    d.polygon([(x + w * 0.46, y + h * 0.38), (x + w * 0.58, y + h * 0.34),
               (x + w * 0.62, y + h * 0.52), (x + w * 0.58, y + h * 0.74),
               (x + w * 0.50, y + h * 0.72), (x + w * 0.45, y + h * 0.54)], fill=land)
    d.polygon([(x + w * 0.59, y + h * 0.08), (x + w * 0.88, y + h * 0.05),
               (x + w * 0.97, y + h * 0.24), (x + w * 0.91, y + h * 0.50),
               (x + w * 0.77, y + h * 0.52), (x + w * 0.68, y + h * 0.38),
               (x + w * 0.60, y + h * 0.24)], fill=land)
    d.polygon([(x + w * 0.82, y + h * 0.70), (x + w * 0.94, y + h * 0.68),
               (x + w * 0.95, y + h * 0.84), (x + w * 0.85, y + h * 0.88)], fill=land)
    for n, (fx, fy) in PINS.items():
        cx, cy = x + w * fx, y + h * fy
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=font(SANS_B, 11))
        d.text((cx - tw / 2, cy - 7), t, font=font(SANS_B, 11),
               fill=(255, 255, 255))


def main():
    with open("stories.json", encoding="utf-8") as f:
        data = json.load(f)
    panels = data["panels"]
    hero = panels[0]
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.line([16, 10, 1008, 10], fill=INK, width=4)
    d.text((512 - d.textlength("THE WORLD", font=font(SERIF_B, 62)) / 2, 16),
           "THE WORLD", font=font(SERIF_B, 62), fill=INK)
    sub = "TUESDAY  ·  24 NOVEMBER 2026"
    d.text((512 - d.textlength(sub, font=font(SERIF_B, 26)) / 2, 82),
           sub, font=font(SERIF_B, 26), fill=RED)
    d.line([16, 112, 1008, 112], fill=INK, width=2)
    n_stories = len(panels) + len(data["briefs"])
    tag = ("%d STORIES  ·  ASIA  ·  EUROPE  ·  PACIFIC  ·  AMERICAS  ·  "
           "EVERY ONE FROM TUESDAY" % n_stories)
    d.text((512 - d.textlength(tag, font=font(SANS_B, 14)) / 2, 118),
           tag, font=font(SANS_B, 14), fill=NAVY)
    d.line([16, 140, 1008, 140], fill=INK, width=2)

    # ---- hero (panel 1: Korea jets) ----
    hx, hy, hw, hh = 16, 148, 992, 196
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=RULE, width=1)
    ILL[1](d, hx + 1, hy + 1, 400, hh - 2)
    tx = hx + 418
    w1 = chip(d, tx, hy + 12, "1 · ASIA · SECURITY", RED)
    chip(d, tx + w1 + 8, hy + 12, "CONFIRMED", NAVY)
    text_block(d, tx, hy + 38, hero["headline"], font(SANS_B, 32), INK,
               hw - 436, lh=36)
    text_block(d, tx, hy + 122, hero["deck"], font(SANS, 17), (60, 60, 60),
               hw - 436, lh=21)
    d.text((tx, hy + 172), "Source: South Korea Joint Chiefs of Staff (JCS)",
           font=font(SANS, 13), fill=GREY)

    # ---- grid: panels 2..11 (5 cols x 2 rows) ----
    gx0, gy0, cw, ch, gap = 16, 352, 192, 178, 8
    for idx, p in enumerate(panels[1:]):
        col, row = idx % 5, idx // 5
        x = gx0 + col * (cw + gap)
        y = gy0 + row * (ch + gap)
        n = p["n"]
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=RULE, width=1)
        ILL[n](d, x + 1, y + 1, cw - 2, 76)
        lab = "%d · %s" % (n, LABELS[n])
        d.text((x + 8, y + 82), lab, font=font(SANS_B, 14), fill=tuple(p["color"]))
        text_block(d, x + 8, y + 102, p["headline"], font(SANS_B, 22), INK,
                   cw - 16, lh=25)

    # ---- bottom band ----
    by = 724
    d.line([16, by, 1008, by], fill=INK, width=2)
    # briefs (left)
    bx = 16
    d.text((bx, by + 8), "ALSO ON TUESDAY", font=font(SANS_B, 16), fill=INK)
    yy = by + 32
    for b in data["briefs"]:
        d.text((bx, yy), "▪", font=font(SANS_B, 16), fill=RED)
        yy = text_block(d, bx + 18, yy, b, font(SANS, 16), INK, 282, lh=20) + 10
    # map (centre)
    mx = 332
    d.text((mx, by + 8), "WHERE IT HAPPENED", font=font(SANS_B, 16), fill=INK)
    draw_map(d, mx, by + 32, 320, 170)
    # timeline + date check (right)
    tx = 668
    d.text((tx, by + 8), "THE DAY — LOCAL TIME", font=font(SANS_B, 16), fill=INK)
    yy = by + 32
    for t, e in data["timeline"]:
        line = "%s — %s" % (t, e)
        d.text((tx, yy), line, font=font(SANS, 13), fill=INK)
        yy += 17
    yy += 4
    d.rectangle([tx, yy, 1008, 990], outline=RED, width=2)
    d.text((tx + 8, yy + 5), "DATE CHECK — ALL EVENTS 24 NOV 2026",
           font=font(SANS_B, 12), fill=RED)
    dc = ("Dates are the local date where each event happened (any time zone, "
          "per the rules); times local + UTC. Left out (Mon 23 Nov or "
          "earlier): Kyiv toll 12; China Ma; Colombia court; Bukele names; "
          "India Power Index; India–NZ draw; Libya probe; EU sanctions; "
          "Denmark ghetto; DRC cobalt. "
          "Not yet: UCL 18:45 CET, NBA 19:00 ET, CFP 19:30 ET.")
    text_block(d, tx + 8, yy + 24, dc, font(SANS, 12), INK, 324, lh=15)

    # ---- footer ----
    d.line([16, 996, 1008, 996], fill=INK, width=1)
    foot1 = ("Sources: AFP · JCS · KCNA · NCS / USGS · PMO Singapore · "
             "Parliament of Malaysia · UEFA · NBA · CFP · SMH / Reuters")
    foot2 = ("Dates are the local date where each event happened (any time zone, "
             "per the rules); times shown local + UTC.")
    d.text((512 - d.textlength(foot1, font=font(SANS, 11)) / 2, 999),
           foot1, font=font(SANS, 11), fill=GREY)
    d.text((512 - d.textlength(foot2, font=font(SANS, 11)) / 2, 1011),
           foot2, font=font(SANS, 11), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
