from PIL import Image, ImageDraw
import random

# Create a more realistic food image
img = Image.new('RGB', (512, 512), (240, 240, 240))
d = ImageDraw.Draw(img)

# Draw a plate (circular)
plate_color = (250, 245, 230)
d.ellipse((80, 80, 430, 430), fill=plate_color, outline=(180, 170, 160), width=4)

# Add plate rim
for i in range(80, 430, 15):
    d.line([(i, 80), (i+5, 75)], fill=(200, 190, 180), width=1)

# Draw pasta/noodles (tan/brown)
noodle_color = (220, 180, 100)
for y in range(120, 380, 8):
    for x in range(120, 380, 15):
        d.line([(x + random.randint(-5, 5), y), (x + random.randint(20, 40), y + random.randint(2, 6))], fill=noodle_color, width=3)

# Draw tomato sauce puddles (red)
sauce_color = (200, 60, 40)
d.ellipse((150, 180, 220, 240), fill=sauce_color, outline=(150, 40, 20), width=2)
d.ellipse((250, 200, 320, 260), fill=sauce_color, outline=(150, 40, 20), width=2)
d.ellipse((180, 300, 260, 350), fill=sauce_color, outline=(150, 40, 20), width=2)

# Add some green vegetables (basil-like)
green_color = (80, 160, 60)
for pos in [(200, 150), (280, 220), (240, 300), (160, 280)]:
    d.ellipse((pos[0]-15, pos[1]-10, pos[0]+15, pos[1]+10), fill=green_color)

# Add some parmesan (white/yellow spots)
cheese_color = (240, 220, 160)
for _ in range(30):
    rx = random.randint(130, 380)
    ry = random.randint(130, 380)
    d.ellipse((rx, ry, rx+8, ry+8), fill=cheese_color)

# Save the image
img.save(r'D:\MessFoodLens\MessFoodLens\sample_food.png')
print("Created realistic pasta image: sample_food.png")
