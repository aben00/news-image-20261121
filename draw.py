#!/usr/bin/env python3
"""Draw "The World Today" -- a one-page newspaper front page summing up
Saturday 21 November 2026, as a 1024x1024 PNG.

Layout: masthead + red date band, three illustrated lead stories, a pinned
world map, six illustrated minis, and a brief index of fifteen more stories.

Deterministic: fixed random seed, no clock, no network, no file reads
beyond the system fonts. Run: python3 draw.py <output.png>

Every story happened, or was first reported, on Saturday 21 November
2026. Stories first reported on 20 November or earlier -- the Russian
missiles in Poland, the UK-EU summit deal, the Denmark rapper plot, the
Rajasthan panchayat results, the Gupta sentencing, the Trump data-centre
press conference, the Kryvyi Rih strike -- were checked and left out,
except where a story has a genuine 21 November development stated on
the page (NATO chief Rutte's visit to Warsaw today).
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SEED = 20261121

PAPER = (247, 243, 232)
INK = (24, 24, 24)
RED = (178, 28, 28)
BLUE = (28, 56, 96)
GREY = (92, 88, 78)
LIGHTGREY = (120, 116, 104)
SEA = (183, 210, 224)
LAND = (203, 192, 154)
LAND_LINE = (146, 136, 106)
GOLD = (198, 142, 32)


def pick_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def serif_b(size):
    return pick_font(["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"], size)


def serif(size):
    return pick_font(["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                      "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"], size)


def sans(size):
    return pick_font(["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"], size)


def sans_b(size):
    return pick_font(["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"], size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, max_w, leading, fill=INK, max_lines=None):
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(d, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def badge(d, x, y, num, r=11):
    """Numbered red disc used by leads, minis and the map pins."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    f = sans_b(13 if r <= 11 else 15)
    tw = d.textlength(str(num), font=f)
    th = f.getbbox("9")[3]
    d.text((x - tw / 2, y - th / 2 - 1), str(num), font=f, fill=(255, 255, 255))


def star(d, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


# ------------------------------------------------------------------ leads

def draw_quake(d, x, y, w, h, rng):
    """Junin, Peru: night ground, jagged crack, seismograph trace."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 52))
    for _ in range(30):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, int(h * 0.5))
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(215, 215, 195))
    d.ellipse([x + w - 46, y + 10, x + w - 18, y + 38], fill=(236, 230, 198))
    # shaking houses
    base = y + h - 34
    bx = x + 14
    while bx < x + w - 40:
        bw = rng.randint(34, 52)
        bh = rng.randint(30, 52)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(12, 16, 30))
        for _ in range(bh // 12):
            wx = bx + rng.randint(5, max(6, bw - 8))
            wy = base - bh + rng.randint(6, max(7, bh - 8))
            if rng.random() < 0.5:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 105))
        bx += bw + rng.randint(6, 12)
    # jagged crack across the ground
    pts = [(x, y + h - 30)]
    cx = x
    while cx < x + w:
        cx += rng.randint(14, 26)
        pts.append((min(cx, x + w), y + h - 30 + rng.randint(-8, 10)))
    d.line(pts, fill=(255, 120, 60), width=3)
    # seismograph trace
    tx, ty = x + 12, y + h - 66
    prev = (tx, ty)
    for i in range(1, 60):
        nx = tx + i * (w - 24) / 60
        amp = 2 if i < 18 else (26 if 24 < i < 44 else 5)
        ny = ty + rng.randint(-amp, amp)
        d.line([prev, (nx, ny)], fill=(120, 220, 130), width=2)
        prev = (nx, ny)


def draw_ashes(d, x, y, w, h, rng):
    """Perth: green outfield, stumps, bat and red ball, big 7/58."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 110, 58))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(38, 88, 44))
    # pitch strip
    d.rectangle([x + w // 2 - 34, y + 18, x + w // 2 + 34, y + h - 46],
                fill=(196, 172, 118))
    # stumps at both ends
    for sy in (y + 30, y + h - 78):
        for k in range(3):
            sx = x + w // 2 - 12 + k * 12
            d.rectangle([sx, sy, sx + 4, sy + 26], fill=(232, 196, 90))
    # bat leaning on the pitch
    d.line([(x + w // 2 + 58, y + 40), (x + w // 2 + 88, y + 96)],
           fill=(214, 178, 120), width=9)
    d.line([(x + w // 2 + 88, y + 96), (x + w // 2 + 98, y + 118)],
           fill=(190, 150, 96), width=12)
    # red ball with seam
    cx, cy = x + w // 2 - 78, y + 78
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(178, 30, 30))
    d.arc([cx - 15, cy - 15, cx + 15, cy + 15], 200, 340, fill=(255, 255, 255), width=2)
    # score figures
    d.text((x + 14, y + h - 44), "172", font=serif_b(30), fill=(255, 255, 255))
    d.text((x + w - 108, y + h - 44), "7/58", font=serif_b(30), fill=(255, 214, 110))


def draw_rahul(d, x, y, w, h, rng):
    """Wellington: blue sky, batsman, bat raised, ball, and a big 100."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 74, 128))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(46, 96, 52))
    # sun
    d.ellipse([x + w - 56, y + 10, x + w - 26, y + 40], fill=(255, 214, 110))
    # crowd dots
    for _ in range(40):
        sx = x + rng.randint(4, w - 4)
        sy = y + h - rng.randint(28, 44)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2],
                  fill=rng.choice([(255, 255, 255), (255, 214, 110), (200, 220, 255)]))
    # batsman: head, body, legs, raised bat
    cx = x + w // 2 - 20
    d.ellipse([cx - 12, y + 36, cx + 12, y + 60], fill=(232, 188, 150))
    d.rectangle([cx - 13, y + 60, cx + 13, y + 92], fill=(20, 40, 90))
    d.rectangle([cx - 11, y + 92, cx - 2, y + h - 26], fill=(24, 24, 24))
    d.rectangle([cx + 2, y + 92, cx + 11, y + h - 26], fill=(24, 24, 24))
    d.line([(cx + 11, y + 68), (cx + 48, y + 30)], fill=(214, 178, 120), width=8)
    d.line([(cx + 48, y + 30), (cx + 60, y + 12)], fill=(190, 150, 96), width=11)
    # ball flying off
    bx, by = x + w - 58, y + 52
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(200, 40, 40))
    # big hundred
    d.text((x + 14, y + h - 42), "100", font=serif_b(30), fill=(255, 255, 255))
    d.text((x + w - 128, y + h - 36), "SENA SET", font=sans_b(15), fill=(255, 214, 110))


# ------------------------------------------------------------------ minis

def draw_f1(d, x, y, w, h, rng):
    """Las Vegas: night street circuit, race car, chequered flag."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 20, 34))
    # track
    d.rectangle([x, y + h - 34, x + w, y + h - 20], fill=(52, 52, 58))
    for i in range(0, w, 26):
        d.rectangle([x + i, y + h - 29, x + i + 14, y + h - 25], fill=(240, 220, 90))
    # city lights
    for _ in range(18):
        lx = x + rng.randint(4, w - 8)
        ly = y + rng.randint(4, 26)
        d.rectangle([lx, ly, lx + 3, ly + 8],
                    fill=rng.choice([(255, 90, 160), (90, 200, 255), (255, 214, 110)]))
    # race car side profile
    cy = y + h - 44
    d.polygon([(x + 18, cy), (x + 34, cy - 16), (x + 62, cy - 18),
               (x + 78, cy - 6), (x + 96, cy)], fill=(200, 30, 30))
    d.rectangle([x + 40, cy - 26, x + 62, cy - 16], fill=(30, 30, 40))
    d.ellipse([x + 26, cy - 6, x + 42, cy + 10], fill=(12, 12, 12))
    d.ellipse([x + 72, cy - 6, x + 88, cy + 10], fill=(12, 12, 12))
    d.ellipse([x + 31, cy - 1, x + 37, cy + 5], fill=(180, 180, 180))
    d.ellipse([x + 77, cy - 1, x + 83, cy + 5], fill=(180, 180, 180))
    # chequered flag
    fx = x + w - 26
    for r in range(3):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([fx + c * 6, y + 8 + r * 6, fx + c * 6 + 6, y + 14 + r * 6],
                            fill=(20, 20, 20))
            else:
                d.rectangle([fx + c * 6, y + 8 + r * 6, fx + c * 6 + 6, y + 14 + r * 6],
                            fill=(255, 255, 255))
    d.line([(fx, y + 8), (fx, y + 44)], fill=(200, 200, 200), width=2)


def draw_atp(d, x, y, w, h, rng):
    """Turin: indoor hard court, net, tennis ball."""
    d.rectangle([x, y, x + w, y + h], fill=(44, 84, 148))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 60, 110))
    # court lines
    d.rectangle([x + 10, y + 12, x + w - 10, y + h - 34], outline=(255, 255, 255), width=2)
    d.line([(x + w // 2, y + 12), (x + w // 2, y + h - 34)], fill=(255, 255, 255), width=2)
    # net
    d.rectangle([x + 8, y + h // 2 - 4, x + w - 8, y + h // 2 + 4], fill=(240, 240, 240))
    # ball
    bx, by = x + w - 30, y + 26
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(200, 230, 60))
    d.arc([bx - 13, by - 13, bx + 13, by + 13], 40, 140, fill=(255, 255, 255), width=2)
    d.arc([bx - 13, by - 13, bx + 13, by + 13], 220, 320, fill=(255, 255, 255), width=2)
    # racket
    d.ellipse([x + 16, y + h - 52, x + 44, y + h - 24], outline=(220, 220, 220), width=4)
    d.line([(x + 30, y + h - 26), (x + 44, y + h - 8)], fill=(220, 220, 220), width=4)


def draw_fpi(d, x, y, w, h, rng):
    """Mumbai: rising market bars and the rupee sign."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 64, 48))
    bars = [18, 26, 22, 36, 44, 58]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx0 = x + 16 + i * bw
        d.rectangle([bx0, y + h - 18 - bh, bx0 + bw - 6, y + h - 18],
                    fill=(90, 200, 130) if i < 5 else (255, 214, 110))
    # trend arrow
    pts = [(x + 16, y + h - 40), (x + 40, y + h - 56), (x + 62, y + h - 48),
           (x + 86, y + h - 72), (x + w - 12, y + h - 84)]
    d.line(pts, fill=(255, 255, 255), width=3)
    d.polygon([(x + w - 12, y + h - 84), (x + w - 24, y + h - 82),
               (x + w - 14, y + h - 72)], fill=(255, 255, 255))
    d.text((x + 10, y + 6), "\u20b9", font=serif_b(26), fill=(255, 255, 255))


def draw_rutte(d, x, y, w, h, rng):
    """Warsaw: EU flag and Polish flag side by side."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
    # EU flag
    d.rectangle([x + 8, y + 14, x + 58, y + h - 14], fill=(0, 51, 153))
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        sx = x + 33 + 15 * math.cos(a)
        sy = y + h // 2 + 15 * math.sin(a)
        star(d, sx, sy, 3, 1.4, 5, (255, 204, 0))
    # Polish flag
    d.rectangle([x + 66, y + 14, x + w - 8, y + (h - 14) // 2 + 7], fill=(255, 255, 255))
    d.rectangle([x + 66, y + (h - 14) // 2 + 7, x + w - 8, y + h - 14], fill=(220, 20, 60))
    d.rectangle([x + 66, y + 14, x + w - 8, y + h - 14], outline=(120, 120, 120), width=1)


def draw_mine(d, x, y, w, h, rng):
    """New South Wales: terraced open-cut mine and a haul truck."""
    d.rectangle([x, y, x + w, y + h], fill=(122, 84, 52))
    # terraces
    for i, ty in enumerate([y + 12, y + 34, y + 56]):
        d.rectangle([x + i * 8, ty, x + w, ty + 18], fill=(96 + i * 14, 64 + i * 10, 40))
    d.rectangle([x, y + 78, x + w, y + h], fill=(52, 40, 30))
    # haul truck
    tx, ty = x + 18, y + h - 30
    d.rectangle([tx, ty - 14, tx + 34, ty], fill=(240, 190, 40))
    d.rectangle([tx + 34, ty - 10, tx + 46, ty], fill=(220, 170, 30))
    d.ellipse([tx + 4, ty - 2, tx + 14, ty + 8], fill=(16, 16, 16))
    d.ellipse([tx + 22, ty - 2, tx + 32, ty + 8], fill=(16, 16, 16))
    d.ellipse([tx + 38, ty - 2, tx + 46, ty + 6], fill=(16, 16, 16))
    # coal lumps
    for _ in range(8):
        lx = x + rng.randint(w // 2, w - 10)
        ly = y + h - rng.randint(6, 16)
        d.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=(20, 20, 20))


def draw_wreck(d, x, y, w, h, rng):
    """Queensland coast: half-sunk warship, waves, bubbles."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 78, 110))
    # sun glint
    d.ellipse([x + w - 44, y + 8, x + w - 16, y + 36], fill=(255, 220, 120))
    # ship hull tilted
    d.polygon([(x + 12, y + h - 52), (x + 74, y + h - 52), (x + 62, y + h - 34),
               (x + 22, y + h - 34)], fill=(90, 90, 96))
    d.rectangle([x + 30, y + h - 68, x + 44, y + h - 52], fill=(70, 70, 76))
    d.line([(x + 37, y + h - 68), (x + 37, y + h - 82)], fill=(60, 60, 66), width=3)
    # waves
    for wy in (y + h - 30, y + h - 16):
        prev = None
        for i in range(25):
            px = x + i * (w / 24)
            py = wy + 3 * math.sin(i * 0.9)
            if prev is not None:
                d.line([prev, (px, py)], fill=(200, 225, 240), width=2)
            prev = (px, py)
    # bubbles
    for _ in range(10):
        bx = x + rng.randint(60, w - 10)
        by = y + rng.randint(10, h - 60)
        r = rng.randint(1, 3)
        d.ellipse([bx - r, by - r, bx + r, by + r], outline=(220, 235, 245), width=1)


# ------------------------------------------------------------------- map

# Simplified continent outlines (lon, lat) in a rough equirectangular view.
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


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    """Equirectangular projection into the map box."""
    px = mx + (lon + 180.0) / 360.0 * mw
    py = my + (75.0 - lat) / 130.0 * mh
    return px, py


def draw_map(d, x, y, w, h, pins, rng):
    """Sea, graticule, continents, numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # graticule
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360 * w
        d.line([(gx, y), (gx, y + h)], fill=(255, 255, 255), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y + (75 - lat) / 130 * h
        d.line([(x, gy), (x + w, gy)], fill=(255, 255, 255), width=1)
    # continents
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x, y, w, h) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    # pins (clamped inside the box so edge pins stay visible)
    for num, lon, lat in pins:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        px = max(x + 12, min(x + w - 12, px))
        py = max(y + 12, min(y + h - 12, py))
        badge(d, px, py, num, r=11)


# ------------------------------------------------------------------ page

LEADS = [
    dict(num=1, place="JUNIN, PERU", title="Quake shakes Peru",
         body=("A magnitude 6.8 earthquake struck central Peru, its epicentre "
               "in the Andes of Junin, 129 km deep. Tremors were felt in Lima, "
               "320 km away, where people ran into the streets. No casualties "
               "were reported."),
         draw=draw_quake),
    dict(num=2, place="PERTH, AUSTRALIA", title="Starc runs riot as Ashes open",
         body=("England were bowled out for 172 on day one of the first Ashes "
               "Test. Mitchell Starc took 7 for 58, his first seven-wicket haul "
               "and his 100th Ashes wicket. Ben Stokes hit back with 5 for 23 "
               "as Australia closed on 123 for 9."),
         draw=draw_ashes),
    dict(num=3, place="WELLINGTON, NZ", title="Rahul completes the SENA set",
         body=("KL Rahul reached 100 off 207 balls on day three of the first "
               "Test, the first Indian opener to score Test centuries in all "
               "four SENA countries. India passed 300 in reply to New "
               "Zealand's 368, Rahul unbeaten on 119."),
         draw=draw_rahul),
]

MINIS = [
    dict(num=4, place="LAS VEGAS, USA", title="Russell fastest in final practice",
         body=("George Russell topped the last practice at the Las Vegas Grand "
               "Prix in 1:34.041, a Mercedes one-two ahead of Kimi Antonelli, "
               "after brushing wheels with Max Verstappen."),
         draw=draw_f1),
    dict(num=5, place="TURIN, ITALY", title="ATP Finals: the last four meet today",
         body=("The top four seeds contest the semi-finals in Turin: Carlos "
               "Alcaraz plays Ben Shelton, Alexander Zverev faces Daniil "
               "Medvedev. The final is on Sunday."),
         draw=draw_atp),
    dict(num=6, place="MUMBAI, INDIA", title="Record rush into Indian shares",
         body=("Foreign investors put a record \u20b91.22 lakh crore into Indian "
               "equities between 2 and 20 November, the biggest monthly "
               "inflow on record, beating November 2020."),
         draw=draw_fpi),
    dict(num=7, place="WARSAW, POLAND", title="NATO chief heads to Warsaw",
         body=("Mark Rutte visits Warsaw today as Poland seeks more allied air "
               "defences, a day after Russian missiles fell on Polish soil "
               "and Donald Tusk called it an intentional provocation."),
         draw=draw_rutte),
    dict(num=8, place="SYDNEY, AUSTRALIA", title="Coalmine law passed at 1.36am",
         body=("New South Wales passed the Mount Pleasant coalmine expansion "
               "in a 1.36am Saturday vote, lifting its annual extraction "
               "rate from 12.5 to 16 million tonnes."),
         draw=draw_mine),
    dict(num=9, place="QUEENSLAND, AUSTRALIA", title="First Aussie warship wreck found",
         body=("The wreck of the first Australian-built warship has been found "
               "off the Queensland coast, 128 years after it sank."),
         draw=draw_wreck),
]

# (number, longitude, latitude) for the map pins.
PINS = [
    (1, -77.0, -12.0),    # Junin, Peru
    (2, 115.9, -31.9),    # Perth
    (3, 174.8, -41.3),    # Wellington
    (4, -115.1, 36.2),    # Las Vegas
    (5, 7.7, 45.1),       # Turin
    (6, 72.9, 19.1),      # Mumbai
    (7, 21.0, 52.2),      # Warsaw
    (8, 151.2, -33.9),    # Sydney
    (9, 146.5, -19.0),    # Queensland coast
]

BRIEFS = [
    "Boy, 11, killed after being struck by a ute in Western Australia.",
    "Three-year-old boy killed by a car at a holiday park on the NSW Central Coast.",
    "Amazon pulls animal-shaped sex dolls from its platform after campaigners complain.",
    "Police warn GTA VI players over a $200 malware kit selling fake downloads.",
    "Cummins keeps Cricket Australia's \u201cunanimous support\u201d as captain despite missing the Ashes opener injured.",
    "Carlos Sainz makes his 250th Grand Prix start in Las Vegas on Saturday.",
    "Rohingya Australians welcome the court ruling that Myanmar committed genocide.",
    "Sydney FC poach a rival club's boss in a \u201cnew era\u201d move.",
    "Ten new Sydney Metro stations to open next week, slashing western Sydney commutes.",
    "Toyota recalls almost 50,000 vehicles in Australia over a back-seat safety defect.",
    "Northern Territory backs the EU free-trade deal in a Coalition revolt.",
    "Australia's security watchdog calls for a big change to the legal definition of terrorism.",
    "Foreign fishers caught off the Australian coast.",
    "India pass 300 in reply to New Zealand's 368, Rahul unbeaten on 119.",
    "Today is also World Television Day, the United Nations observance.",
]


def build():
    rng = random.Random(SEED)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16  # margin

    # ---- masthead
    title = "THE WORLD TODAY"
    tf = serif_b(46)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=INK)
    d.line([(M, 62), (W - M, 62)], fill=INK, width=2)
    d.line([(M, 66), (W - M, 66)], fill=INK, width=1)

    # ---- red date band
    d.rectangle([M, 72, W - M, 100], fill=RED)
    date = "SATURDAY  \u00b7  21 NOVEMBER  \u00b7  2026"
    df = sans_b(19)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 76), date, font=df, fill=(255, 255, 255))

    # ---- three lead stories
    lead_y, lead_h = 110, 282
    lead_w, gap = 322, 7
    for i, lead in enumerate(LEADS):
        x = M + i * (lead_w + gap)
        d.rectangle([x, lead_y, x + lead_w, lead_y + lead_h], outline=GREY, width=1)
        d.rectangle([x, lead_y, x + lead_w, lead_y + 20], fill=BLUE)
        badge(d, x + 16, lead_y + 10, lead["num"], r=9)
        pf = sans_b(11)
        d.text((x + 30, lead_y + 4), lead["place"], font=pf, fill=(255, 255, 255))
        ix, iy, iw, ih = x + 1, lead_y + 21, lead_w - 2, 132
        lead["draw"](d, ix, iy, iw, ih, rng)
        hf = serif_b(20)
        hy = lead_y + 21 + ih + 6
        hy = text_block(d, x + 10, hy, lead["title"], hf, lead_w - 20, 22,
                        max_lines=2)
        bf = sans(12)
        text_block(d, x + 10, hy + 2, lead["body"], bf, lead_w - 20, 14,
                   max_lines=5)

    # ---- world map strip
    map_y, map_h = 402, 138
    d.rectangle([M, map_y, W - M, map_y + map_h], outline=GREY, width=1)
    d.text((M + 8, map_y + 5), "THE DAY ON THE MAP", font=sans_b(11), fill=BLUE)
    draw_map(d, M + 1, map_y + 22, W - 2 * M - 2, map_h - 23, PINS, rng)

    # ---- six illustrated minis, two rows of three
    mini_y0, mini_h, mini_gap = 550, 138, 7
    mini_w = 322
    for i, mini in enumerate(MINIS):
        row, col = divmod(i, 3)
        x = M + col * (mini_w + mini_gap)
        y = mini_y0 + row * (mini_h + mini_gap)
        d.rectangle([x, y, x + mini_w, y + mini_h], outline=GREY, width=1)
        ix, iy, iw, ih = x + 1, y + 1, 108, mini_h - 2
        mini["draw"](d, ix, iy, iw, ih, rng)
        tx = x + 118
        badge(d, x + 118, y + 12, mini["num"], r=9)
        d.text((x + 132, y + 5), mini["place"], font=sans_b(9), fill=GREY)
        hf = serif_b(14)
        hy = text_block(d, tx, y + 24, mini["title"], hf, mini_w - 128, 17,
                        max_lines=2)
        bf = sans(11)
        text_block(d, tx, hy + 2, mini["body"], bf, mini_w - 128, 13,
                   max_lines=5)

    # ---- brief index
    brief_y = 840
    d.line([(M, brief_y), (W - M, brief_y)], fill=INK, width=2)
    d.text((M, brief_y + 6), "ALSO TODAY", font=sans_b(13), fill=RED)
    col_w = (W - 2 * M - 16) // 3
    bf = sans(11)
    for i, brief in enumerate(BRIEFS):
        col, row = divmod(i, 5)
        bx = M + col * (col_w + 8)
        by = brief_y + 24 + row * 24
        d.text((bx, by), "\u25aa", font=sans_b(11), fill=RED)
        text_block(d, bx + 12, by, brief, bf, col_w - 12, 12, max_lines=2)

    # ---- footer
    fy = 990
    d.line([(M, fy), (W - M, fy)], fill=INK, width=1)
    foot = ("Sources: Reuters, BBC, AP, Cricbuzz, Formula 1, ATP, The West Australian, "
            "The Daily Short.  Every story above happened, or was first reported, "
            "on Saturday 21 November 2026.")
    text_block(d, M, fy + 6, foot, sans(10), W - 2 * M, 13, fill=GREY,
               max_lines=2)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    img = build()
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
