#!/usr/bin/env python3
"""Render THE WORLD front page, 24 November 2026 (1024x1024 PNG).
Fresh code written from the builder brief spec. All art is flat PIL vector
drawing (no external images, no network). Stories come from stories.json.
Layout (v3 discipline: no decks on grid panels, big headlines):
  masthead 0-100 | hero 104-336 | grid 4x3 344-780 | bottom band 788-996 | footer 1000-1022
"""
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 30, 36)
NAVY = (27, 58, 92)
TEAL = (14, 107, 107)
GOLD = (176, 124, 22)
CARD = (255, 255, 255)
RULE = (120, 110, 95)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
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


def text_block(d, x, y, text, fnt, fill, max_w, lh=None, align="left"):
    lh = lh or int(fnt.size * 1.18)
    lines = wrap(d, text, fnt, max_w)
    for i, ln in enumerate(lines):
        if align == "center":
            w = d.textlength(ln, font=fnt)
            d.text((x + (max_w - w) / 2, y + i * lh), ln, font=fnt, fill=fill)
        else:
            d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh


def chip(d, x, y, label, bg, fg=(255, 255, 255)):
    f = font(SANS_B, 13)
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 19], radius=9, fill=bg)
    d.text((x + 7, y + 3), label, font=f, fill=fg)
    return w


# ---------------- flat illustrations: one subject per panel ----------------
def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 74))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(38, 34, 30))
    # damaged apartment block
    bx, bw, bt = x + w * 0.14, w * 0.52, y + h * 0.16
    d.rectangle([bx, bt, bx + bw, y + h * 0.86], fill=(24, 24, 28))
    d.polygon([(bx + bw * 0.55, bt), (bx + bw, bt), (bx + bw, bt + h * 0.16),
               (bx + bw * 0.72, bt + h * 0.10)], fill=(52, 58, 74))
    for r in range(3):
        for c in range(4):
            wx, wy = bx + 8 + c * (bw - 16) / 4, bt + 12 + r * (h * 0.2)
            d.rectangle([wx, wy, wx + 12, wy + 9], fill=(232, 190, 90))
    # rubble + rescuer (yellow helmet, orange vest)
    d.polygon([(bx + bw - 6, y + h * 0.86), (bx + bw + w * 0.22, y + h * 0.86),
               (bx + bw + w * 0.10, y + h * 0.62)], fill=(90, 82, 72))
    hx = x + w * 0.80
    d.ellipse([hx - 2, y + h * 0.50, hx + 18, y + h * 0.50 + 16], fill=(250, 220, 90))
    d.rectangle([hx, y + h * 0.50 + 16, hx + 16, y + h * 0.86], fill=(220, 90, 30))
    d.rectangle([hx + 3, y + h * 0.50 + 22, hx + 13, y + h * 0.50 + 30], fill=(255, 255, 255))


def ill_jets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 110, 168))
    d.ellipse([x + w * 0.68, y + 6, x + w * 0.86, y + 24], fill=(250, 220, 120))
    d.ellipse([x + w * 0.06, y + h * 0.55, x + w * 0.30, y + h * 0.68], fill=(235, 240, 245))
    d.ellipse([x + w * 0.55, y + h * 0.68, x + w * 0.80, y + h * 0.80], fill=(235, 240, 245))

    def jet(jx, jy, s, col):
        d.polygon([(jx, jy), (jx + 46 * s, jy + 6 * s), (jx, jy + 12 * s)], fill=col)
        d.polygon([(jx + 30 * s, jy + 2 * s), (jx + 40 * s, jy - 8 * s),
                   (jx + 44 * s, jy + 3 * s)], fill=col)
        d.polygon([(jx + 30 * s, jy + 10 * s), (jx + 40 * s, jy + 20 * s),
                   (jx + 44 * s, jy + 9 * s)], fill=col)
    jet(x + w * 0.12, y + h * 0.18, 0.9, (30, 34, 40))
    jet(x + w * 0.52, y + h * 0.42, 0.7, (20, 24, 30))


def ill_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(122, 28, 30))
    d.ellipse([x + w * 0.18, y + h * 0.70, x + w * 0.82, y + h * 0.86], fill=(90, 60, 30))
    # handle (diagonal) + head (horizontal bar)
    d.line([x + w * 0.34, y + h * 0.66, x + w * 0.68, y + h * 0.26],
           fill=(190, 145, 85), width=10)
    d.rectangle([x + w * 0.22, y + h * 0.16, x + w * 0.78, y + h * 0.36], fill=(150, 105, 55))
    d.rectangle([x + w * 0.22, y + h * 0.16, x + w * 0.78, y + h * 0.23], fill=(175, 130, 70))


def ill_ucl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 110, 60))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(12, 84, 46))
    # trophy
    cx = x + w * 0.72
    d.polygon([(cx - 16, y + h * 0.16), (cx + 16, y + h * 0.16), (cx + 10, y + h * 0.48),
               (cx - 10, y + h * 0.48)], fill=(232, 190, 90))
    d.ellipse([cx - 22, y + h * 0.12, cx - 8, y + h * 0.30], outline=(232, 190, 90), width=4)
    d.ellipse([cx + 8, y + h * 0.12, cx + 22, y + h * 0.30], outline=(232, 190, 90), width=4)
    d.rectangle([cx - 4, y + h * 0.48, cx + 4, y + h * 0.66], fill=(232, 190, 90))
    d.rectangle([cx - 14, y + h * 0.66, cx + 14, y + h * 0.74], fill=(232, 190, 90))
    # ball
    bx, by, r = x + w * 0.22, y + h * 0.48, 22
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(255, 255, 255))
    d.polygon([(bx, by - 9), (bx + 8, by - 3), (bx + 5, by + 7), (bx - 5, by + 7),
               (bx - 8, by - 3)], fill=(20, 20, 20))


def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 164, 120))
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(120, 88, 58))
    pts = [(x + w * 0.45, y), (x + w * 0.52, y + h * 0.25), (x + w * 0.42, y + h * 0.45),
           (x + w * 0.55, y + h * 0.66), (x + w * 0.48, y + h)]
    d.line(pts, fill=(40, 26, 16), width=5)
    d.polygon([(x + w * 0.10, y + h * 0.30), (x + w * 0.34, y + h * 0.30),
               (x + w * 0.34, y + h * 0.66), (x + w * 0.10, y + h * 0.66)], fill=(90, 70, 50))
    d.polygon([(x + w * 0.08, y + h * 0.30), (x + w * 0.22, y + h * 0.18),
               (x + w * 0.36, y + h * 0.30)], fill=(70, 54, 38))
    # seismograph trace
    tr = [(x + w * 0.60, y + h * 0.40), (x + w * 0.66, y + h * 0.40),
          (x + w * 0.69, y + h * 0.18), (x + w * 0.72, y + h * 0.62),
          (x + w * 0.75, y + h * 0.28), (x + w * 0.80, y + h * 0.40),
          (x + w * 0.92, y + h * 0.40)]
    d.line(tr, fill=(176, 30, 36), width=3)


def ill_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 107, 107))
    d.ellipse([x + w * 0.70, y + 8, x + w * 0.88, y + 26], fill=(250, 220, 120))
    px, py = x + w * 0.16, y + h * 0.45
    d.ellipse([px, py - 10, px + 110, py + 10], fill=(240, 240, 235))
    d.polygon([(px + 100, py - 8), (px + 128, py), (px + 100, py + 8)], fill=(240, 240, 235))
    d.polygon([(px + 45, py - 8), (px + 62, py - 26), (px + 74, py - 8)], fill=(200, 60, 40))
    d.polygon([(px + 45, py + 8), (px + 62, py + 24), (px + 74, py + 8)], fill=(200, 60, 40))
    for i in range(4):
        d.ellipse([px + 22 + i * 16, py - 3, px + 28 + i * 16, py + 3], fill=(27, 58, 92))


def ill_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(27, 58, 92))
    cx, cy, s = x + w * 0.5, y + h * 0.52, 30
    for i in range(5):
        d.line([cx - s - 14, cy - s + 8 + i * 10, cx - s, cy - s + 8 + i * 10],
               fill=(120, 180, 200), width=3)
        d.line([cx + s, cy - s + 8 + i * 10, cx + s + 14, cy - s + 8 + i * 10],
               fill=(120, 180, 200), width=3)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(20, 20, 20))
    d.rectangle([cx - s + 8, cy - s + 8, cx + s - 8, cy + s - 8],
                outline=(232, 190, 90), width=3)
    d.text((cx - 8, cy - 12), "AI", font=font(SANS_B, 20), fill=(232, 190, 90))


def ill_office(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 96, 110))
    d.rectangle([x + w * 0.18, y + h * 0.24, x + w * 0.82, y + h * 0.86], fill=(210, 205, 190))
    d.rectangle([x + w * 0.18, y + h * 0.24, x + w * 0.82, y + h * 0.36], fill=(70, 76, 90))
    for c in range(3):
        wx = x + w * (0.26 + c * 0.24)
        d.rectangle([wx, y + h * 0.44, wx + w * 0.14, y + h * 0.64], fill=(60, 90, 130))
    d.rectangle([x + w * 0.46, y + h * 0.44, x + w * 0.54, y + h * 0.86], fill=(40, 40, 44))
    d.line([x + w * 0.50, y + h * 0.06, x + w * 0.50, y + h * 0.24], fill=(240, 240, 235), width=3)
    d.polygon([(x + w * 0.50, y + h * 0.06), (x + w * 0.66, y + h * 0.12),
               (x + w * 0.50, y + h * 0.18)], fill=(200, 60, 40))


def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 200, 168))
    d.polygon([(x + w * 0.14, y + h * 0.30), (x + w * 0.50, y + h * 0.10),
               (x + w * 0.86, y + h * 0.30)], fill=(90, 70, 50))
    for c in range(4):
        cx = x + w * (0.22 + c * 0.19)
        d.rectangle([cx, y + h * 0.32, cx + 10, y + h * 0.82], fill=(250, 245, 235))
    d.rectangle([x + w * 0.44, y + h * 0.52, x + w * 0.56, y + h * 0.82], fill=(60, 50, 40))
    d.rectangle([x + w * 0.14, y + h * 0.82, x + w * 0.86, y + h * 0.90], fill=(90, 70, 50))


def ill_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 120, 70))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(200, 90, 40))
    d.line([x, y + h * 0.70, x + w, y + h * 0.70], fill=(255, 255, 255), width=3)
    # racket
    d.ellipse([x + w * 0.58, y + h * 0.10, x + w * 0.92, y + h * 0.52],
              outline=(240, 240, 235), width=6)
    d.line([x + w * 0.68, y + h * 0.46, x + w * 0.52, y + h * 0.86],
           fill=(150, 105, 55), width=6)
    # ball
    bx, by, r = x + w * 0.26, y + h * 0.40, 24
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(200, 220, 60))
    d.arc([bx - r, by - r, bx + r, by + r], 300, 60, fill=(255, 255, 255), width=3)
    d.arc([bx - r, by - r, bx + r, by + r], 120, 240, fill=(255, 255, 255), width=3)


def ill_basket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 90, 30))
    d.rectangle([x + w * 0.62, y + h * 0.14, x + w * 0.94, y + h * 0.62],
                fill=(240, 240, 235))
    d.ellipse([x + w * 0.68, y + h * 0.34, x + w * 0.88, y + h * 0.48],
              outline=(200, 60, 40), width=4)
    d.line([x + w * 0.70, y + h * 0.48, x + w * 0.68, y + h * 0.66],
           fill=(255, 255, 255), width=2)
    d.line([x + w * 0.86, y + h * 0.48, x + w * 0.88, y + h * 0.66],
           fill=(255, 255, 255), width=2)
    bx, by, r = x + w * 0.28, y + h * 0.50, 26
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(230, 120, 40))
    d.line([bx - r, by, bx + r, by], fill=(20, 20, 20), width=3)
    d.line([bx, by - r, bx, by + r], fill=(20, 20, 20), width=3)
    d.arc([bx - r, by - r, bx + r, by + r], 300, 60, fill=(20, 20, 20), width=3)


def ill_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 90, 50))
    d.line([x + w * 0.78, y + h * 0.10, x + w * 0.78, y + h * 0.62],
           fill=(250, 220, 120), width=5)
    d.line([x + w * 0.68, y + h * 0.10, x + w * 0.88, y + h * 0.10],
           fill=(250, 220, 120), width=5)
    cx, cy = x + w * 0.34, y + h * 0.52
    d.ellipse([cx - 52, cy - 22, cx + 52, cy + 22], fill=(120, 72, 32))
    d.line([cx - 18, cy, cx + 18, cy], fill=(255, 255, 255), width=3)
    for i in range(-2, 3):
        d.line([cx + i * 8, cy - 5, cx + i * 8, cy + 5], fill=(255, 255, 255), width=2)


def ill_haiti(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    d.rectangle([x + w * 0.12, y + h * 0.18, x + w * 0.88, y + h * 0.44], fill=(30, 60, 140))
    d.rectangle([x + w * 0.12, y + h * 0.44, x + w * 0.88, y + h * 0.70], fill=(200, 40, 50))
    d.ellipse([x + w * 0.44, y + h * 0.30, x + w * 0.56, y + h * 0.58], fill=(255, 255, 255))
    for i, hx in enumerate((0.24, 0.50, 0.76)):
        cx = x + w * hx
        d.ellipse([cx - 12, y + h * 0.76, cx + 12, y + h * 0.76 + 12], fill=(60, 90, 60))
        d.rectangle([cx - 12, y + h * 0.76 + 10, cx + 12, y + h * 0.76 + 14], fill=(40, 60, 40))


ILL = {1: ill_kyiv, 2: ill_jets, 3: ill_gavel, 4: ill_ucl, 5: ill_quake, 6: ill_plane,
       7: ill_chip, 8: ill_office, 9: ill_court, 10: ill_tennis, 11: ill_basket,
       12: ill_football, 13: ill_haiti}

# pin positions on the schematic map (fractions of map box)
PINS = {1: (0.52, 0.28), 2: (0.90, 0.28), 3: (0.78, 0.42), 4: (0.72, 0.46),
        5: (0.79, 0.58), 6: (0.87, 0.66), 7: (0.92, 0.40), 8: (0.20, 0.58),
        9: (0.24, 0.50), 10: (0.50, 0.33), 11: (0.12, 0.36), 12: (0.18, 0.44),
        13: (0.27, 0.55)}


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
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=font(SANS_B, 12))
        d.text((cx - tw / 2, cy - 7), t, font=font(SANS_B, 12), fill=(255, 255, 255))


def main():
    with open("stories.json", encoding="utf-8") as f:
        data = json.load(f)
    panels = data["panels"]
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
    tag = "16 STORIES  ·  EUROPE  ·  ASIA  ·  AMERICAS  ·  EVERY ONE FROM TUESDAY"
    d.text((512 - d.textlength(tag, font=font(SANS_B, 14)) / 2, 118),
           tag, font=font(SANS_B, 14), fill=NAVY)
    d.line([16, 140, 1008, 140], fill=INK, width=2)

    # ---- hero (panel 1) ----
    hx, hy, hw, hh = 16, 148, 992, 188
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=RULE, width=1)
    ILL[1](d, hx + 1, hy + 1, 400, hh - 2)
    tx = hx + 418
    w1 = chip(d, tx, hy + 12, "1 · EUROPE · WAR", RED)
    chip(d, tx + w1 + 8, hy + 12, "CONFIRMED", NAVY)
    text_block(d, tx, hy + 40, "Kyiv death toll reaches 12",
               font(SANS_B, 34), INK, hw - 436, lh=38)
    text_block(d, tx, hy + 118,
               "Monday strikes hit Dymer, north of Kyiv. Rescuers still search the rubble.",
               font(SANS, 18), (60, 60, 60), hw - 436, lh=23)
    d.text((tx, hy + 164), "Sources: officials via AP / Reuters",
           font=font(SANS, 14), fill=(110, 100, 85))

    # ---- grid: panels 2..13 (4 cols x 3 rows) ----
    gx0, gy0, cw, ch, gap = 16, 344, 242, 136, 8
    for idx, p in enumerate(panels[1:]):
        col, row = idx % 4, idx // 4
        x = gx0 + col * (cw + gap)
        y = gy0 + row * (ch + gap)
        n = p["n"]
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=RULE, width=1)
        ILL[n](d, x + 1, y + 1, cw - 2, 62)
        lab = f"{n} · {p['label']}"
        d.text((x + 8, y + 68), lab, font=font(SANS_B, 13), fill=tuple(p["color"]))
        text_block(d, x + 8, y + 86, p["headline"], font(SANS_B, 21), INK,
                   cw - 16, lh=24)

    # ---- bottom band ----
    by = 780
    d.line([16, by, 1008, by], fill=INK, width=2)
    # briefs (left)
    bx = 16
    d.text((bx, by + 8), "ALSO ON TUESDAY", font=font(SANS_B, 16), fill=INK)
    briefs = data["briefs"]
    yy = by + 32
    for b in briefs:
        d.text((bx, yy), "▪", font=font(SANS_B, 16), fill=RED)
        yy = text_block(d, bx + 18, yy, b, font(SANS, 16), INK, 292, lh=20) + 8
    # map (centre)
    mx = 334
    d.text((mx, by + 8), "WHERE IT HAPPENED", font=font(SANS_B, 16), fill=INK)
    draw_map(d, mx, by + 32, 340, 148)
    # timeline + date check (right)
    tx = 690
    d.text((tx, by + 8), "THE DAY IN UTC", font=font(SANS_B, 16), fill=INK)
    tl = [("01:04", "Korean jets enter zone"),
          ("02:16", "Pakistan quake, M4.1"),
          ("02:37", "China death sentence"),
          ("17:45", "UCL Matchday 5 kicks off")]
    yy = by + 32
    for t, e in tl:
        d.text((tx, yy), t, font=font(SANS_B, 15), fill=RED)
        d.text((tx + 62, yy), e, font=font(SANS, 15), fill=INK)
        yy += 19
    yy += 4
    d.rectangle([tx, yy, 1008, 996], outline=RED, width=2)
    d.text((tx + 8, yy + 5), "DATE CHECK — ALL EVENTS 24 NOV 2026",
           font=font(SANS_B, 13), fill=RED)
    dc = ("Left out (23 Nov or earlier): Huang, O'Hare, Oxfam Gaza, FIFA, Fury, "
          "Treasury, grain, TRIPP, LUCAS, schools, Lahore, Ohio, ICJ, COP31. "
          "Not yet: UCL, NBA, CFP.")
    text_block(d, tx + 8, yy + 26, dc, font(SANS, 14), INK, 302, lh=18)

    # ---- footer ----
    d.line([16, 1004, 1008, 1004], fill=INK, width=1)
    foot = ("Sources: AFP · AP / Reuters · NCS / USGS · Gold Wall Press · EssentiallySports. "
            "Times UTC. CLAIM = one side's account.")
    d.text((512 - d.textlength(foot, font=font(SANS, 14)) / 2, 1008),
           foot, font=font(SANS, 14), fill=(110, 100, 85))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
