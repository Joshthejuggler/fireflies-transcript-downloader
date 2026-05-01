from PIL import Image, ImageDraw, ImageFilter
import math, random

SIZE = 1024
HALF = SIZE // 2

# ── Base image ────────────────────────────────────────────────────────────────
result = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

# ── Background: deep navy gradient ───────────────────────────────────────────
bg = Image.new('RGBA', (SIZE, SIZE))
bg_draw = ImageDraw.Draw(bg)
for y in range(SIZE):
    t = y / SIZE
    r = int(10  + t * 8)
    g = int(12  + t * 8)
    b = int(35  + t * 30)
    bg_draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))
result = Image.alpha_composite(result, bg)

# ── Glow halo around abdomen ──────────────────────────────────────────────────
glow = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
gd   = ImageDraw.Draw(glow)
cx, cy = HALF, HALF + 80
for i in range(18, 0, -1):
    alpha = int(18 * (1 - i / 18))
    rx, ry = 100 + i * 18, 70 + i * 13
    gd.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(160, 255, 60, alpha))
glow = glow.filter(ImageFilter.GaussianBlur(radius=22))
result = Image.alpha_composite(result, glow)

# ── Wings ─────────────────────────────────────────────────────────────────────
wing_layer = Image.new('RGBA', (SIZE, SIZE), (0,0,0,0))
wd = ImageDraw.Draw(wing_layer)

def draw_wing(draw, cx, cy, flip=1):
    pts = [
        (cx,        cy - 60),
        (cx + flip*220, cy - 200),
        (cx + flip*280, cy -  60),
        (cx + flip*200, cy +  60),
        (cx + flip*100, cy +  30),
    ]
    draw.polygon(pts, fill=(140, 200, 255, 55), outline=(170, 220, 255, 120))

draw_wing(wd, HALF, HALF - 80, flip=-1)   # left
draw_wing(wd, HALF, HALF - 80, flip=1)    # right
wing_layer = wing_layer.filter(ImageFilter.GaussianBlur(radius=2))
result = Image.alpha_composite(result, wing_layer)

# ── Body ──────────────────────────────────────────────────────────────────────
body = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
bd   = ImageDraw.Draw(body)

# head
bd.ellipse([HALF-42, HALF-195, HALF+42, HALF-125], fill=(38, 44, 65, 255))
# eyes
bd.ellipse([HALF-30, HALF-182, HALF-12, HALF-148], fill=(90, 200, 255, 230))
bd.ellipse([HALF+12, HALF-182, HALF+30, HALF-148], fill=(90, 200, 255, 230))
# thorax
bd.ellipse([HALF-62, HALF-130, HALF+62, HALF-20],  fill=(32, 38, 58, 255))
# abdomen – bright glow core
bd.ellipse([HALF-80, HALF-25,  HALF+80, HALF+145], fill=(195, 255, 65, 255))
# abdomen – darker tip
bd.ellipse([HALF-55, HALF+100, HALF+55, HALF+155], fill=(120, 200, 30, 255))
# abdomen stripe
bd.rectangle([HALF-78, HALF+55, HALF+78, HALF+70], fill=(140, 230, 40, 255))

result = Image.alpha_composite(result, body)

# ── Antennae ──────────────────────────────────────────────────────────────────
ant = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
ad  = ImageDraw.Draw(ant)
ad.line([(HALF-18, HALF-185), (HALF-80, HALF-280)], fill=(55, 65, 90, 255), width=6)
ad.line([(HALF+18, HALF-185), (HALF+80, HALF-280)], fill=(55, 65, 90, 255), width=6)
# tips glow
ad.ellipse([HALF-96, HALF-296, HALF-68, HALF-268], fill=(195, 255, 65, 200))
ad.ellipse([HALF+68, HALF-296, HALF+96, HALF-268], fill=(195, 255, 65, 200))
result = Image.alpha_composite(result, ant)

# ── Sparkles ──────────────────────────────────────────────────────────────────
sp = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
sd = ImageDraw.Draw(sp)
random.seed(7)
for _ in range(28):
    x = random.randint(30, SIZE-30)
    y = random.randint(30, SIZE-30)
    # keep sparkles away from center body
    if abs(x-HALF) < 160 and abs(y-HALF) < 250:
        continue
    r = random.randint(2, 7)
    a = random.randint(60, 180)
    sd.ellipse([x-r, y-r, x+r, y+r], fill=(200, 255, 100, a))
result = Image.alpha_composite(result, sp)

# ── Save 1024 master ──────────────────────────────────────────────────────────
out = '/sessions/lucid-bold-albattani/mnt/outputs/fireflies_icon_1024.png'
result.save(out)
print(f"Saved: {out}")
