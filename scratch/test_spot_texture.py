import math
from PIL import Image

def generate_gallery_wall_spot(width=512, height=1024):
    # Generates the exact scalloped gallery track light wall-wash seen in the reference photo.
    # The light originates from an angled ceiling track fixture ~1.8m in front of the wall.
    im = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = []
    
    # Apex of the scalloped arc near top (y ~ 120 / 1024)
    apex_y = 110.0
    
    for y in range(height):
        for x in range(width):
            nx = (x - width / 2.0) / (width / 2.0) # -1.0 to 1.0
            dy = (y - apex_y) # distance below apex
            
            if dy <= 0:
                # Above apex: smooth soft decay
                dist_above = -dy
                fade_above = max(0.0, 1.0 - (dist_above / 35.0))
                # very small glow near the apex center
                intensity = 0.05 * fade_above * max(0.0, 1.0 - abs(nx) * 3.0)
            else:
                # Below apex: conical / hyperbolic spread
                # Width increases with sqrt(dy) and linear dy
                spread = 0.22 + 0.026 * math.sqrt(dy * 12.0) + 0.00065 * dy
                norm_x = abs(nx) / spread
                
                if norm_x < 1.0:
                    # Smooth cosine beam profile
                    radial = math.pow(math.cos(norm_x * math.pi * 0.5), 1.4)
                    
                    # Vertical falloff:
                    # Rises quickly below apex, stays bright across the painting zone (y: 250-700),
                    # then smoothly tapers off towards the floor
                    if dy < 120.0:
                        vert = math.pow(dy / 120.0, 0.75)
                    else:
                        vert = math.pow(max(0.0, 1.0 - (dy - 120.0) / (height - apex_y - 120.0)), 1.25)
                    
                    # Core beam highlight
                    core_dist = math.hypot(nx * 1.5, (y - 380.0) / 280.0)
                    core_glow = math.pow(max(0.0, 1.0 - core_dist / 1.1), 1.8) * 0.45
                    
                    intensity = min(1.0, radial * vert * 0.85 + core_glow)
                else:
                    intensity = 0.0
            
            if intensity > 0.002:
                # Warm 3000K museum halogen spectrum
                # Bright warm white in core, soft amber at perimeter
                r = min(255, int(255 * intensity * 1.05))
                g = min(255, int(238 * (intensity * 0.96 + 0.04)))
                b = min(255, int(185 * (intensity * 0.65 + 0.05)))
                a = min(255, int(255 * math.pow(intensity, 1.1)))
                pixels.append((r, g, b, a))
            else:
                pixels.append((0, 0, 0, 0))
                
    im.putdata(pixels)
    im.save('scratch/gallery_spot_test.png')
    print("Saved scratch/gallery_spot_test.png successfully!")

generate_gallery_wall_spot()

