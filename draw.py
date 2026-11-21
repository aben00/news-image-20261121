#!/usr/bin/env python3
"""Draw "The World Today" -- a one-page newspaper front page summing up
Saturday 21 November 2026, as a 1024x1024 PNG. Round 2.

Layout: masthead + red date band, three illustrated lead stories, a pinned
world map with a numbered pin key, nine illustrated minis (three rows), and
a brief index of twenty more stories -- 32 verified stories of the day,
12 illustrations, 12 map pins.

Deterministic: fixed random seed, no clock, no network, no file reads
beyond the system fonts. Run: python3 draw.py <output.png>

Every story happened, or was first reported, on Saturday 21 November
2026. Stories first reported on 20 November or earlier were checked and
left out: the Russian missiles in Poland, the UK-EU summit deal, the
Denmark rapper plot, the Rajasthan panchayat results, the Gupta
sentencing, the Trump data-centre press conference, the Kryvyi Rih
strike, the Bayer Roundup ruling, the Palisades arson verdict, the
FBI/USDA hacks, the Gen Z protests, the Tbilisi blast, the Han Duck-soo
ruling, the daraxonrasib trial results, the Nigeria boat capsize, the
Afghanistan mortar blast, the deep-sea mining leases, the Jurf
al-Sakhar entry and the Kenya drilling start. Each story kept below has
a genuine 21 November event stated on the page -- including the NATO
chief's visit to Warsaw, the COP31 talks resuming, the Manipur toll
update, the MQ-9 claim, the Jurf al-Sakhar headquarters opening and
the NWSL final, all dated Saturday 21 November.

The Peru quake is given as magnitude 6.7, the figure of the USGS and
Peru's Geophysical Institute (early reports said 6.8).
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SEED = 20261121
MARGIN = 16

PAPER = (247, 243, 232)
INK = (24, 24, 24)
RED = (178, 28, 28)
BLUE = (28, 56, 96)
GREY = (92, 88, 78)
FAINT = (120, 116, 104)
SEA = (183, 210, 224)
LAND = (203, 192, 154)
LAND_EDGE = (146, 136, 106)
GOLD = (198, 142, 32)

_FONT_CACHE = {}


def font(path, size):
    """Load a TTF once; fall back to Pillow's default bitmap font."""
    key = (path, size)
    if key not in _FONT_CACHE:
        if os.path.exists(path):
            _FONT_CACHE[key] = ImageFont.truetype(path, size)
        else:
            _FONT_CACHE[key] = ImageFont.load_default(size)
    return _FONT_CACHE[key]


def serif_bold(size):
    return font("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", size)


def serif_italic(size):
    return font("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", size)


def sans(size):
    return font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def sans_bold(size):
    return font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def wrap_lines(draw, text, fnt, max_w):
    """Greedy word wrap; returns the lines that fit inside max_w."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_text(draw, x, y, text, fnt, max_w, leading, fill=INK, limit=None):
    """Draw wrapped text starting at (x, y); return y below the last line."""
    lines = wrap_lines(draw, text, fnt, max_w)
    if limit is not None:
        lines = lines[:limit]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def disc(draw, cx, cy, num, radius=10):
    """Numbered red disc: story number, map pin, key marker."""
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 fill=RED, outline=(255, 255, 255), width=2)
    fnt = sans_bold(12 if radius <= 10 else 14)
    tw = draw.textlength(str(num), font=fnt)
    top = fnt.getbbox("9")[3]
    draw.text((cx - tw / 2, cy - top / 2 - 1), str(num), font=fnt,
              fill=(255, 255, 255))


def five_star(draw, cx, cy, outer, inner, fill):
    pts = []
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / 5 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ------------------------------------------------------------- lead art

def art_quake(draw, x, y, w, h, rng):
    """Junin, Peru: night sky, moon, shaking houses, crack, seismograph."""
    draw.rectangle([x, y, x + w, y + h], fill=(30, 34, 52))
    for _ in range(28):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.45))
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(215, 215, 195))
    draw.ellipse([x + w - 48, y + 8, x + w - 20, y + 36],
                 fill=(236, 230, 198))
    ground = y + h - 30
    bx = x + 12
    while bx < x + w - 42:
        bw = rng.randint(34, 52)
        bh = rng.randint(28, 50)
        tilt = rng.randint(-3, 3)
        draw.rectangle([bx, ground - bh + tilt, bx + bw, ground],
                       fill=(12, 16, 30))
        for _ in range(bh // 12):
            wx = bx + rng.randint(5, max(6, bw - 8))
            wy = ground - bh + rng.randint(6, max(7, bh - 8))
            if rng.random() < 0.5:
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 105))
        bx += bw + rng.randint(6, 12)
    pts = [(x, ground)]
    cx = x
    while cx < x + w:
        cx += rng.randint(14, 26)
        pts.append((min(cx, x + w), ground + rng.randint(-8, 10)))
    draw.line(pts, fill=(255, 120, 60), width=3)
    tx, ty = x + 12, y + h - 62
    prev = (tx, ty)
    for i in range(1, 60):
        nx = tx + i * (w - 24) / 60
        amp = 2 if i < 18 else (26 if 24 < i < 44 else 5)
        ny = ty + rng.randint(-amp, amp)
        draw.line([prev, (nx, ny)], fill=(120, 220, 130), width=2)
        prev = (nx, ny)


def art_ashes(draw, x, y, w, h, rng):
    """Perth: green outfield, pitch, stumps, bat, red ball, scores."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 110, 58))
    draw.rectangle([x, y + h - 44, x + w, y + h], fill=(38, 88, 44))
    draw.rectangle([x + w // 2 - 34, y + 8, x + w // 2 + 34, y + h - 44],
                   fill=(196, 172, 118))
    # one set of stumps at the top of the pitch
    for k in range(3):
        sx = x + w // 2 - 12 + k * 12
        draw.rectangle([sx, y + 12, sx + 4, y + 32], fill=(232, 196, 90))
    # red ball, lower left of the pitch, clear of the "172"
    cx, cy = x + w // 2 - 70, y + 62
    draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(178, 30, 30))
    draw.arc([cx - 11, cy - 11, cx + 11, cy + 11], 200, 340,
             fill=(255, 255, 255), width=2)
    # bat leaning at upper right, kept inside the tile
    draw.line([(x + w // 2 + 60, y + 22), (x + w // 2 + 88, y + 58)],
              fill=(214, 178, 120), width=9)
    draw.line([(x + w // 2 + 88, y + 58), (x + w // 2 + 96, y + 66)],
              fill=(190, 150, 96), width=11)
    draw.text((x + 14, y + h - 38), "172", font=serif_bold(30),
              fill=(255, 255, 255))
    draw.text((x + w - 104, y + h - 38), "7/58", font=serif_bold(30),
              fill=(255, 214, 110))


def art_rahul(draw, x, y, w, h, rng):
    """Wellington: blue sky, sun, crowd, batsman raising his bat, 100."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 74, 128))
    draw.rectangle([x, y + h - 24, x + w, y + h], fill=(46, 96, 52))
    draw.ellipse([x + w - 56, y + 10, x + w - 26, y + 40],
                 fill=(255, 214, 110))
    for _ in range(38):
        sx = x + rng.randint(4, w - 4)
        sy = y + h - rng.randint(28, 44)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                     fill=rng.choice([(255, 255, 255), (255, 214, 110),
                                      (200, 220, 255)]))
    cx = x + w // 2 - 20
    draw.ellipse([cx - 12, y + 34, cx + 12, y + 58], fill=(232, 188, 150))
    draw.rectangle([cx - 13, y + 58, cx + 13, y + 90], fill=(20, 40, 90))
    draw.rectangle([cx - 11, y + 90, cx - 2, y + h - 4], fill=(24, 24, 24))
    draw.rectangle([cx + 2, y + 90, cx + 11, y + h - 4], fill=(24, 24, 24))
    draw.line([(cx + 11, y + 66), (cx + 48, y + 28)], fill=(214, 178, 120),
              width=8)
    draw.line([(cx + 48, y + 28), (cx + 60, y + 10)], fill=(190, 150, 96),
              width=11)
    bx, by = x + w - 58, y + 50
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(200, 40, 40))
    draw.text((x + 14, y + h - 40), "100", font=serif_bold(30),
              fill=(255, 255, 255))
    draw.text((x + w - 128, y + h - 34), "SENA SET", font=sans_bold(15),
              fill=(255, 214, 110))


# ------------------------------------------------------------- mini art

def art_f1(draw, x, y, w, h, rng):
    """Las Vegas: night street circuit, race car, chequered flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 20, 34))
    draw.rectangle([x, y + h - 34, x + w, y + h - 20], fill=(52, 52, 58))
    for i in range(0, w, 26):
        draw.rectangle([x + i, y + h - 29, x + i + 14, y + h - 25],
                       fill=(240, 220, 90))
    for _ in range(18):
        lx = x + rng.randint(4, w - 8)
        ly = y + rng.randint(4, 26)
        draw.rectangle([lx, ly, lx + 3, ly + 8],
                       fill=rng.choice([(255, 90, 160), (90, 200, 255),
                                        (255, 214, 110)]))
    cy = y + h - 44
    draw.polygon([(x + 18, cy), (x + 34, cy - 16), (x + 62, cy - 18),
                  (x + 78, cy - 6), (x + 96, cy)], fill=(200, 30, 30))
    draw.rectangle([x + 40, cy - 26, x + 62, cy - 16], fill=(30, 30, 40))
    draw.ellipse([x + 26, cy - 6, x + 42, cy + 10], fill=(12, 12, 12))
    draw.ellipse([x + 72, cy - 6, x + 88, cy + 10], fill=(12, 12, 12))
    draw.ellipse([x + 31, cy - 1, x + 37, cy + 5], fill=(180, 180, 180))
    draw.ellipse([x + 77, cy - 1, x + 83, cy + 5], fill=(180, 180, 180))
    fx = x + w - 26
    for r in range(3):
        for c in range(3):
            col = (20, 20, 20) if (r + c) % 2 == 0 else (255, 255, 255)
            draw.rectangle([fx + c * 6, y + 8 + r * 6,
                            fx + c * 6 + 6, y + 14 + r * 6], fill=col)
    draw.line([(fx, y + 8), (fx, y + 44)], fill=(200, 200, 200), width=2)


def art_atp(draw, x, y, w, h, rng):
    """Turin: indoor hard court, net, tennis ball, racket."""
    draw.rectangle([x, y, x + w, y + h], fill=(44, 84, 148))
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 60, 110))
    draw.rectangle([x + 10, y + 12, x + w - 10, y + h - 34],
                   outline=(255, 255, 255), width=2)
    draw.line([(x + w // 2, y + 12), (x + w // 2, y + h - 34)],
              fill=(255, 255, 255), width=2)
    draw.rectangle([x + 8, y + h // 2 - 4, x + w - 8, y + h // 2 + 4],
                   fill=(240, 240, 240))
    bx, by = x + w - 30, y + 26
    draw.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(200, 230, 60))
    draw.arc([bx - 13, by - 13, bx + 13, by + 13], 40, 140,
             fill=(255, 255, 255), width=2)
    draw.arc([bx - 13, by - 13, bx + 13, by + 13], 220, 320,
             fill=(255, 255, 255), width=2)
    draw.ellipse([x + 16, y + h - 52, x + 44, y + h - 24],
                 outline=(220, 220, 220), width=4)
    draw.line([(x + 30, y + h - 26), (x + 44, y + h - 8)],
              fill=(220, 220, 220), width=4)


def art_fpi(draw, x, y, w, h, rng):
    """Mumbai: rising market bars, trend arrow, rupee sign."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 64, 48))
    bars = [18, 26, 22, 36, 44, 58]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx0 = x + 16 + i * bw
        col = (90, 200, 130) if i < 5 else (255, 214, 110)
        draw.rectangle([bx0, y + h - 18 - bh, bx0 + bw - 6, y + h - 18],
                       fill=col)
    pts = [(x + 16, y + h - 40), (x + 40, y + h - 56), (x + 62, y + h - 48),
           (x + 86, y + h - 72), (x + w - 12, y + h - 84)]
    draw.line(pts, fill=(255, 255, 255), width=3)
    draw.polygon([(x + w - 12, y + h - 84), (x + w - 24, y + h - 82),
                  (x + w - 14, y + h - 72)], fill=(255, 255, 255))
    draw.text((x + 10, y + 6), "\u20b9", font=serif_bold(26),
              fill=(255, 255, 255))


def art_rutte(draw, x, y, w, h, rng):
    """Warsaw: EU flag and Polish flag side by side."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    draw.rectangle([x + 8, y + 14, x + 58, y + h - 14], fill=(0, 51, 153))
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        sx = x + 33 + 15 * math.cos(a)
        sy = y + h // 2 + 15 * math.sin(a)
        five_star(draw, sx, sy, 3, 1.4, (255, 204, 0))
    draw.rectangle([x + 66, y + 14, x + w - 8, y + (h - 14) // 2 + 7],
                   fill=(255, 255, 255))
    draw.rectangle([x + 66, y + (h - 14) // 2 + 7, x + w - 8, y + h - 14],
                   fill=(220, 20, 60))
    draw.rectangle([x + 66, y + 14, x + w - 8, y + h - 14],
                   outline=(120, 120, 120), width=1)


def art_mine(draw, x, y, w, h, rng):
    """New South Wales: terraced open-cut mine and a haul truck."""
    draw.rectangle([x, y, x + w, y + h], fill=(122, 84, 52))
    for i, ty in enumerate([y + 12, y + 34, y + 56]):
        draw.rectangle([x + i * 8, ty, x + w, ty + 18],
                       fill=(96 + i * 14, 64 + i * 10, 40))
    draw.rectangle([x, y + 78, x + w, y + h], fill=(52, 40, 30))
    tx, ty = x + 18, y + h - 30
    draw.rectangle([tx, ty - 14, tx + 34, ty], fill=(240, 190, 40))
    draw.rectangle([tx + 34, ty - 10, tx + 46, ty], fill=(220, 170, 30))
    draw.ellipse([tx + 4, ty - 2, tx + 14, ty + 8], fill=(16, 16, 16))
    draw.ellipse([tx + 22, ty - 2, tx + 32, ty + 8], fill=(16, 16, 16))
    draw.ellipse([tx + 38, ty - 2, tx + 46, ty + 6], fill=(16, 16, 16))
    for _ in range(8):
        lx = x + rng.randint(w // 2, w - 10)
        ly = y + h - rng.randint(6, 16)
        draw.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=(20, 20, 20))


def art_wreck(draw, x, y, w, h, rng):
    """Queensland coast: half-sunk warship, waves, bubbles."""
    draw.rectangle([x, y, x + w, y + h], fill=(28, 78, 110))
    draw.ellipse([x + w - 44, y + 8, x + w - 16, y + 36],
                 fill=(255, 220, 120))
    draw.polygon([(x + 12, y + h - 52), (x + 74, y + h - 52),
                  (x + 62, y + h - 34), (x + 22, y + h - 34)],
                 fill=(90, 90, 96))
    draw.rectangle([x + 30, y + h - 68, x + 44, y + h - 52],
                   fill=(70, 70, 76))
    draw.line([(x + 37, y + h - 68), (x + 37, y + h - 82)],
              fill=(60, 60, 66), width=3)
    for wy in (y + h - 30, y + h - 16):
        prev = None
        for i in range(25):
            px = x + i * (w / 24)
            py = wy + 3 * math.sin(i * 0.9)
            if prev is not None:
                draw.line([prev, (px, py)], fill=(200, 225, 240), width=2)
            prev = (px, py)
    for _ in range(10):
        bx = x + rng.randint(60, w - 10)
        by = y + rng.randint(10, h - 60)
        r = rng.randint(1, 3)
        draw.ellipse([bx - r, by - r, bx + r, by + r],
                     outline=(220, 235, 245), width=1)


def art_basra(draw, x, y, w, h, rng):
    """Basra: dusk sky, power-plant towers, flames, fire truck, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 28, 22))
    draw.ellipse([x + 8, y + 8, x + 34, y + 34], fill=(255, 190, 90))
    # cooling towers and chimney silhouettes
    draw.polygon([(x + 14, y + h - 18), (x + 22, y + 34), (x + 38, y + 34),
                  (x + 46, y + h - 18)], fill=(24, 20, 20))
    draw.polygon([(x + 52, y + h - 18), (x + 58, y + 44), (x + 72, y + 44),
                  (x + 78, y + h - 18)], fill=(30, 24, 24))
    draw.rectangle([x + 82, y + 26, x + 88, y + h - 18], fill=(24, 20, 20))
    # flames licking up between the towers
    for fx, fh, col in [(x + 26, 34, (255, 120, 30)),
                        (x + 40, 46, (255, 170, 40)),
                        (x + 60, 38, (255, 120, 30)),
                        (x + 84, 30, (255, 170, 40))]:
        draw.polygon([(fx - 8, y + h - 18), (fx, y + h - 18 - fh),
                      (fx + 8, y + h - 18)], fill=col)
    # smoke puffs
    for _ in range(9):
        sx = x + rng.randint(10, w - 14)
        sy = y + rng.randint(6, 34)
        r = rng.randint(4, 8)
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 110, 105))
    # fire truck
    ty = y + h - 22
    draw.rectangle([x + 10, ty - 10, x + 40, ty], fill=(200, 30, 30))
    draw.rectangle([x + 40, ty - 7, x + 50, ty], fill=(220, 60, 40))
    draw.ellipse([x + 14, ty - 2, x + 24, ty + 8], fill=(16, 16, 16))
    draw.ellipse([x + 32, ty - 2, x + 42, ty + 8], fill=(16, 16, 16))
    draw.line([(x + 44, ty - 8), (x + 62, ty - 26)], fill=(200, 200, 200),
              width=2)


def art_riyadh(draw, x, y, w, h, rng):
    """Riyadh: night skyline, tallest tower, missile trails, intercepts."""
    draw.rectangle([x, y, x + w, y + h], fill=(14, 18, 40))
    for _ in range(22):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.4))
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 235))
    base = y + h - 20
    # skyline blocks
    bx = x + 6
    while bx < x + w - 16:
        bw = rng.randint(12, 20)
        bh = rng.randint(22, 46)
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(28, 34, 58))
        for _ in range(bh // 10):
            wx = bx + rng.randint(3, max(4, bw - 5))
            wy = base - bh + rng.randint(4, max(5, bh - 5))
            if rng.random() < 0.6:
                draw.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 210, 105))
        bx += bw + 3
    # the tallest tower, lit
    tx0 = x + w // 2 - 8
    draw.rectangle([tx0, y + 26, tx0 + 16, base], fill=(52, 66, 104))
    draw.rectangle([tx0 + 3, y + 18, tx0 + 13, y + 26], fill=(90, 110, 160))
    for wy in range(y + 30, base - 6, 10):
        draw.rectangle([tx0 + 2, wy, tx0 + 5, wy + 4], fill=(255, 214, 110))
        draw.rectangle([tx0 + 11, wy, tx0 + 14, wy + 4], fill=(255, 214, 110))
    # missile trails arcing down, met by intercept bursts
    for sx0, sy0, ex0, ey0 in [(x + 10, y + 12, x + 34, y + 44),
                               (x + w - 12, y + 8, x + w - 38, y + 40)]:
        draw.line([(sx0, sy0), (ex0, ey0)], fill=(255, 150, 60), width=2)
        five_star(draw, ex0, ey0, 9, 4, (255, 220, 120))
        five_star(draw, ex0, ey0, 4, 2, (255, 255, 255))


def art_bepi(draw, x, y, w, h, rng):
    """Mercury: black space, cratered planet, probe with solar panels."""
    draw.rectangle([x, y, x + w, y + h], fill=(8, 8, 14))
    for _ in range(30):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(225, 225, 240))
    # sun glare, top right
    draw.ellipse([x + w - 34, y + 4, x + w - 6, y + 32], fill=(255, 230, 150))
    # Mercury: big cratered disc, lower left
    cx, cy, cr = x + 34, y + h - 34, 30
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(168, 152, 132))
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                 outline=(120, 106, 90), width=2)
    for ox, oy, orr in [(-12, -8, 7), (8, 4, 5), (-4, 12, 6), (14, -12, 4),
                        (-16, 8, 4)]:
        draw.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr,
                      cy + oy + orr], outline=(120, 106, 90), width=1)
    # the probe: gold body, two blue solar wings, dish
    px, py = x + w - 46, y + h - 52
    draw.rectangle([px - 14, py - 5, px - 2, py + 5], fill=(40, 90, 160))
    draw.rectangle([px + 2, py - 5, px + 14, py + 5], fill=(40, 90, 160))
    draw.rectangle([px - 5, py - 7, px + 5, py + 7], fill=(210, 170, 60))
    draw.line([(px, py - 7), (px + 8, py - 16)], fill=(220, 220, 220), width=2)
    draw.ellipse([px + 5, py - 19, px + 11, py - 13], outline=(220, 220, 220),
                 width=1)
    draw.line([(px - 2, py + 10), (px - 8, py + 22)], fill=(255, 170, 60),
              width=2)


# ------------------------------------------------------------------- map

# Simplified continent outlines (lon, lat), equirectangular view.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-70, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-168, 66)],
    # South America
    [(-79, 9), (-62, 11), (-52, 5), (-50, -5), (-35, -8), (-40, -22),
     (-48, -28), (-58, -38), (-65, -47), (-70, -54), (-73, -40),
     (-72, -20), (-80, -5), (-79, 9)],
    # Africa
    [(-17, 15), (-10, 31), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
     (51, 11), (40, -5), (40, -18), (32, -29), (19, -35), (12, -18),
     (9, -1), (-8, 4), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 60),
     (40, 50), (35, 45), (28, 41), (23, 36), (19, 40), (12, 44), (3, 42),
     (-10, 36)],
    # Asia
    [(40, 68), (60, 69), (80, 73), (110, 74), (140, 72), (160, 70),
     (178, 66), (162, 60), (158, 52), (142, 45), (135, 35), (127, 33),
     (120, 28), (108, 20), (105, 10), (100, 8), (97, 16), (90, 22),
     (80, 13), (75, 8), (70, 20), (60, 25), (52, 27), (48, 30), (43, 36),
     (40, 42), (40, 68)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (137, -15), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (132, -32), (125, -33),
     (115, -35), (114, -22)],
    # New Zealand
    [(166, -46), (168, -44), (172, -41), (174, -39), (176, -38), (178, -37),
     (176, -40), (173, -42), (169, -46), (166, -46)],
]


def project(lon, lat, mx, my, mw, mh):
    """Equirectangular projection into the map box."""
    px = mx + (lon + 180.0) / 360.0 * mw
    py = my + (75.0 - lat) / 130.0 * mh
    return px, py


def paint_map(draw, x, y, w, h, pins):
    """Sea, graticule, continents, numbered pins (offset where crowded)."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        draw.line([(gx, y), (gx, y + h)], fill=(255, 255, 255), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y + (75 - lat) / 130 * h
        draw.line([(x, gy), (x + w, gy)], fill=(255, 255, 255), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, x, y, w, h) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for num, lon, lat, dx, dy in pins:
        px, py = project(lon, lat, x, y, w, h)
        px = max(x + 10, min(x + w - 10, px))
        py = max(y + 10, min(y + h - 10, py))
        bx, by = px + dx, py + dy
        bx = max(x + 10, min(x + w - 10, bx))
        by = max(y + 10, min(y + h - 10, by))
        if dx or dy:
            draw.line([(px, py), (bx, by)], fill=(60, 60, 60), width=1)
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        disc(draw, bx, by, num, radius=9)


# ------------------------------------------------------------------ data

LEADS = [
    dict(num=1, place="JUN\u00cdN, PERU", title="Quake shakes Peru",
         body=("A magnitude 6.7 earthquake struck central Peru, 129 km deep, "
               "near Jun\u00edn. Tremors were felt in Lima, 320 km away, where "
               "people ran into the streets. No casualties were reported."),
         art=art_quake),
    dict(num=2, place="PERTH, AUSTRALIA", title="Starc runs riot as Ashes open",
         body=("England were bowled out for 172 on day one of the first Ashes "
               "Test. Mitchell Starc took 7 for 58 \u2014 his first "
               "seven-wicket haul and his 100th Ashes wicket \u2014 as "
               "Australia closed on 123 for 9."),
         art=art_ashes),
    dict(num=3, place="WELLINGTON, NZ", title="Rahul completes the SENA set",
         body=("KL Rahul reached 100 off 207 balls on day three of the first "
               "Test, the first Indian opener to score Test centuries in all "
               "four SENA countries. India passed 300 in reply to New "
               "Zealand's 368."),
         art=art_rahul),
]

MINIS = [
    dict(num=4, place="LAS VEGAS, USA", title="Russell fastest in final practice",
         body=("George Russell topped final practice at the Las Vegas Grand "
               "Prix in 1:34.041 \u2014 a Mercedes one-two ahead of Kimi "
               "Antonelli \u2014 after brushing wheels with Max Verstappen."),
         art=art_f1),
    dict(num=5, place="TURIN, ITALY", title="ATP Finals: the last four meet today",
         body=("The top four seeds contest the semi-finals in Turin: Carlos "
               "Alcaraz plays Ben Shelton, Alexander Zverev faces Daniil "
               "Medvedev. The final is on Sunday."),
         art=art_atp),
    dict(num=6, place="MUMBAI, INDIA", title="Record rush into Indian shares",
         body=("Foreign investors put a record \u20b91.22 lakh crore into "
               "Indian equities between 2 and 20 November, the biggest "
               "monthly inflow on record."),
         art=art_fpi),
    dict(num=7, place="WARSAW, POLAND", title="NATO chief heads to Warsaw",
         body=("Mark Rutte visits Warsaw today as Poland seeks more allied "
               "air defences, a day after Russian missiles fell on Polish "
               "soil."),
         art=art_rutte),
    dict(num=8, place="SYDNEY, AUSTRALIA", title="Coalmine law passed at 1.36am",
         body=("New South Wales passed the Mount Pleasant coalmine expansion "
               "in a 1.36am Saturday vote, lifting annual extraction from "
               "12.5 to 16 million tonnes."),
         art=art_mine),
    dict(num=9, place="QUEENSLAND, AUSTRALIA", title="First Aussie warship wreck found",
         body=("The wreck of the first Australian-built warship has been "
               "found off the Queensland coast, 128 years after it sank."),
         art=art_wreck),
    dict(num=10, place="BASRA, IRAQ", title="Fire kills four at power station",
         body=("A fire at the Hartha power station north of Basra killed at "
               "least four people and injured 30, spreading to nearby "
               "houses and halting the plant."),
         art=art_basra),
    dict(num=11, place="RIYADH, SAUDI ARABIA", title="Three missiles at Riyadh intercepted",
         body=("The Saudi-led coalition intercepted three Houthi missiles "
               "fired at Riyadh early on Saturday, two days after a strike "
               "damaged the capital's tallest tower."),
         art=art_riyadh),
    dict(num=12, place="DARMSTADT, GERMANY", title="BepiColombo reaches Mercury",
         body=("After an eight-year journey, the ESA-JAXA BepiColombo probe "
               "fires its thrusters to enter orbit around Mercury, only the "
               "second spacecraft ever to do so."),
         art=art_bepi),
]

# (number, longitude, latitude, badge offset x, badge offset y)
PINS = [
    (1, -75.0, -11.0, 0, 0),      # Junin, Peru
    (2, 115.9, -31.9, 0, 0),      # Perth
    (3, 174.8, -41.3, 0, 0),      # Wellington
    (4, -115.1, 36.2, 0, 0),      # Las Vegas
    (5, 7.7, 45.1, -14, 6),       # Turin
    (6, 72.9, 19.1, 0, 0),        # Mumbai
    (7, 21.0, 52.2, 14, 4),       # Warsaw
    (8, 151.2, -33.9, 12, 8),     # Sydney
    (9, 146.5, -19.0, -14, -10),  # Queensland coast
    (10, 47.8, 30.5, -14, -12),   # Basra
    (11, 46.7, 24.7, 14, 10),     # Riyadh
    (12, 8.65, 49.87, 12, -14),   # Darmstadt (BepiColombo control)
]

# The pin key: two columns of six, matching the map numbers.
KEY = ["1 Jun\u00edn, Peru", "2 Perth", "3 Wellington", "4 Las Vegas",
       "5 Turin", "6 Mumbai", "7 Warsaw", "8 Sydney", "9 Queensland",
       "10 Basra", "11 Riyadh", "12 Darmstadt*"]

BRIEFS = [
    "Boy, 11, killed after being struck by a ute in Western Australia.",
    "Three-year-old boy killed by a car at a holiday park on the NSW Central Coast.",
    "Amazon pulls animal-shaped sex dolls after campaigners complain.",
    "Police warn GTA VI players over a $200 malware kit selling fake downloads.",
    "Cummins keeps Cricket Australia's \u201cunanimous support\u201d as captain.",
    "Carlos Sainz makes his 250th Grand Prix start in Las Vegas on Saturday.",
    "Rohingya Australians welcome the court ruling that Myanmar committed genocide.",
    "Sydney FC poach a rival club's boss in a \u201cnew era\u201d move.",
    "Ten new Sydney Metro stations to open next week.",
    "Toyota recalls almost 50,000 vehicles in Australia over a back-seat safety defect.",
    "Northern Territory backs the EU free-trade deal in a Coalition revolt.",
    "Security watchdog calls for a big change to the legal definition of terrorism.",
    "Foreign fishers caught off the Australian coast.",
    "India pass 300 in reply to New Zealand's 368, Rahul unbeaten on 119.",
    "Today is also World Television Day, the United Nations observance.",
    "COP31 talks resume in Antalya after Friday's overtime deadlock.",
    "Manipur liquor toll reaches 13 dead and 346 in hospital.",
    "Iran says it shot down a 58th US MQ-9 drone over the Strait of Hormuz.",
    "Iraq opens a joint security HQ in Jurf al-Sakhar, a day after retaking the town.",
    "Washington Spirit face Kansas City Current in tonight's NWSL final.",
]


# ------------------------------------------------------------------ page

def build():
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = MARGIN

    # ---- masthead
    title = "THE WORLD TODAY"
    tf = serif_bold(46)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=INK)
    d.line([(m, 62), (W - m, 62)], fill=INK, width=2)
    d.line([(m, 66), (W - m, 66)], fill=INK, width=1)

    # ---- red date band
    d.rectangle([m, 72, W - m, 100], fill=RED)
    date = "SATURDAY  \u00b7  21 NOVEMBER  \u00b7  2026"
    df = sans_bold(19)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 76), date, font=df, fill=(255, 255, 255))

    # ---- three lead stories
    lead_y, lead_h = 108, 238
    lead_w, gap = 322, 7
    for i, lead in enumerate(LEADS):
        x = m + i * (lead_w + gap)
        d.rectangle([x, lead_y, x + lead_w, lead_y + lead_h], outline=GREY,
                    width=1)
        d.rectangle([x, lead_y, x + lead_w, lead_y + 20], fill=BLUE)
        disc(d, x + 16, lead_y + 10, lead["num"], radius=9)
        d.text((x + 30, lead_y + 4), lead["place"], font=sans_bold(11),
               fill=(255, 255, 255))
        lead["art"](d, x + 1, lead_y + 21, lead_w - 2, 100, rng)
        hy = lead_y + 127
        hy = put_text(d, x + 10, hy, lead["title"], serif_bold(19),
                      lead_w - 20, 21, limit=2)
        put_text(d, x + 10, hy + 2, lead["body"], sans(12), lead_w - 20, 14,
                 limit=4)

    # ---- world map strip + pin key
    map_y, map_h = 354, 108
    map_w = 632
    d.rectangle([m, map_y, m + map_w, map_y + map_h], outline=GREY, width=1)
    d.text((m + 8, map_y + 4), "THE DAY ON THE MAP", font=sans_bold(11),
           fill=BLUE)
    paint_map(d, m + 1, map_y + 20, map_w - 2, map_h - 21, PINS)
    key_x = m + map_w + 8
    key_w = W - m - key_x
    d.rectangle([key_x, map_y, key_x + key_w, map_y + map_h], outline=GREY,
                width=1)
    d.text((key_x + 8, map_y + 4), "WHERE THE STORIES ARE",
           font=sans_bold(11), fill=BLUE)
    kf = sans(10)
    for i, label in enumerate(KEY):
        col, row = divmod(i, 6)
        kx = key_x + 8 + col * 172
        ky = map_y + 22 + row * 12
        num, _, rest = label.partition(" ")
        d.text((kx, ky), num, font=sans_bold(10), fill=RED)
        d.text((kx + 20, ky), rest, font=kf, fill=INK)
    d.text((key_x + 8, map_y + 22 + 6 * 12 + 2),
           "*12 BepiColombo control \u2014 the probe is at Mercury.",
           font=sans(9), fill=FAINT)

    # ---- nine illustrated minis, three rows of three
    mini_y0, mini_h, mini_gap = 470, 122, 5
    mini_w = 322
    for i, mini in enumerate(MINIS):
        row, col = divmod(i, 3)
        x = m + col * (mini_w + gap)
        y = mini_y0 + row * (mini_h + mini_gap)
        d.rectangle([x, y, x + mini_w, y + mini_h], outline=GREY, width=1)
        mini["art"](d, x + 1, y + 1, 100, mini_h - 2, rng)
        tx = x + 110
        disc(d, tx + 8, y + 11, mini["num"], radius=9)
        d.text((tx + 22, y + 4), mini["place"], font=sans_bold(9), fill=GREY)
        hy = put_text(d, tx, y + 24, mini["title"], serif_bold(14),
                      mini_w - 118, 16, limit=2)
        put_text(d, tx, hy + 2, mini["body"], sans(11), mini_w - 118, 12,
                 limit=5)

    # ---- brief index: twenty more stories, four columns of five
    brief_y = 852
    d.line([(m, brief_y), (W - m, brief_y)], fill=INK, width=2)
    d.text((m, brief_y + 6), "ALSO TODAY \u2014 20 MORE STORIES",
           font=sans_bold(13), fill=RED)
    col_w = (W - 2 * m - 24) // 4
    bf = sans(10)
    for i, brief in enumerate(BRIEFS):
        col, row = divmod(i, 5)
        bx = m + col * (col_w + 8)
        by = brief_y + 28 + row * 22
        d.text((bx, by), "\u25aa", font=sans_bold(10), fill=RED)
        put_text(d, bx + 12, by, brief, bf, col_w - 12, 11, limit=2)

    # ---- footer
    fy = 996
    d.line([(m, fy), (W - m, fy)], fill=INK, width=1)
    foot = ("Sources: Reuters, BBC, AP, AFP, Cricbuzz, Formula 1, ATP, NASA, "
            "ESA, The West Australian. Every story happened, or was first "
            "reported, on Saturday 21 November 2026.")
    put_text(d, m, fy + 6, foot, sans(10), W - 2 * m, 13, fill=GREY,
             limit=1)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    img = build()
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
