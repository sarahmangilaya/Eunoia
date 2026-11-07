from PIL import Image

im = Image.open('assets/concierge/eunoia_card_back.png')
w, h = im.size
print("Card back size:", w, h)

# Let's inspect where gold pixels exist (r > 120, g > 90, b < 90)
# Top left corner:
tl_max_x, tl_max_y = 0, 0
for y in range(h // 3):
    for x in range(w // 3):
        r, g, b = im.getpixel((x, y))[:3]
        if r > 110 and g > 85 and b < 90:
            tl_max_x = max(tl_max_x, x)
            tl_max_y = max(tl_max_y, y)

print("Top-left gold filigree reaches x =", tl_max_x, f"({tl_max_x/w*100:.1f}%)", "y =", tl_max_y, f"({tl_max_y/h*100:.1f}%)")

# Bottom left corner:
bl_max_x, bl_min_y = 0, h
for y in range(2 * h // 3, h):
    for x in range(w // 3):
        r, g, b = im.getpixel((x, y))[:3]
        if r > 110 and g > 85 and b < 90:
            bl_max_x = max(bl_max_x, x)
            bl_min_y = min(bl_min_y, y)

print("Bottom-left gold filigree reaches x =", bl_max_x, f"({bl_max_x/w*100:.1f}%)", "y from bottom =", h - bl_min_y, f"({(h-bl_min_y)/h*100:.1f}%)")

