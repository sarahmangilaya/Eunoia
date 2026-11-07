from PIL import Image

im = Image.open('C:/Users/JM/.gemini/antigravity/brain/d4ca79f1-1cf2-4e33-af91-640fdd922b66/eunoia_card_front_1794066280993.jpg')
print("front size:", im.size)
# Sample pixels at corners and center
print("top-left (10, 10):", im.getpixel((10, 10)))
print("center (w/2, h/2):", im.getpixel((im.size[0]//2, im.size[1]//2)))

# Scan along horizontal center
w, h = im.size
row = [im.getpixel((x, h//2)) for x in range(0, w, 20)]
print("row sample (every 20px):", [(i*20, p) for i, p in enumerate(row[:15])])

