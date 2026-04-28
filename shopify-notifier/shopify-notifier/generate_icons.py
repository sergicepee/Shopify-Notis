#!/usr/bin/env python3
"""
generate_icons.py — genera los iconos PNG para la PWA
Uso: python3 generate_icons.py
Requiere: pip install Pillow
"""

import os
import struct
import zlib
import math

def create_shopify_icon_png(size):
    """Genera un icono PNG de Shopify puro en Python sin dependencias externas."""
    img = [[0, 0, 0, 0] for _ in range(size * size)]  # RGBA

    def px(x, y, r, g, b, a=255):
        if 0 <= x < size and 0 <= y < size:
            idx = y * size + x
            img[idx] = [r, g, b, a]

    def fill_circle(cx, cy, radius, r, g, b, a=255):
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                if dx*dx + dy*dy <= radius*radius:
                    px(cx+dx, cy+dy, r, g, b, a)

    def fill_rect(x1, y1, x2, y2, r, g, b, a=255):
        for y in range(y1, y2):
            for x in range(x1, x2):
                px(x, y, r, g, b, a)

    def fill_rounded_rect(x1, y1, x2, y2, rad, r, g, b, a=255):
        # Fill inner area
        fill_rect(x1+rad, y1, x2-rad, y2, r, g, b, a)
        fill_rect(x1, y1+rad, x2, y2-rad, r, g, b, a)
        # Corners
        fill_circle(x1+rad, y1+rad, rad, r, g, b, a)
        fill_circle(x2-rad, y1+rad, rad, r, g, b, a)
        fill_circle(x1+rad, y2-rad, rad, r, g, b, a)
        fill_circle(x2-rad, y2-rad, rad, r, g, b, a)

    s = size
    rad = int(s * 0.18)

    # Background: Shopify green #95bf47
    fill_rounded_rect(0, 0, s, s, rad, 149, 191, 71)

    # Bag body (white rounded rect)
    bx1 = int(s * 0.22)
    bx2 = int(s * 0.78)
    by1 = int(s * 0.45)
    by2 = int(s * 0.82)
    brad = max(4, int(s * 0.05))
    fill_rounded_rect(bx1, by1, bx2, by2, brad, 255, 255, 255)

    # Handle (white arc approximated as rounded rect with hole)
    hcx = s // 2
    hcy = int(s * 0.38)
    hrad_out = int(s * 0.15)
    hrad_in = int(s * 0.09)
    hthick = hrad_out - hrad_in

    for dy in range(-hrad_out, 1):
        for dx in range(-hrad_out, hrad_out+1):
            dist = math.sqrt(dx*dx + dy*dy)
            if hrad_in <= dist <= hrad_out:
                px(hcx+dx, hcy+dy, 255, 255, 255)

    # Letter S in green on white bag
    # Simple pixel S for small sizes
    cx = s // 2
    cy = int(s * 0.63)
    ts = max(6, int(s * 0.14))

    # Draw a simple "S" shape
    for y in range(cy - ts, cy + ts + 1):
        for x in range(cx - ts//2, cx + ts//2 + 1):
            ry = (y - cy) / ts
            rx = (x - cx) / (ts/2)
            # Top bar
            if abs(ry + 0.7) < 0.2 and rx < 0.4:
                px(x, y, 149, 191, 71)
            # Middle bar
            if abs(ry) < 0.2:
                px(x, y, 149, 191, 71)
            # Bottom bar
            if abs(ry - 0.7) < 0.2 and rx > -0.4:
                px(x, y, 149, 191, 71)
            # Left top curve
            if -0.9 < ry < -0.1 and abs(rx + 0.7) < 0.25:
                px(x, y, 149, 191, 71)
            # Right bottom curve
            if 0.1 < ry < 0.9 and abs(rx - 0.7) < 0.25:
                px(x, y, 149, 191, 71)

    # Convert to PNG bytes
    return encode_png(img, size, size)


def encode_png(pixels, width, height):
    def chunk(name, data):
        c = struct.pack('>I', len(data)) + name + data
        c += struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
        return c

    raw = b''
    for y in range(height):
        raw += b'\x00'
        for x in range(width):
            p = pixels[y * width + x]
            raw += bytes([p[0], p[1], p[2], p[3]])

    png = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    # Use RGBA (color type 6)
    ihdr = struct.pack('>II', width, height) + bytes([8, 6, 0, 0, 0])
    png += chunk(b'IHDR', ihdr)

    # Re-encode as RGBA
    raw = b''
    for y in range(height):
        raw += b'\x00'
        for x in range(width):
            p = pixels[y * width + x]
            raw += bytes([p[0], p[1], p[2], p[3]])

    compressed = zlib.compress(raw, 9)
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png


def create_with_pillow(size, out_path):
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Background: Shopify green
        rad = int(size * 0.18)
        draw.rounded_rectangle([0, 0, size, size], radius=rad, fill=(149, 191, 71, 255))

        # Bag body
        bx1, by1 = int(size*0.2), int(size*0.44)
        bx2, by2 = int(size*0.8), int(size*0.82)
        brad = max(4, int(size*0.05))
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=brad, fill=(255, 255, 255, 255))

        # Handle (arc)
        hcx = size // 2
        hcy_top = int(size * 0.22)
        hcy_bot = int(size * 0.50)
        hx1 = int(size * 0.32)
        hx2 = int(size * 0.68)
        draw.arc([hx1, hcy_top, hx2, hcy_bot], start=180, end=0,
                 fill=(255, 255, 255, 255), width=max(3, int(size*0.07)))

        # Text S
        cx = size // 2
        cy = int(size * 0.63)
        fs = max(12, int(size * 0.22))
        try:
            font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', fs)
        except:
            try:
                font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', fs)
            except:
                font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), 'S', font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw//2, cy - th//2 - bbox[1]), 'S', font=font, fill=(149, 191, 71, 255))

        img.save(out_path, 'PNG')
        return True
    except ImportError:
        return False


out_dir = os.path.join(os.path.dirname(__file__), 'public', 'icons')
os.makedirs(out_dir, exist_ok=True)

for size in [192, 512]:
    out_path = os.path.join(out_dir, f'icon-{size}.png')
    success = create_with_pillow(size, out_path)
    if success:
        print(f'Generated (Pillow): {out_path}')
    else:
        data = create_shopify_icon_png(size)
        with open(out_path, 'wb') as f:
            f.write(data)
        print(f'Generated (built-in): {out_path}')

print('Done!')
