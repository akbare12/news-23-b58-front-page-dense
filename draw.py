#!/usr/bin/env python3
"""news-23 b58 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
DRED = (139, 0, 0)
BLUE = (20, 60, 140)
TEAL = (0, 128, 128)
GREEN = (34, 139, 34)
PURPLE = (128, 0, 128)
BROWN = (139, 90, 0)
GRAY = (110, 110, 110)
LGRAY = (230, 230, 230)
CREAM = (250, 244, 220)
NAVY = (10, 25, 60)

def text(x, y, s, font, fill=BLACK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, kind):
    # chip drawn right-aligned ending at x, top y, height 13
    f = F(SANS_B, 9)
    w = int(d.textlength(label, font=f)) + 10
    col = BLUE if kind == "REPORTED" else RED
    d.rectangle([x - w, y, x, y + 13], fill=col)
    d.text((x - w + 5, y + 1), label, font=f, fill=WHITE)
    return w

# ---------- masthead ----------
d.rectangle([0, 0, W, 58], fill=BLACK)
text(12, 6, "THE WORLD TODAY", F(SERIF_B, 44), WHITE)
text(1012, 20, "MONDAY 23 NOVEMBER 2026", F(SANS_B, 17), GOLD, anchor="ra")

# ---------- kicker ----------
text(12, 63, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     F(SANS_B, 13), RED)

# ---------- number strip (2 rows x 5 cols) ----------
strip = [
    [("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", BLUE), ("11,762", "EBOLA CASES, DRC", GREEN),
     ("10T won", "SEOUL STABILISATION FUND", BROWN), ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE)],
    [("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES/WEEK", RED), ("12,000", "CLEARED IN MANCHESTER", BLUE),
     ("264 kg", "EXPLOSIVES IN LEBANON", BROWN), ("$107.3B", "ANTHROPIC IPO", PURPLE)],
]
xs = [12, 214, 416, 618, 820]
fnum, flab = F(SANS_B, 18), F(SANS_B, 10)
for r, row in enumerate(strip):
    ny = 80 + r * 30
    for c, (num, lab, col) in enumerate(row):
        text(xs[c], ny, num, fnum, col)
        text(xs[c], ny + 20, lab, flab, BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", 7, (0, 128, 128)), ("AMERICAS 8", 8, (20, 90, 200)),
           ("MIDDLE EAST 6", 6, (200, 160, 20)), ("EUROPE 5", 5, (128, 0, 128)),
           ("AFRICA 3", 3, (200, 40, 40)), ("WORLD 2", 2, (110, 110, 110))]
rx = 0
for name, n, col in regions:
    w = int(round(n / 31 * W))
    d.rectangle([rx, 140, rx + w, 156], fill=col)
    text(rx + w / 2, 143, name, F(SANS_B, 11), WHITE, anchor="ma")
    rx += w

# ---------- UTC strip ----------
text(12, 160, "THE DAY IN UTC  ~00:00 Kospi dives  ~06:30 Guterres opens  ~09:00 Power Index  ~12:00 Paris 2% tax  ~15:00 Kyiv missiles",
     F(SANS, 10), BLACK)
text(1012, 160, "~ APPROX", F(SANS, 10), GRAY, anchor="ra")

# ---------- hero scenes ----------
HX = [12, 349, 686]
HW = 326
SY, SH = 176, 128

# scene 1: Kospi chart + solid skyline
d.rectangle([HX[0], SY, HX[0] + HW, SY + SH], fill=NAVY)
# solid buildings with lit windows
import random
random.seed(23)
bx = HX[0] + 8
while bx < HX[0] + HW - 20:
    bw = random.randint(18, 30)
    bh = random.randint(28, 62)
    d.rectangle([bx, SY + SH - 22 - bh, bx + bw, SY + SH - 22], fill=(24, 48, 96))
    for wy in range(SY + SH - 22 - bh + 5, SY + SH - 26, 9):
        for wx in range(bx + 4, bx + bw - 3, 8):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
    bx += bw + 4
# chart line
pts = [(HX[0] + 14, SY + 52), (HX[0] + 60, SY + 30), (HX[0] + 105, SY + 58),
       (HX[0] + 150, SY + 26), (HX[0] + 200, SY + 44), (HX[0] + 250, SY + 18),
       (HX[0] + 300, SY + 34)]
d.line(pts, fill=(255, 170, 40), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 200, 90), outline=(255, 170, 40))
text(HX[0] + 10, SY + 4, "-3.3%", F(SANS_B, 26), RED)
d.rectangle([HX[0], SY + SH - 22, HX[0] + HW, SY + SH], fill=BLACK)
text(HX[0] + 8, SY + SH - 19, "KOSPI 4,708.54   \u00b7   -161 PTS", F(SANS_B, 11), WHITE)

# scene 2: Guterres
d.rectangle([HX[1], SY, HX[1] + HW, SY + SH], fill=(0, 128, 120))
text(HX[1] + 12, SY + 10, "150 DELEGATES", F(SANS_B, 30), GOLD)
text(HX[1] + 12, SY + 44, "BACK A RISK", F(SANS_B, 30), GOLD)
text(HX[1] + 12, SY + 78, "FRAMEWORK", F(SANS_B, 30), GOLD)
cx, cy, r = HX[1] + HW - 52, SY + 88, 26
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
d.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=WHITE, width=1)
d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=1)
d.line([cx - r + 6, cy - 14, cx + r - 6, cy - 14], fill=WHITE, width=1)
d.line([cx - r + 6, cy + 14, cx + r - 6, cy + 14], fill=WHITE, width=1)
d.rectangle([HX[1], SY + SH - 22, HX[1] + HW, SY + SH], fill=BLACK)
text(HX[1] + 8, SY + SH - 19, "UN   \u00b7   BRIDGETOWN", F(SANS_B, 11), WHITE)

# scene 3: Power Index bars
d.rectangle([HX[2], SY, HX[2] + HW, SY + SH], fill=CREAM)
text(HX[2] + 10, SY + 4, "NARROWEST SINCE 2018", F(SANS_B, 12), BLACK)
text(HX[2] + HW - 10, SY + 4, "GAP 5.3", F(SANS_B, 12), BROWN, anchor="ra")
bars = [("78.9", 70, (10, 25, 60), "US"), ("73.6", 64, (178, 34, 34), "CHINA"), ("40.5", 38, (184, 134, 11), "INDIA")]
base = SY + SH - 22
bx0 = HX[2] + 30
for i, (val, bh, col, lab) in enumerate(bars):
    x0 = bx0 + i * 100
    text(x0 + 26, base - bh - 20, val, F(SANS_B, 15), BLACK, anchor="ma")
    d.rectangle([x0, base - bh, x0 + 52, base], fill=col)
    text(x0 + 26, base - bh + (bh - 12) // 2, lab, F(SANS_B, 11), WHITE, anchor="ma")
d.rectangle([HX[2], SY + SH - 22, HX[2] + HW, SY + SH], fill=BLACK)
text(HX[2] + 8, SY + SH - 19, "ASIA POWER INDEX 2026", F(SANS_B, 11), WHITE)

# ---------- hero text ----------
heroes = [
    ("1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS"),
    ("3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
fhead, fbody, fsrc = F(SERIF_B, 17), F(SANS, 11), F(SANS, 10)
for i, (num, head, body, src) in enumerate(heroes):
    x = HX[i]
    d.ellipse([x, 314, x + 18, 332], fill=RED)
    d.text((x + 9, 315), num, font=F(SANS_B, 11), fill=WHITE, anchor="ma")
    hl = wrap(head, fhead, HW - 24)
    hy = 312
    for ln in hl[:2]:
        text(x + 24, hy, ln, fhead, BLACK)
        hy += 19
    bl = wrap(body, fbody, HW - 4)
    by = 352
    for ln in bl[:2]:
        text(x, by, ln, fbody, BLACK)
        by += 14
    text(x, 380, src, fsrc, GRAY)
    chip(x + HW, 378, "REPORTED", "REPORTED")

# ---------- MORE OF THE DAY bar ----------
d.rectangle([0, 398, W, 416], fill=BLACK)
text(12, 401, "MORE OF THE DAY  \u2014  10 STORIES", F(SANS_B, 13), WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", BLUE, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", RED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", BROWN, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", BLUE, "US FUTURES JUMP 3%", "Futures up 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "States sue over AI claims.", "AP", "REPORTED"),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "$83 raise; $97.17 close.", "WSJ", "REPORTED"),
    ("EUROPE", PURPLE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", GRAY, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CX = [12, 214, 416, 618, 820]
CW = 192
fcat, fch, fcb = F(SANS_B, 10), F(SANS_B, 12), F(SANS, 10)
for idx, (cat, col, head, body, src, kind) in enumerate(cards):
    r, c = divmod(idx, 5)
    x = CX[c]
    y = 420 + r * 72
    d.rectangle([x, y, x + CW, y + 15], fill=col)
    text(x + 4, y + 2, cat, fcat, WHITE)
    text(x + CW - 4, y + 2, str(idx + 1), fcat, WHITE, anchor="ra")
    hl = wrap(head, fch, CW - 8)
    hy = y + 17
    for ln in hl[:2]:
        text(x + 2, hy, ln, fch, BLACK)
        hy += 14
    text(x + 2, y + 45, body, fcb, BLACK)
    text(x + 2, y + 59, src, fcb, GRAY)
    chip(x + CW, y + 57, kind, kind)

# ---------- map + ALSO header ----------
d.rectangle([0, 568, W, 586], fill=BLACK)
text(12, 571, "WHERE IT HAPPENED", F(SANS_B, 13), WHITE)
text(330, 571, "ALSO ON MONDAY", F(SANS_B, 13), WHITE)

# ---------- map ----------
d.rectangle([12, 590, 318, 884], fill=(245, 245, 240))
for gx in range(12, 319, 24):
    d.line([gx, 590, gx, 884], fill=(225, 225, 220), width=1)
for gy in range(590, 885, 24):
    d.line([12, gy, 318, gy], fill=(225, 225, 220), width=1)
d.ellipse([20, 620, 180, 800], fill=(190, 220, 170))
d.ellipse([150, 600, 310, 790], fill=(190, 220, 170))
d.ellipse([60, 800, 200, 880], fill=(190, 220, 170))
pins = [(272, 605), (58, 792), (288, 640), (78, 705), (108, 668), (218, 748),
        (52, 645), (28, 755), (72, 812), (150, 824), (190, 620), (205, 665), (240, 600)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=1)
    d.text((px, py - 6), str(i), font=F(SANS_B, 10), fill=WHITE, anchor="ma")
fleg = F(SANS, 9)
text(16, 848, "Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing", fleg, BLACK)
text(16, 861, "4 Washington  \u00b7  5 New York  \u00b7  6 Tehran  \u00b7  7 Chicago", fleg, BLACK)
text(16, 874, "8 SF  \u00b7  9 Denver  \u00b7  10 Austin  \u00b7  11 Warsaw  \u00b7  12 Kyiv  \u00b7  13 Moscow", fleg, BLACK)

# ---------- ALSO list ----------
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
falt = F(SANS, 11)
for i, item in enumerate(also):
    col = 330 if i < 9 else 680
    row = i % 9
    text(col, 596 + row * 32, item, falt, BLACK)

# ---------- DATE CHECK ----------
d.rectangle([12, 892, 1012, 958], outline=RED, width=2)
text(16, 896, "DATE CHECK", F(SANS_B, 13), RED)
text(1008, 897, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", F(SANS_B, 9), RED, anchor="ra")
fdc = F(SANS, 11)
text(16, 916, "LEFT OUT \u2014 NOT 23 NOV:  Democrats reach 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)  \u00b7", fdc, BLACK)
text(16, 930, "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)", fdc, BLACK)
text(16, 944, "NOT YET:  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff", fdc, BLACK)

# ---------- footer ----------
ff = F(SANS, 9)
text(12, 964, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", ff, GRAY)
text(12, 976, "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", ff, GRAY)
text(12, 988, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", ff, GRAY)

# ---------- bottom bar ----------
d.rectangle([0, 1000, W, H], fill=BLACK)
text(W // 2, 1006, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions", F(SANS_B, 13), GOLD, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
