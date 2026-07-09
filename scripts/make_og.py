#!/usr/bin/env python3
"""Genera la imagen Open Graph (1200x630) a partir de los assets del sitio."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H = 1200, 630
SAGE_DEEP = (45, 90, 71)
SAGE_DARK = (107, 158, 138)
CREAM = (250, 250, 248)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# --- Fondo: imagen del hero, difuminada y oscurecida con velo verde ---
bg = Image.open("assets/fondopsico.webp").convert("RGB")
bg = ImageOps.fit(bg, (W, H), method=Image.LANCZOS)
bg = bg.filter(ImageFilter.GaussianBlur(8))
# Velo verde para legibilidad
veil = Image.new("RGB", (W, H), SAGE_DEEP)
bg = Image.blend(bg, veil, 0.62)
canvas = bg.copy()
draw = ImageDraw.Draw(canvas)

# --- Foto circular a la derecha ---
photo = Image.open("assets/foto.webp").convert("RGB")
d = 300
photo = ImageOps.fit(photo, (d, d), method=Image.LANCZOS)
mask = Image.new("L", (d, d), 0)
ImageDraw.Draw(mask).ellipse((0, 0, d, d), fill=255)
px, py = W - d - 90, (H - d) // 2
# Anillo blanco
ring = 8
draw.ellipse((px - ring, py - ring, px + d + ring, py + d + ring), fill=WHITE)
canvas.paste(photo, (px, py), mask)

# --- Texto a la izquierda ---
x = 90
f_eyebrow = ImageFont.truetype(SANS_B, 26)
f_name = ImageFont.truetype(SERIF, 58)
f_role = ImageFont.truetype(SERIF_R, 34)
f_foot = ImageFont.truetype(SANS, 24)

# Eyebrow
draw.text((x, 150), "PSICOLOGÍA INFANTO-JUVENIL", font=f_eyebrow,
          fill=(200, 224, 213))
# Nombre (dos líneas)
draw.text((x, 200), "Lic. Julieta", font=f_name, fill=WHITE)
draw.text((x, 268), "Siganevich", font=f_name, fill=WHITE)
# Línea decorativa
draw.rounded_rectangle((x, 350, x + 90, 356), radius=3, fill=(168, 213, 194))
# Rol
draw.text((x, 378), "Terapia Cognitivo Conductual (TCC)", font=f_role, fill=(230, 240, 235))
draw.text((x, 418), "para niños y adolescentes", font=f_role, fill=(230, 240, 235))
# Footer / ubicación (con un punto dibujado en vez de emoji)
draw.ellipse((x, 508, x + 12, 520), fill=(168, 213, 194))
draw.text((x + 24, 500), "Caballito, CABA   ·   Turnos por WhatsApp",
          font=f_foot, fill=(200, 224, 213))

canvas.save("assets/og-image.jpg", "JPEG", quality=88, optimize=True)
print("assets/og-image.jpg", canvas.size)
