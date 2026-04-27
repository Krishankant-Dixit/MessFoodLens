"""
Nutrition data dictionary for common food items.
Values are per standard serving size.
"""

NUTRITION_DATA = {
    "pizza": {
        "calories": 285,
        "protein": "12g",
        "carbs": "36g",
        "fats": "10g",
        "fiber": "2g",
        "serving": "1 slice (107g)",
        "meal_quality_score": 55,
    },
    "burger": {
        "calories": 354,
        "protein": "20g",
        "carbs": "29g",
        "fats": "17g",
        "fiber": "1g",
        "serving": "1 burger (150g)",
        "meal_quality_score": 45,
    },
    "rice": {
        "calories": 130,
        "protein": "2g",
        "carbs": "28g",
        "fats": "0g",
        "fiber": "0g",
        "serving": "1 cup cooked (186g)",
        "meal_quality_score": 70,
    },
    "pasta": {
        "calories": 220,
        "protein": "8g",
        "carbs": "43g",
        "fats": "1g",
        "fiber": "3g",
        "serving": "1 cup cooked (140g)",
        "meal_quality_score": 65,
    },
    "salad": {
        "calories": 20,
        "protein": "1g",
        "carbs": "3g",
        "fats": "0g",
        "fiber": "2g",
        "serving": "1 cup (67g)",
        "meal_quality_score": 95,
    },
    "sandwich": {
        "calories": 250,
        "protein": "11g",
        "carbs": "33g",
        "fats": "8g",
        "fiber": "2g",
        "serving": "1 sandwich (130g)",
        "meal_quality_score": 60,
    },
    "sushi": {
        "calories": 200,
        "protein": "9g",
        "carbs": "38g",
        "fats": "1g",
        "fiber": "1g",
        "serving": "6 pieces (156g)",
        "meal_quality_score": 80,
    },
    "steak": {
        "calories": 271,
        "protein": "26g",
        "carbs": "0g",
        "fats": "18g",
        "fiber": "0g",
        "serving": "3 oz (85g)",
        "meal_quality_score": 65,
    },
    "soup": {
        "calories": 80,
        "protein": "4g",
        "carbs": "12g",
        "fats": "2g",
        "fiber": "2g",
        "serving": "1 cup (240ml)",
        "meal_quality_score": 75,
    },
    "chicken": {
        "calories": 165,
        "protein": "31g",
        "carbs": "0g",
        "fats": "4g",
        "fiber": "0g",
        "serving": "3 oz (85g)",
        "meal_quality_score": 85,
    },
    "fish": {
        "calories": 140,
        "protein": "28g",
        "carbs": "0g",
        "fats": "3g",
        "fiber": "0g",
        "serving": "3 oz (85g)",
        "meal_quality_score": 90,
    },
    "hot dog": {
        "calories": 190,
        "protein": "7g",
        "carbs": "2g",
        "fats": "17g",
        "fiber": "0g",
        "serving": "1 frank (57g)",
        "meal_quality_score": 35,
    },
    "french fries": {
        "calories": 312,
        "protein": "3g",
        "carbs": "41g",
        "fats": "15g",
        "fiber": "4g",
        "serving": "medium (117g)",
        "meal_quality_score": 30,
    },
    "ice cream": {
        "calories": 207,
        "protein": "4g",
        "carbs": "25g",
        "fats": "11g",
        "fiber": "0g",
        "serving": "1 cup (132g)",
        "meal_quality_score": 25,
    },
    "apple pie": {
        "calories": 411,
        "protein": "4g",
        "carbs": "58g",
        "fats": "19g",
        "fiber": "2g",
        "serving": "1 slice (155g)",
        "meal_quality_score": 30,
    },
    "donut": {
        "calories": 253,
        "protein": "3g",
        "carbs": "29g",
        "fats": "14g",
        "fiber": "1g",
        "serving": "1 medium (60g)",
        "meal_quality_score": 20,
    },
    "waffles": {
        "calories": 218,
        "protein": "6g",
        "carbs": "33g",
        "fats": "8g",
        "fiber": "1g",
        "serving": "2 waffles (140g)",
        "meal_quality_score": 40,
    },
    "pancakes": {
        "calories": 227,
        "protein": "6g",
        "carbs": "38g",
        "fats": "7g",
        "fiber": "1g",
        "serving": "2 medium (136g)",
        "meal_quality_score": 45,
    },
    "omelette": {
        "calories": 154,
        "protein": "11g",
        "carbs": "1g",
        "fats": "12g",
        "fiber": "0g",
        "serving": "2-egg omelette (130g)",
        "meal_quality_score": 75,
    },
    "fried rice": {
        "calories": 238,
        "protein": "5g",
        "carbs": "40g",
        "fats": "7g",
        "fiber": "1g",
        "serving": "1 cup (198g)",
        "meal_quality_score": 55,
    },
    "tacos": {
        "calories": 226,
        "protein": "9g",
        "carbs": "20g",
        "fats": "12g",
        "fiber": "3g",
        "serving": "2 tacos (128g)",
        "meal_quality_score": 55,
    },
    "nachos": {
        "calories": 346,
        "protein": "9g",
        "carbs": "36g",
        "fats": "19g",
        "fiber": "4g",
        "serving": "1 serving (113g)",
        "meal_quality_score": 35,
    },
}

# Fallback nutrition for unrecognised foods
UNKNOWN_NUTRITION = {
    "calories": 0,
    "protein": "N/A",
    "carbs": "N/A",
    "fats": "N/A",
    "fiber": "N/A",
    "serving": "N/A",
    "meal_quality_score": 0,
}


def get_nutrition(food_label: str) -> dict:
    """
    Return nutrition data for the given food label.
    Performs a case-insensitive lookup, then partial-match fallback.
    """
    label_lower = food_label.lower().strip()

    # Exact match
    if label_lower in NUTRITION_DATA:
        return {"food": food_label, **NUTRITION_DATA[label_lower]}

    # Partial match (e.g. "cheese pizza" → "pizza")
    for key in NUTRITION_DATA:
        if key in label_lower or label_lower in key:
            return {"food": food_label, **NUTRITION_DATA[key]}

    # Fallback
    return {"food": food_label, **UNKNOWN_NUTRITION}
