"""Nutrition lookup data for supported foods.

The values are intentionally conservative estimates for a standard serving.
These numbers are meant for rough diet tracking and app demo purposes only.
"""

from __future__ import annotations

import re
from typing import Dict, Any

NUTRITION_DATA: Dict[str, Dict[str, Any]] = {
    # Fast Food & Burgers
    "pizza": {"calories": 285, "protein": 12, "carbs": 36, "fats": 10, "fiber": 2, "serving": "1 slice (107g)"},
    "burger": {"calories": 330, "protein": 18, "carbs": 28, "fats": 15, "fiber": 3, "serving": "1 burger (150g)"},
    "hot dog": {"calories": 250, "protein": 10, "carbs": 22, "fats": 12, "fiber": 1, "serving": "1 hot dog (90g)"},
    "french fries": {"calories": 320, "protein": 4, "carbs": 41, "fats": 15, "fiber": 4, "serving": "1 medium (117g)"},
    "fried chicken": {"calories": 320, "protein": 24, "carbs": 10, "fats": 20, "fiber": 0, "serving": "2 pieces (150g)"},
    
    # Breakfast
    "waffles": {"calories": 220, "protein": 6, "carbs": 28, "fats": 9, "fiber": 2, "serving": "2 waffles (100g)"},
    "pancakes": {"calories": 240, "protein": 7, "carbs": 31, "fats": 9, "fiber": 2, "serving": "2 pancakes (120g)"},
    "omelette": {"calories": 210, "protein": 14, "carbs": 2, "fats": 15, "fiber": 1, "serving": "1 omelette (120g)"},
    "cereal": {"calories": 150, "protein": 3, "carbs": 30, "fats": 2, "fiber": 3, "serving": "1 cup (40g)"},
    "toast": {"calories": 90, "protein": 3, "carbs": 17, "fats": 1, "fiber": 3, "serving": "1 slice (30g)"},
    "bread": {"calories": 90, "protein": 3, "carbs": 17, "fats": 1, "fiber": 3, "serving": "1 slice (30g)"},
    "bagel": {"calories": 210, "protein": 8, "carbs": 41, "fats": 2, "fiber": 2, "serving": "1 bagel (89g)"},
    
    # Protein
    "steak": {"calories": 350, "protein": 31, "carbs": 0, "fats": 22, "fiber": 0, "serving": "1 serving (150g)"},
    "chicken": {"calories": 320, "protein": 26, "carbs": 0, "fats": 23, "fiber": 0, "serving": "1 serving (150g)"},
    "fish": {"calories": 260, "protein": 22, "carbs": 0, "fats": 17, "fiber": 0, "serving": "1 fillet (150g)"},
    "salmon": {"calories": 280, "protein": 25, "carbs": 0, "fats": 18, "fiber": 0, "serving": "1 fillet (150g)"},
    "pork": {"calories": 310, "protein": 28, "carbs": 0, "fats": 20, "fiber": 0, "serving": "1 serving (150g)"},
    "beef": {"calories": 350, "protein": 31, "carbs": 0, "fats": 22, "fiber": 0, "serving": "1 serving (150g)"},
    "turkey": {"calories": 300, "protein": 26, "carbs": 0, "fats": 20, "fiber": 0, "serving": "1 serving (150g)"},
    "lamb": {"calories": 340, "protein": 29, "carbs": 0, "fats": 24, "fiber": 0, "serving": "1 serving (150g)"},
    "shrimp": {"calories": 120, "protein": 23, "carbs": 0, "fats": 2, "fiber": 0, "serving": "1 serving (100g)"},
    
    # Grains
    "rice": {"calories": 205, "protein": 4, "carbs": 45, "fats": 0, "fiber": 1, "serving": "1 cup cooked (195g)"},
    "pasta": {"calories": 220, "protein": 8, "carbs": 43, "fats": 2, "fiber": 3, "serving": "1 cup cooked (140g)"},
    "noodles": {"calories": 220, "protein": 8, "carbs": 43, "fats": 2, "fiber": 3, "serving": "1 cup cooked (140g)"},
    "fried rice": {"calories": 300, "protein": 10, "carbs": 38, "fats": 12, "fiber": 2, "serving": "1 bowl (200g)"},
    "ramen": {"calories": 280, "protein": 9, "carbs": 38, "fats": 10, "fiber": 3, "serving": "1 bowl (200g)"},
    "couscous": {"calories": 176, "protein": 6, "carbs": 36, "fats": 0, "fiber": 2, "serving": "1 cup cooked (157g)"},
    "quinoa": {"calories": 222, "protein": 8, "carbs": 39, "fats": 4, "fiber": 7, "serving": "1 cup cooked (185g)"},
    
    # Sides
    "french fries": {"calories": 320, "protein": 4, "carbs": 41, "fats": 15, "fiber": 4, "serving": "1 medium (117g)"},
    "baked beans": {"calories": 150, "protein": 8, "carbs": 30, "fats": 2, "fiber": 7, "serving": "1 cup (150g)"},
    "corn": {"calories": 132, "protein": 5, "carbs": 23, "fats": 2, "fiber": 2, "serving": "1 cup (145g)"},
    "peas": {"calories": 118, "protein": 8, "carbs": 21, "fats": 0, "fiber": 7, "serving": "1 cup (145g)"},
    
    # Vegetables
    "vegetables": {"calories": 90, "protein": 4, "carbs": 14, "fats": 2, "fiber": 5, "serving": "1 cup cooked (150g)"},
    "broccoli": {"calories": 55, "protein": 4, "carbs": 11, "fats": 1, "fiber": 2, "serving": "1 cup (156g)"},
    "spinach": {"calories": 41, "protein": 5, "carbs": 7, "fats": 0, "fiber": 1, "serving": "1 cup cooked (180g)"},
    "carrot": {"calories": 52, "protein": 1, "carbs": 12, "fats": 0, "fiber": 3, "serving": "1 medium (61g)"},
    "lettuce": {"calories": 15, "protein": 1, "carbs": 3, "fats": 0, "fiber": 1, "serving": "1 cup (47g)"},
    "potato": {"calories": 103, "protein": 2, "carbs": 23, "fats": 0, "fiber": 2, "serving": "1 medium (150g)"},
    "sweet potato": {"calories": 111, "protein": 2, "carbs": 26, "fats": 0, "fiber": 4, "serving": "1 medium (150g)"},
    "tomato": {"calories": 27, "protein": 1, "carbs": 6, "fats": 0, "fiber": 2, "serving": "1 medium (123g)"},
    "cucumber": {"calories": 16, "protein": 1, "carbs": 4, "fats": 0, "fiber": 1, "serving": "1 cup (104g)"},
    "mushroom": {"calories": 22, "protein": 3, "carbs": 3, "fats": 0, "fiber": 1, "serving": "1 cup (70g)"},
    
    # Fruits
    "apple": {"calories": 95, "protein": 0, "carbs": 25, "fats": 0, "fiber": 4, "serving": "1 medium (182g)"},
    "banana": {"calories": 105, "protein": 1, "carbs": 27, "fats": 0, "fiber": 3, "serving": "1 medium (118g)"},
    "orange": {"calories": 62, "protein": 1, "carbs": 16, "fats": 0, "fiber": 3, "serving": "1 medium (131g)"},
    "strawberry": {"calories": 49, "protein": 1, "carbs": 12, "fats": 0, "fiber": 3, "serving": "1 cup (152g)"},
    "grape": {"calories": 104, "protein": 1, "carbs": 28, "fats": 0, "fiber": 1, "serving": "1 cup (151g)"},
    "watermelon": {"calories": 46, "protein": 1, "carbs": 11, "fats": 0, "fiber": 1, "serving": "1 cup (152g)"},
    "mango": {"calories": 99, "protein": 1, "carbs": 25, "fats": 0, "fiber": 3, "serving": "1 cup (165g)"},
    "pineapple": {"calories": 83, "protein": 1, "carbs": 22, "fats": 0, "fiber": 3, "serving": "1 cup (165g)"},
    
    # Dairy
    "milk": {"calories": 149, "protein": 8, "carbs": 12, "fats": 8, "fiber": 0, "serving": "1 cup (244g)"},
    "cheese": {"calories": 113, "protein": 7, "carbs": 1, "fats": 9, "fiber": 0, "serving": "1 oz (28g)"},
    "yogurt": {"calories": 100, "protein": 10, "carbs": 7, "fats": 3, "fiber": 0, "serving": "1 cup (227g)"},
    "ice cream": {"calories": 210, "protein": 4, "carbs": 24, "fats": 11, "fiber": 0, "serving": "1 cup (150g)"},
    
    # Desserts
    "cake": {"calories": 250, "protein": 3, "carbs": 40, "fats": 10, "fiber": 1, "serving": "1 slice (80g)"},
    "donut": {"calories": 300, "protein": 4, "carbs": 38, "fats": 15, "fiber": 1, "serving": "1 donut (70g)"},
    "cookie": {"calories": 140, "protein": 2, "carbs": 18, "fats": 7, "fiber": 1, "serving": "1 cookie (30g)"},
    "chocolate": {"calories": 235, "protein": 3, "carbs": 26, "fats": 14, "fiber": 3, "serving": "1 bar (35g)"},
    "apple pie": {"calories": 260, "protein": 3, "carbs": 34, "fats": 12, "fiber": 2, "serving": "1 slice (120g)"},
    "pie": {"calories": 260, "protein": 3, "carbs": 34, "fats": 12, "fiber": 2, "serving": "1 slice (120g)"},
    
    # Asian
    "sushi": {"calories": 180, "protein": 8, "carbs": 30, "fats": 4, "fiber": 1, "serving": "1 serving (120g)"},
    "pad thai": {"calories": 350, "protein": 12, "carbs": 38, "fats": 15, "fiber": 3, "serving": "1 serving (200g)"},
    "spring roll": {"calories": 140, "protein": 5, "carbs": 20, "fats": 5, "fiber": 2, "serving": "1 roll (50g)"},
    
    # Mexican
    "tacos": {"calories": 240, "protein": 12, "carbs": 26, "fats": 10, "fiber": 3, "serving": "2 tacos (150g)"},
    "enchilada": {"calories": 260, "protein": 12, "carbs": 28, "fats": 12, "fiber": 3, "serving": "1 enchilada (150g)"},
    "nachos": {"calories": 310, "protein": 8, "carbs": 38, "fats": 14, "fiber": 4, "serving": "1 serving (150g)"},
    "burrito": {"calories": 320, "protein": 14, "carbs": 40, "fats": 12, "fiber": 4, "serving": "1 burrito (200g)"},
    
    # Indian
    "chapati": {"calories": 180, "protein": 5, "carbs": 30, "fats": 4, "fiber": 3, "serving": "1 chapati (60g)"},
    "curry": {"calories": 240, "protein": 12, "carbs": 20, "fats": 12, "fiber": 2, "serving": "1 serving (200g)"},
    "naan": {"calories": 262, "protein": 8, "carbs": 43, "fats": 5, "fiber": 1, "serving": "1 naan (90g)"},
    "samosa": {"calories": 262, "protein": 5, "carbs": 32, "fats": 12, "fiber": 2, "serving": "1 samosa (50g)"},
    
    # Soups & Salads
    "soup": {"calories": 180, "protein": 9, "carbs": 20, "fats": 7, "fiber": 3, "serving": "1 bowl (250ml)"},
    "salad": {"calories": 120, "protein": 5, "carbs": 12, "fats": 6, "fiber": 4, "serving": "1 bowl (200g)"},
    "caesar salad": {"calories": 180, "protein": 8, "carbs": 16, "fats": 10, "fiber": 2, "serving": "1 bowl (200g)"},
    
    # Sandwiches & Wraps
    "sandwich": {"calories": 290, "protein": 16, "carbs": 32, "fats": 10, "fiber": 3, "serving": "1 sandwich (150g)"},
    "wrap": {"calories": 280, "protein": 15, "carbs": 35, "fats": 9, "fiber": 3, "serving": "1 wrap (150g)"},
    
    # Snacks
    "nuts": {"calories": 200, "protein": 7, "carbs": 8, "fats": 16, "fiber": 3, "serving": "1 oz (28g)"},
    "chips": {"calories": 160, "protein": 2, "carbs": 15, "fats": 10, "fiber": 1, "serving": "1 oz (28g)"},
    "popcorn": {"calories": 110, "protein": 4, "carbs": 22, "fats": 2, "fiber": 4, "serving": "1 cup (31g)"},
    "pretzel": {"calories": 108, "protein": 3, "carbs": 21, "fats": 1, "fiber": 1, "serving": "1 oz (28g)"},
}

ALIAS_MAP = {
    # Burgers
    "cheeseburger": "burger",
    "hamburger": "burger",
    "beef burger": "burger",
    
    # Hot dogs
    "hotdog": "hot dog",
    "frankfurter": "hot dog",
    "wiener": "hot dog",
    
    # Fries
    "french fries": "french fries",
    "frenchfried": "french fries",
    "fries": "french fries",
    "deep fried potato": "french fries",
    
    # Chicken
    "fried chicken": "fried chicken",
    "crispy chicken": "fried chicken",
    "chicken breast": "chicken",
    "roasted chicken": "chicken",
    "grilled chicken": "chicken",
    
    # Breakfast
    "waffle": "waffles",
    "waffles": "waffles",
    "pancake": "pancakes",
    "pancakes": "pancakes",
    "omelet": "omelette",
    "omelette": "omelette",
    "scrambled eggs": "omelette",
    "cereal": "cereal",
    "toast": "toast",
    "bread": "bread",
    "whole wheat bread": "bread",
    "bagel": "bagel",
    "english muffin": "toast",
    
    # Proteins
    "steak": "steak",
    "beef steak": "steak",
    "grilled steak": "steak",
    "baked chicken": "chicken",
    "fish": "fish",
    "grilled fish": "fish",
    "baked fish": "fish",
    "salmon": "salmon",
    "grilled salmon": "salmon",
    "pork": "pork",
    "pork chop": "pork",
    "beef": "beef",
    "roast beef": "beef",
    "turkey": "turkey",
    "turkey breast": "turkey",
    "lamb": "lamb",
    "lamb chop": "lamb",
    "shrimp": "shrimp",
    "prawn": "shrimp",
    
    # Grains
    "white rice": "rice",
    "brown rice": "rice",
    "jasmine rice": "rice",
    "rice": "rice",
    "spaghetti": "pasta",
    "noodles": "noodles",
    "lo mein": "noodles",
    "chow mein": "noodles",
    "ramen": "ramen",
    "instant ramen": "ramen",
    "fried rice": "fried rice",
    "egg fried rice": "fried rice",
    "couscous": "couscous",
    "quinoa": "quinoa",
    
    # Sides
    "baked beans": "baked beans",
    "corn": "corn",
    "sweet corn": "corn",
    "peas": "peas",
    "green peas": "peas",
    
    # Vegetables
    "broccoli": "broccoli",
    "spinach": "spinach",
    "carrot": "carrot",
    "lettuce": "lettuce",
    "potato": "potato",
    "sweet potato": "sweet potato",
    "yam": "sweet potato",
    "tomato": "tomato",
    "cucumber": "cucumber",
    "mushroom": "mushroom",
    
    # Fruits
    "apple": "apple",
    "granny smith apple": "apple",
    "red apple": "apple",
    "banana": "banana",
    "orange": "orange",
    "mandarin": "orange",
    "strawberry": "strawberry",
    "berry": "strawberry",
    "grape": "grape",
    "watermelon": "watermelon",
    "mango": "mango",
    "pineapple": "pineapple",
    
    # Dairy
    "milk": "milk",
    "whole milk": "milk",
    "cheese": "cheese",
    "cheddar": "cheese",
    "yogurt": "yogurt",
    "greek yogurt": "yogurt",
    "ice cream": "ice cream",
    
    # Desserts
    "cake": "cake",
    "chocolate cake": "cake",
    "donut": "donut",
    "doughnut": "donut",
    "cookie": "cookie",
    "chocolate chip cookie": "cookie",
    "chocolate": "chocolate",
    "apple pie": "apple pie",
    "pie": "pie",
    
    # Asian
    "sushi": "sushi",
    "nigiri": "sushi",
    "pad thai": "pad thai",
    "spring roll": "spring roll",
    
    # Mexican
    "taco": "tacos",
    "tacos": "tacos",
    "enchilada": "enchilada",
    "nachos": "nachos",
    "burrito": "burrito",
    "quesadilla": "burrito",
    
    # Indian
    "chapati": "chapati",
    "chapathi": "chapati",
    "roti": "chapati",
    "curry": "curry",
    "naan": "naan",
    "samosa": "samosa",
    "biryani": "curry",
    
    # Soups & Salads
    "soup": "soup",
    "broth": "soup",
    "salad": "salad",
    "garden salad": "salad",
    "caesar salad": "caesar salad",
    "greek salad": "salad",
    
    # Sandwiches & Wraps
    "sandwich": "sandwich",
    "wrap": "wrap",
    "burrito wrap": "wrap",
    
    # Snacks
    "nuts": "nuts",
    "almond": "nuts",
    "peanut": "nuts",
    "chips": "chips",
    "popcorn": "popcorn",
    "pretzel": "pretzel",
    "snack": "chips",
}

SUPPORTED_FOODS = tuple(sorted(NUTRITION_DATA.keys()))


def normalize_food_label(label: str) -> str:
    """Return a normalized food label mapped to a supported food name.

    The normalization is STRICTLY CONSERVATIVE: 
    - Only maps labels that genuinely correspond to supported foods
    - Does NOT invent food mappings for non-food objects (plate, dish, bowl, etc)
    - Returns the original label if no match found (predict() will reject it)
    """
    if not label:
        return ""

    cleaned = label.lower().strip()
    cleaned = cleaned.replace("_", " ")
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    cleaned = " ".join(cleaned.split())

    if not cleaned:
        return ""

    # Direct alias lookup
    if cleaned in ALIAS_MAP:
        return ALIAS_MAP[cleaned]

    # Substring matching for close aliases
    for key, value in ALIAS_MAP.items():
        if key in cleaned or cleaned in key:
            return value

    # REMOVED: No aggressive fallback that maps plate/dish/bowl to pizza/salad
    # If model predicts "Petri_dish", "plate", "tray", etc., those should NOT
    # be converted to default foods. Return unmapped so predict() can reject it.

    # Return the cleaned label unchanged - predict() will reject if not in NUTRITION_DATA
    return cleaned


def safe_nutrition_lookup(food_name: str) -> Dict[str, Any] | None:
    normalized = normalize_food_label(food_name)
    if normalized in NUTRITION_DATA:
        return NUTRITION_DATA[normalized]
    return None


def calculate_meal_quality_score(nutrition: Dict[str, Any]) -> int:
    """Estimate a 0-100 meal quality score from nutrition values.

    This is a transparent heuristic based on balance and moderation:
    - higher protein and fiber increase score
    - very high calories, fat, and carbs lower the score
    - the result is deterministic and intentionally conservative

    The score is not a medical diagnosis and should be treated as a rough estimate.
    """
    calories = max(0, float(nutrition.get("calories", 0)))
    protein = max(0, float(nutrition.get("protein", 0)))
    carbs = max(0, float(nutrition.get("carbs", 0)))
    fats = max(0, float(nutrition.get("fats", 0)))
    fiber = max(0, float(nutrition.get("fiber", 0)))

    protein_score = min(1.0, protein / 30.0) * 35
    fiber_score = min(1.0, fiber / 8.0) * 20
    moderate_calorie_score = max(0.0, 1.0 - (calories / 700.0)) * 15
    moderate_fat_score = max(0.0, 1.0 - (fats / 25.0)) * 15
    moderate_carb_score = max(0.0, 1.0 - (carbs / 80.0)) * 15

    score = protein_score + fiber_score + moderate_calorie_score + moderate_fat_score + moderate_carb_score
    return max(0, min(100, int(round(score))))
