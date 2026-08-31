from PIL import Image, ImageDraw
import random

# Create a realistic-looking pizza image
img = Image.new('RGB', (400, 400), (240, 235, 225))
d = ImageDraw.Draw(img)

# Draw plate rim
d.ellipse((30, 30, 370, 370), outline=(200, 180, 150), width=8)

# Draw pizza/bread base (tan/brown)
d.ellipse((50, 50, 350, 350), fill=(220, 160, 80), outline=(180, 120, 40), width=2)

# Add pizza texture (slightly darker patches)
for _ in range(40):
    x = random.randint(80, 320)
    y = random.randint(80, 320)
    d.ellipse((x, y, x+15, y+15), fill=(200, 140, 60))

# Add tomato sauce (red spots)
sauce_points = [(120, 120), (280, 150), (200, 250), (150, 280), (300, 280), (250, 120)]
for px, py in sauce_points:
    d.ellipse((px-20, py-20, px+20, py+20), fill=(200, 60, 40))

# Add cheese (yellow/white spots)
for _ in range(50):
    x = random.randint(100, 300)
    y = random.randint(100, 300)
    d.ellipse((x, y, x+12, y+12), fill=(240, 220, 100))

# Add basil/vegetable (green)
green_spots = [(140, 160), (250, 200), (180, 280), (300, 150), (120, 240)]
for px, py in green_spots:
    d.ellipse((px-15, py-15, px+15, py+15), fill=(60, 150, 40))
    
# Add some black pepper/spice
for _ in range(20):
    x = random.randint(100, 300)
    y = random.randint(100, 300)
    d.point((x, y), fill=(30, 30, 30))

img.save(r'D:\MessFoodLens\MessFoodLens\sample_food.png')
print("Created pizza-like image")
