from PIL import Image

def find_card_bounds(im):
    w, h = im.size
    # Card is emerald green (g > r + 10 or gold rim r > 120 and b < 100)
    # Neutral grey backdrop has abs(r - g) <= 5 and abs(g - b) <= 5
    def is_card_pixel(p):
        r, g, b = p[:3]
        # emerald interior:
        if g > r + 8 and g > b:
            return True
        # gold border:
        if r > 110 and g > 90 and b < 90:
            return True
        # very dark interior of card:
        if r < 10 and g < 35 and b < 30 and (g > r or b > r):
            return True
        return False

    center_y = h // 2
    xs = [x for x in range(w) if is_card_pixel(im.getpixel((x, center_y)))]
    
    center_x = w // 2
    ys = [y for y in range(h) if is_card_pixel(im.getpixel((center_x, y)))]
    
    return min(xs), min(ys), max(xs), max(ys)

im_front = Image.open('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/eunoia_card_front_1794066280993.jpg')
bounds_front = find_card_bounds(im_front)
print("Front bounds:", bounds_front, "size:", bounds_front[2]-bounds_front[0], "x", bounds_front[3]-bounds_front[1])

im_back = Image.open('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/eunoia_card_back_1794066299362.jpg')
bounds_back = find_card_bounds(im_back)
print("Back bounds:", bounds_back, "size:", bounds_back[2]-bounds_back[0], "x", bounds_back[3]-bounds_back[1])

# Crop both with a tiny 2px inset so no grey fringe is visible:
crop_f = im_front.crop((bounds_front[0]+2, bounds_front[1]+2, bounds_front[2]-2, bounds_front[3]-2))
crop_f.save('assets/concierge/eunoia_card_front.png')
print("Saved perfect front crop:", crop_f.size)

crop_b = im_back.crop((bounds_back[0]+2, bounds_back[1]+2, bounds_back[2]-2, bounds_back[3]-2))
crop_b.save('assets/concierge/eunoia_card_back.png')
print("Saved perfect back crop:", crop_b.size)
