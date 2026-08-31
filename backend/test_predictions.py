from model import FoodClassifier
from PIL import Image

classifier = FoodClassifier()
img = Image.open(r'D:\MessFoodLens\MessFoodLens\sample_food.png')

result = classifier.predict(img)

print("Prediction result:")
print(f"  Success: {result['success']}")
print(f"  Food: {result.get('food', 'N/A')}")
print(f"  Confidence: {result.get('confidence', 'N/A')}%")
print(f"  Message: {result.get('message', 'N/A')}")
print(f"\nTop predictions:")
for label_info in result.get('raw_labels', []):
    print(f"  {label_info.get('label', 'unknown')}: {label_info.get('confidence', 0)}%")

