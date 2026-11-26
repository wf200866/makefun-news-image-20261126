#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news hero magazine as a 1024x1024 PNG."""
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (244, 239, 228)
INK = (20, 22, 26)
NAVY = (14, 21, 40)
RED = (193, 39, 45)
TEAL = (14, 124, 123)
AMBER = (219, 148, 42)
VIOLET = (91, 62, 150)
GREEN = (38, 120, 74)
SLATE = (54, 66, 88)
MUTED = (108, 104, 96)
WHITE = (255, 255, 255)
CREAM = (250, 246, 236)

FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d, text, f):
    return d.textlength(text, font=f)


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if tw(d, test, f) <= maxw or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, f, x, y, fill, gap=1.18):
    lh = f.size * gap
    for i, line in enumerate(lines):
        d.text((x, y + i * lh), line, font=f, fill=fill)
    return y + len(lines) * lh


def wrap_draw(d, text, f, x, y, maxw, fill, gap=1.18):
    return draw_lines(d, wrap(d, text, f, maxw), f, x, y, fill, gap)


def fit_block(d, text, path, size, maxw, maxh, floor=10, gap=1.16):
    """Pick the largest size whose wrapped paragraph fits maxw x maxh."""
    s = size
    while s > floor:
        f = font(path, s)
        lines = wrap(d, text, f, maxw)
        if len(lines) * f.size * gap <= maxh:
            return f, lines
        s -= 1
    f = font(path, s)
    return f, wrap(d, text, f, maxw)


def mix(c1, c2, t):
    return tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))


def tint(c, t=0.86):
    return mix(c, WHITE, t)


def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        d.line([(x0, y), (x1, y)], fill=mix(top, bottom, t))


# ---------------------------------------------------------------- header
def header(d):
    d.rectangle([0, 0, W, 120], fill=NAVY)
    cap = font(FONT_SANS_B, 16)
    label = "WORLD NEWS  ·  THE DAY IN ONE IMAGE"
    d.text(((W - tw(d, label, cap)) / 2, 14), label, font=cap, fill=AMBER)
    date_f = font(FONT_SANS_B, 45)
    date = "THURSDAY 26 NOVEMBER 2026"
    d.text(((W - tw(d, date, date_f)) / 2, 44), date, font=date_f, fill=WHITE)
    d.rectangle([0, 114, W, 126], fill=RED)
    sub = font(FONT_SANS, 17)
    line = "Thanksgiving nor'easter  ·  India tariffs  ·  Gaza warning  ·  Huawei verdict  ·  Shein  ·  Cricket history"
    d.rectangle([0, 126, W, 158], fill=CREAM)
    d.text(((W - tw(d, line, sub)) / 2, 132), line, font=sub, fill=MUTED)


# ---------------------------------------------------------------- hero
def cloud(d, cx, cy, w, h, color):
    for dx, dy, ew, eh in [(-0.30, 0.10, 0.55, 0.80), (0.0, -0.10, 0.62, 1.00),
                           (0.30, 0.10, 0.55, 0.80), (0.0, 0.22, 0.80, 0.55)]:
        d.ellipse([cx + dx * w - ew * w / 2, cy + dy * h - eh * h / 2,
                   cx + dx * w + ew * w / 2, cy + dy * h + eh * h / 2], fill=color)


def balloon(d, cx, cy, rw, rh, color):
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=color)
    d.ellipse([cx - rw * 0.55, cy - rh * 0.72, cx - rw * 0.05, cy - rh * 0.30],
              fill=mix(color, WHITE, 0.45))
    # little tail + tether
    d.polygon([(cx - rw * 0.20, cy + rh * 0.92), (cx + rw * 0.20, cy + rh * 0.92),
               (cx, cy + rh * 1.18)], fill=color)
    d.line([(cx, cy + rh * 1.15), (cx - rw * 0.25, cy + rh + 60)], fill=(30, 36, 52), width=2)


def hero(d):
    top, bot = 162, 470
    vgrad(d, (0, top, W, bot), (43, 55, 84), (120, 130, 150))
    # storm clouds
    for cx, cy, w, h, c in [(700, 250, 360, 120, (70, 82, 108)),
                            (870, 300, 300, 110, (58, 70, 96)),
                            (560, 300, 260, 90, (82, 94, 120))]:
        cloud(d, cx, cy, w, h, c)
    # rain streaks
    import random
    random.seed(7)
    for _ in range(70):
        x = random.randint(470, 1010)
        y = random.randint(250, 430)
        ln = random.randint(10, 22)
        d.line([(x, y), (x - 5, y + ln)], fill=(150, 162, 184), width=1)
    # skyline
    sky = (26, 33, 52)
    base = bot - 6
    buildings = [(470, 70), (505, 96), (545, 60), (580, 120), (625, 82), (665, 140),
                 (712, 70), (748, 104), (792, 64), (828, 118), (872, 88), (912, 132),
                 (958, 96), (995, 70)]
    for x, hgt in buildings:
        d.rectangle([x, base - hgt, x + 30, base], fill=sky)
        for wy in range(base - hgt + 12, base - 8, 16):
            for wx in range(x + 6, x + 26, 9):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(196, 170, 96))
    # balloons grounded low on the right
    balloon(d, 730, 392, 46, 54, (176, 44, 52))
    balloon(d, 830, 404, 40, 47, (32, 120, 150))
    balloon(d, 918, 396, 36, 42, (214, 160, 52))
    d.line([(0, base), (W, base)], fill=(15, 19, 30), width=4)

    # text panel
    d.rectangle([24, 188, 560, 452], fill=(16, 22, 38))
    d.rectangle([24, 188, 34, 452], fill=RED)
    tag = font(FONT_SANS_B, 16)
    d.rectangle([50, 206, 50 + tw(d, "THANKSGIVING", tag) + 20, 232], fill=RED)
    d.text((60, 209), "THANKSGIVING", font=tag, fill=WHITE)
    d.text((50 + tw(d, "THANKSGIVING", tag) + 30, 210), "NEW YORK", font=tag, fill=AMBER)
    head = font(FONT_SANS_B, 38)
    y = 250
    y = draw_lines(d, wrap(d, "MACY'S 100th PARADE POSTPONED", head, 486), head, 50, y, WHITE, 1.02)
    body = font(FONT_SANS, 20)
    sub = "First weather delay ever: a nor'easter with 60 mph gusts grounds the balloons; parade moved to Sat 28 Nov."
    bf, blines = fit_block(d, sub, FONT_SANS, 20, 486, 424 - (y + 10), floor=15, gap=1.26)
    y = draw_lines(d, blines, bf, 50, y + 10, (226, 230, 238), 1.26)
    fine = font(FONT_SANS_B, 15)
    d.text((50, 430), "Mayor Zohran Mamdani confirms  ·  100th edition", font=fine, fill=AMBER)


# ---------------------------------------------------------------- cards
def stat_icon(d, box, text, color, big=46):
    x0, y0, x1, y1 = box
    f = font(FONT_SANS_B, big)
    d.text(((x0 + x1 - tw(d, text, f)) / 2, (y0 + y1 - f.size) / 2 - 4),
           text, font=f, fill=color)


def gavel(d, cx, cy, color, r=1.0):
    d.rounded_rectangle([cx - 46 * r, cy - 30 * r, cx + 10 * r, cy - 14 * r], radius=4, fill=color)
    d.rounded_rectangle([cx + 4 * r, cy - 34 * r, cx + 16 * r, cy - 10 * r], radius=3, fill=color)
    d.line([(cx - 18 * r, cy - 8 * r), (cx + 8 * r, cy + 34 * r)], fill=color, width=max(3, int(10 * r)))
    d.rounded_rectangle([cx - 54 * r, cy + 34 * r, cx + 8 * r, cy + 44 * r], radius=3, fill=color)


def bag(d, cx, cy, color, r=1.0):
    d.rounded_rectangle([cx - 24 * r, cy - 18 * r, cx + 24 * r, cy + 28 * r], radius=5, fill=color)
    d.arc([cx - 12 * r, cy - 30 * r, cx + 12 * r, cy - 6 * r], 180, 360, fill=color, width=int(4 * r))
    f = font(FONT_SANS_B, int(22 * r))
    d.text((cx - tw(d, "$", f) / 2, cy - 12 * r), "$", font=f, fill=WHITE)


def warning(d, cx, cy, color):
    d.polygon([(cx, cy - 48), (cx + 52, cy + 42), (cx - 52, cy + 42)], fill=color)
    f = font(FONT_SANS_B, 54)
    d.text((cx - tw(d, "!", f) / 2, cy + 18), "!", font=f, fill=WHITE)


def card(d, box, accent, kicker, head, body, icon, head_px=27, icon_w=116, compact=False):
    x0, y0, x1, y1 = box
    bg = tint(accent, 0.88)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=bg, outline=mix(accent, WHITE, 0.55), width=1)
    d.rounded_rectangle([x0, y0, x0 + 9, y1], radius=4, fill=accent)
    if compact:
        # Small cards: one text column, a corner glyph kept above the headline,
        # and a summary fitted to the space that is actually left.
        pad = 16
        textw = (x1 - x0) - 2 * pad
        kf = font(FONT_SANS_B, 13)
        d.text((x0 + pad, y0 + 10), kicker, font=kf, fill=accent)
        if icon == "gavel":
            gavel(d, x1 - 24, y0 + 22, accent, r=0.30)
        elif icon == "bag":
            bag(d, x1 - 25, y0 + 24, accent, r=0.34)
        head_top = y0 + 38
        hs = head_px
        hf = font(FONT_SANS_B, hs)
        hlines = wrap(d, head, hf, textw)
        while hs > 16 and len(hlines) * hs * 1.04 > 46:
            hs -= 1
            hf = font(FONT_SANS_B, hs)
            hlines = wrap(d, head, hf, textw)
        hy = draw_lines(d, hlines, hf, x0 + pad, head_top, INK, 1.04)
        bf, blines = fit_block(d, body, FONT_SANS, 13, textw, (y1 - 10) - (hy + 4))
        bottom = draw_lines(d, blines, bf, x0 + pad, hy + 4, (66, 62, 56), 1.13)
        if bottom > y1 - 4:
            raise SystemExit(f"compact card overflow: {kicker}")
        return
    pad = 20
    textw = (x1 - icon_w) - (x0 + pad) - 8
    kf = font(FONT_SANS_B, 14)
    d.text((x0 + pad, y0 + 12), kicker, font=kf, fill=accent)
    hf = font(FONT_SANS_B, head_px)
    hy = y0 + 32
    hlines = wrap(d, head, hf, textw)
    hy = draw_lines(d, hlines, hf, x0 + pad, hy, INK, 1.04)
    bf = font(FONT_SANS, max(13, head_px - 11))
    wrap_draw(d, body, bf, x0 + pad, hy + 5, textw, (66, 62, 56), 1.16)
    if icon == "trade":
        stat_icon(d, (x1 - icon_w, y0, x1 - 6, y1 - 22), "25%", accent, 44)
        af = font(FONT_SANS_B, 18)
        d.text((x1 - icon_w + (icon_w - tw(d, "TARIFFS", af)) / 2 - 3, y1 - 30), "TARIFFS", font=af, fill=accent)
    elif icon == "warning":
        warning(d, (x1 - icon_w / 2 - 4), (y0 + y1) / 2, accent)
    elif icon == "gavel":
        gavel(d, x1 - icon_w / 2 - 6, (y0 + y1) / 2, accent)
    elif icon == "money":
        stat_icon(d, (x1 - icon_w, y0, x1 - 6, y1 - 22), "$100M", accent, 34)
        af = font(FONT_SANS_B, 15)
        d.text((x1 - icon_w + (icon_w - tw(d, "FTC", af)) / 2 - 3, y1 - 30), "FTC", font=af, fill=accent)
    elif icon == "sport":
        stat_icon(d, (x1 - 210, y0, x1 - 20, y1 - 22), "204", accent, 58)
        af = font(FONT_SANS_B, 16)
        t = "off 53 balls · 28 sixes"
        d.text((x1 - 210 + (190 - tw(d, t, af)) / 2, y1 - 30), t, font=af, fill=accent)


def cards(d):
    card(d, (12, 482, 572, 632), AMBER, "TRADE  ·  WASHINGTON / NEW DELHI",
         "US proposes up to 25% tariffs on Indian goods",
         "Section 301 action against 14 economies over excess industrial capacity; 17% if a trade deal is reached.",
         "trade", head_px=26, icon_w=116)
    card(d, (584, 482, 1012, 786), VIOLET, "UN  ·  GAZA / WEST BANK",
         "UN warns of widening risk of atrocity crimes",
         "Rights chief Volker Turk says the warnings \"have not been heeded\" as the danger grows for Palestinians in Gaza and the West Bank.",
         "warning", head_px=29, icon_w=130)
    card(d, (12, 644, 274, 794), SLATE, "COURTS  ·  NEW YORK",
         "Huawei convicted on 10 of 12 counts",
         "Brooklyn jury; acquitted of racketeering conspiracy.",
         "gavel", head_px=22, icon_w=74, compact=True)
    card(d, (286, 644, 572, 794), RED, "BUSINESS  ·  FTC",
         "Shein to pay $100M to settle FTC case",
         "Claims it misled US shoppers on shipping delays, hidden reviews and cotton origin.",
         "money", head_px=22, icon_w=104, compact=True)
    card(d, (12, 806, 1012, 966), GREEN, "SPORT  ·  DOHA",
         "15-year-old Vaibhav Sooryavanshi hits 204 off 53 balls",
         "28 sixes for India A against UAE: the fastest List A hundred (28 balls) and double hundred (52 balls).",
         "sport", head_px=30, icon_w=210)


def footer(d):
    d.line([(12, 978), (W - 12, 978)], fill=(186, 178, 160), width=1)
    af = font(FONT_SANS_B, 14)
    label = "ALSO   "
    x = 12
    d.text((x, 985), label, font=af, fill=RED)
    x += tw(d, label, af)
    also = "Andy Taylor dies at 65  ·  Giuliani awarded Medal of Freedom  ·  2,100 migrants reach Canary Islands in a day  ·  China-Cambodia drills"
    f = font(FONT_SANS, 13)
    for seg in also.split("  ·  "):
        piece = seg + ("  ·  " if seg != "China-Cambodia drills" else "")
        d.text((x, 986), piece, font=f, fill=INK)
        x += tw(d, piece, f)
    sf = font(FONT_SANS, 11)
    src = "Sources: Reuters  ·  AP  ·  AFP  ·  UN News  ·  FTC  ·  NDTV"
    d.text((12, 1006), src, font=sf, fill=MUTED)


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    header(d)
    hero(d)
    cards(d)
    footer(d)
    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print("wrote", out)
