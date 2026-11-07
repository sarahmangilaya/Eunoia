import math
from PIL import Image

w, h = 512, 512
im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
pix = im.load()

# Apex of spotlight is near top of plane (on wall above frame)
lx, ly = 256.0, 30.0

for y in range(h):
    dy = y - ly
    for x in range(w):
        dx = x - lx
        
        intensity = 0.0
        if dy > -5.0:
            dist = math.hypot(dx, dy)
            # Beam half-angle ~ 48 degrees
            spread = 30.0 + dy * 0.72
            x_norm = abs(dx) / spread
            
            if x_norm < 1.0:
                # Cosine angular falloff
                fan = math.cos(x_norm * math.pi * 0.5) ** 1.3
                # Longitudinal falloff along the beam
                dist_taper = max(0.0, 1.0 - (dy / 490.0)) ** 1.15
                top_ease = min(1.0, (dy + 5.0) / 35.0)
                intensity = fan * dist_taper * top_ease
        
        # Generous warm glow centered on the artwork (dy around 160..280)
        d_art = math.hypot(dx * 0.9, (dy - 220.0) * 0.8)
        art_glow = max(0.0, 1.0 - d_art / 240.0) ** 1.6 * 0.55
        
        total = min(1.0, intensity * 0.75 + art_glow)
        if total > 0.005:
            # Radiant golden gallery lighting
            r = int(255 * min(1.0, total * 1.15))
            g = int(235 * min(1.0, total * 0.98 + 0.04))
            b = int(170 * min(1.0, total * 0.62 + 0.04))
            a = int(255 * (total ** 1.05))
            pix[x, y] = (r, g, b, a)

im.save('scratch/gallery_spot_perfect.png')
print('gallery_spot_perfect.png generated')

