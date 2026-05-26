from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1284, 2778
BG   = (10, 12, 16)
BG2  = (19, 22, 31)
GOLD = (201, 168, 76)
GOLD2= (232, 201, 106)
TEAL = (0, 201, 167)
TEXT = (244, 241, 232)
DIM  = (100, 96, 82)
DIM2 = (60, 58, 50)
BORDER = (40, 44, 58)

OUT = "/Users/besonnet.kl2/noor-ios/screenshots"
os.makedirs(OUT, exist_ok=True)

def font(size, bold=False):
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFNSText.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            pass
    return ImageFont.load_default()

def canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def centered(d, text, y, f, color=TEXT):
    bb = d.textbbox((0, 0), text, font=f)
    x = (W - (bb[2] - bb[0])) // 2
    d.text((x, y), text, fill=color, font=f)

def draw_ring(d, cx, cy, r, pct, color=GOLD):
    circ = 2 * math.pi * r
    # background ring
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=BORDER, width=10)
    # filled arc
    steps = 360
    filled = int(steps * pct)
    for i in range(filled):
        angle = math.radians(i - 90)
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        t = i / steps
        rc = int(GOLD[0] * (1-t) + TEAL[0] * t * 0.3 + GOLD[0] * 0.7)
        gc = int(GOLD[1] * (1-t) + TEAL[1] * t * 0.3 + GOLD[1] * 0.7)
        bc = int(GOLD[2] * (1-t) + TEAL[2] * t * 0.3 + GOLD[2] * 0.7)
        d.ellipse([x-5, y-5, x+5, y+5], fill=(rc, gc, bc))

def pill_row(d, text, y, active=False):
    f = font(36)
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    px, py = 36, 18
    x0 = (W - tw - px*2) // 2
    x1 = x0 + tw + px*2
    fill = GOLD if active else BG2
    tcol = BG if active else DIM
    d.rounded_rectangle([x0, y, x1, y+tw//2+py*2+4], radius=16, fill=fill, outline=BORDER, width=1)
    d.text((x0+px, y+py), text, fill=tcol, font=f)


# ── Screenshot 1: Hero — Dhikr Counter ───────────────────────────────────────
img, d = canvas()

# top bar
d.text((60, 120), "NOOR", fill=GOLD, font=font(52))
d.text((60, 185), "DHIKR", fill=DIM, font=font(28))

# arabic text centered
centered(d, "سُبْحَانَ اللهِ", 340, font(80), TEXT)
centered(d, "Subhan Allah", 450, font(40), DIM)
centered(d, "Glory be to Allah", 510, font(34), DIM2)

# ring
cx, cy = W//2, 900
r = 240
draw_ring(d, cx, cy, r, 0.72, GOLD)
# count inside
centered(d, "24", cy - 60, font(130), TEXT)
centered(d, "of 33", cy + 80, font(40), DIM)

# tap button
bx0, by0 = 100, 1260
bx1, by1 = W - 100, 1380
d.rounded_rectangle([bx0, by0, bx1, by1], radius=20, fill=GOLD)
centered(d, "Tap", 1292, font(64), BG)

# switcher pills
dhikrs = ["سبحان الله", "الحمد لله", "الله أكبر", "لا إله إلا الله"]
x = 60
y = 1420
for i, dh in enumerate(dhikrs):
    f = font(32)
    bb = d.textbbox((0, 0), dh, font=f)
    tw = bb[2] - bb[0]
    px = 28
    x1 = x + tw + px*2
    active = i == 0
    d.rounded_rectangle([x, y, x1, y+80], radius=14,
                         fill=GOLD if active else BG2,
                         outline=BORDER, width=1)
    d.text((x+px, y+18), dh, fill=BG if active else DIM, font=f)
    x = x1 + 16

# bottom nav
nav_y = H - 200
d.rectangle([0, nav_y, W, H], fill=(10, 12, 16))
d.line([0, nav_y, W, nav_y], fill=BORDER, width=1)
tabs = [("📿", "DHIKR", True), ("📖", "DUA", False), ("✦", "REFLECT", False), ("⭐", "WINS", False)]
tw = W // len(tabs)
for i, (icon, label, active) in enumerate(tabs):
    tx = i * tw + tw // 2
    col = GOLD if active else DIM2
    centered(d, icon, nav_y + 20, font(44), col)
    centered_x = i * tw
    bb = d.textbbox((0,0), label, font=font(24))
    lw = bb[2] - bb[0]
    d.text((centered_x + (tw - lw)//2, nav_y + 78), label, fill=col, font=font(24))

img.save(f"{OUT}/01_hero.png")
print("✓ 01_hero.png")


# ── Screenshot 2: Dua Library ─────────────────────────────────────────────────
img, d = canvas()

centered(d, "DUA LIBRARY", 160, font(80), TEXT)
centered(d, "Duas for every moment", 270, font(44), DIM)

categories = [
    ("Anxiety",     "حَسْبُنَا اللهُ وَنِعْمَ الْوَكِيلُ",  "Allah is sufficient for us"),
    ("Morning",     "اللَّهُمَّ بِكَ أَصْبَحْنَا",            "O Allah, by You we enter morning"),
    ("Gratitude",   "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "All praise is due to Allah"),
    ("Travel",      "سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا",  "Glory to Him who made this easy"),
]

y = 420
for cat, ar, meaning in categories:
    d.rounded_rectangle([60, y, W-60, y+200], radius=20, fill=BG2, outline=BORDER, width=1)
    d.text((88, y+18), cat.upper(), fill=GOLD, font=font(30))
    bb = d.textbbox((0,0), ar, font=font(38))
    aw = bb[2]-bb[0]
    d.text((W-60-aw-28, y+60), ar, fill=TEXT, font=font(38))
    d.text((88, y+148), meaning, fill=DIM, font=font(30))
    y += 228

# privacy badge
d.rounded_rectangle([200, y+40, W-200, y+130], radius=20, fill=BG2, outline=BORDER, width=1)
centered(d, "All offline. No account needed.", y+68, font(34), DIM)

# bottom nav
nav_y = H - 200
d.rectangle([0, nav_y, W, H], fill=BG)
d.line([0, nav_y, W, nav_y], fill=BORDER, width=1)
tabs = [("📿", "DHIKR", False), ("📖", "DUA", True), ("✦", "REFLECT", False), ("⭐", "WINS", False)]
tw = W // len(tabs)
for i, (icon, label, active) in enumerate(tabs):
    col = GOLD if active else DIM2
    bb = d.textbbox((0,0), icon, font=font(44))
    iw = bb[2]-bb[0]
    d.text((i*tw + (tw-iw)//2, nav_y+20), icon, fill=col, font=font(44))
    bb = d.textbbox((0,0), label, font=font(24))
    lw = bb[2]-bb[0]
    d.text((i*tw + (tw-lw)//2, nav_y+78), label, fill=col, font=font(24))

img.save(f"{OUT}/02_channels.png")
print("✓ 02_channels.png")


# ── Screenshot 3: Reflect ─────────────────────────────────────────────────────
img, d = canvas()

centered(d, "✦  REFLECT", 160, font(80), GOLD)
centered(d, "Your private daily journal", 270, font(44), DIM)

# journal card
d.rounded_rectangle([60, 360, W-60, 760], radius=24, fill=BG2, outline=BORDER, width=1)
d.text((100, 400), "Today's Intention", fill=GOLD, font=font(34))
d.text((100, 460), "Make my work a form of worship.\nHelp me stay focused on what matters.", fill=TEXT, font=font(38))
d.text((100, 620), "26 May 2026", fill=DIM, font=font(28))

# wins section
d.rounded_rectangle([60, 800, W-60, 1000], radius=24, fill=BG2, outline=BORDER, width=1)
d.text((100, 840), "⭐  Today's Wins", fill=GOLD, font=font(34))
d.text((100, 900), "✓  Fajr on time     ✓  Read Quran     ✓  helped a friend", fill=TEXT, font=font(32))

# privacy note
centered(d, "Private. Local. Yours.", 1080, font(52), TEXT)
centered(d, "Nothing ever leaves your device.", 1154, font(38), DIM)

d.rounded_rectangle([200, 1220, W-200, 1320], radius=20, fill=BG2, outline=BORDER, width=1)
centered(d, "No cloud. No account. No tracking.", 1248, font(34), DIM)

# bottom nav
nav_y = H - 200
d.rectangle([0, nav_y, W, H], fill=BG)
d.line([0, nav_y, W, nav_y], fill=BORDER, width=1)
tabs = [("📿", "DHIKR", False), ("📖", "DUA", False), ("✦", "REFLECT", True), ("⭐", "WINS", False)]
tw = W // len(tabs)
for i, (icon, label, active) in enumerate(tabs):
    col = GOLD if active else DIM2
    bb = d.textbbox((0,0), icon, font=font(44))
    iw = bb[2]-bb[0]
    d.text((i*tw + (tw-iw)//2, nav_y+20), icon, fill=col, font=font(44))
    bb = d.textbbox((0,0), label, font=font(24))
    lw = bb[2]-bb[0]
    d.text((i*tw + (tw-lw)//2, nav_y+78), label, fill=col, font=font(24))

img.save(f"{OUT}/03_visualizer.png")
print("✓ 03_visualizer.png")


# ── Screenshot 4: No BS ───────────────────────────────────────────────────────
img, d = canvas()

centered(d, "BUILT FOR MUSLIMS", 260, font(80), TEXT)
centered(d, "Not for your data.", 380, font(60), GOLD)

facts = [
    ("📵", "No account required"),
    ("🔒", "All data stays on your iPhone"),
    ("✈️",  "Works fully offline"),
    ("🚫", "No ads. No subscriptions."),
]
y = 580
for icon, text in facts:
    d.rounded_rectangle([80, y, W-80, y+140], radius=22, fill=BG2, outline=BORDER, width=1)
    d.text((130, y+38), icon, fill=GOLD, font=font(52))
    d.text((240, y+46), text, fill=TEXT, font=font(48))
    y += 168

centered(d, "PAY ONCE. REMEMBER ALWAYS.", H-480, font(52), GOLD)
centered(d, "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ", H-390, font(52), DIM)
centered(d, "Built by Architect-DNA · Bern, Switzerland", H-290, font(34), DIM2)

img.save(f"{OUT}/04_nobs.png")
print("✓ 04_nobs.png")

print(f"\nAll screenshots → {OUT}/")
