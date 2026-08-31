"""Food image classification using EfficientNet with food-awareness boost."""

from __future__ import annotations

import time
import logging
from typing import Dict, List, Any

import numpy as np
from PIL import Image

from nutrition_data import NUTRITION_DATA, normalize_food_label, calculate_meal_quality_score

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.15


class FoodClassifier:
    """Food recognition using EfficientNet with food-specific boost.
    
    This classifier uses EfficientNet pre-trained on ImageNet but applies
    food-specific confidence boosting for food-related predictions to improve
    food recognition accuracy.
    """

    def __init__(self, threshold: float = CONFIDENCE_THRESHOLD) -> None:
        self.threshold = threshold
        try:
            from tensorflow.keras.applications import EfficientNetB0
            self.model = EfficientNetB0(weights="imagenet")
            self.use_efficient = True
            logger.info("Loaded EfficientNetB0 model")
        except Exception as e:
            logger.warning(f"Could not load EfficientNetB0: {e}. Using MobileNetV2 fallback.")
            # Fallback to MobileNetV2
            from tensorflow.keras.applications import MobileNetV2
            self.model = MobileNetV2(weights="imagenet")
            self.use_efficient = False

        # Food keywords for confidence boosting
        self.food_keywords = {
            "pizza", "burger", "hot dog", "sandwich", "sushi", "taco",
            "pasta", "noodles", "rice", "chicken", "fish", "steak", "beef",
            "pork", "lamb", "salad", "soup", "bread", "toast", "bagel",
            "cake", "ice cream", "donut", "cookie", "chocolate", "fruit",
            "vegetable", "apple", "banana", "orange", "strawberry", "grape",
            "egg", "cheese", "milk", "yogurt", "pancake", "waffle", "fries",
            "chips", "nuts", "popcorn", "croissant", "broccoli", "spinach",
            "corn", "peas", "beans", "potato", "tomato", "carrot", "lettuce",
            "cucumber", "mushroom", "wrap", "burrito", "enchilada", "ramen",
            "pad thai", "curry", "naan", "samosa", "spring roll", "nacho",
            "sauce", "dressing", "gravy", "roast", "grilled", "fried", "baked",
            "boiled", "steamed", "raw", "fresh", "cooked", "meal", "food",
            "dinner", "lunch", "breakfast", "dessert", "appetizer", "snack",
            "dish", "plate", "bowl", "serving", "portion", "cuisine"
        }

    def _top_predictions(self, image: Image.Image, top_k: int = 20) -> List[Dict[str, Any]]:
        """Get top predictions and boost food-related ones."""
        resized = image.resize((224, 224), Image.Resampling.LANCZOS)
        array = np.array(resized).astype("float32")
        
        if self.use_efficient:
            from tensorflow.keras.applications.efficientnet import preprocess_input
        else:
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
        
        from tensorflow.keras.applications.imagenet_utils import decode_predictions
        
        preprocessed = preprocess_input(array)[np.newaxis, ...]
        predictions = self.model.predict(preprocessed, verbose=0)
        decoded = decode_predictions(predictions, top=top_k)

        results: List[Dict[str, Any]] = []
        for _, label, score in decoded[0]:
            confidence = float(score)
            
            # Apply food-specific confidence boost
            label_lower = label.lower().replace("_", " ")
            if any(keyword in label_lower for keyword in self.food_keywords):
                # Boost confidence for food-related predictions
                confidence = min(1.0, confidence * 1.5)
            
            results.append({
                "label": label,
                "confidence": confidence,
            })
        
        return results

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        started = time.perf_counter()
        raw_predictions = self._top_predictions(image)
        
        # DEBUG: Log raw predictions
        logger.info(f"\nTOP RAW PREDICTIONS:")
        for i, pred in enumerate(raw_predictions[:5], 1):
            logger.info(f"  {i}. {pred['label']}: {pred['confidence']*100:.2f}%")

        best_match: Dict[str, Any] | None = None
        best_matches_tried = []
        
        for prediction in raw_predictions:
            normalized = normalize_food_label(prediction["label"])
            best_matches_tried.append((prediction["label"], normalized, normalized in NUTRITION_DATA))
            
            if normalized not in NUTRITION_DATA:
                continue

            candidate = {
                "label": normalized,
                "confidence": float(prediction["confidence"]),
            }
            if best_match is None or candidate["confidence"] > best_match["confidence"]:
                best_match = candidate
        
        # DEBUG: Log normalization results
        logger.info(f"\nNORMALIZATION & LOOKUP:")
        for original, normalized, in_db in best_matches_tried[:5]:
            logger.info(f"  '{original}' → '{normalized}' {'[IN DB]' if in_db else '[NOT FOUND]'}")

        if best_match is None:
            logger.info(f"\nRESULT: No food detected")
            return {
                "success": False,
                "food": None,
                "confidence": 0,
                "message": "No food detected. Please upload a clear food image.",
                "raw_labels": raw_predictions[:5],
                "inference_time_ms": round((time.perf_counter() - started) * 1000, 2),
            }

        if best_match["confidence"] < self.threshold:
            logger.info(f"\nRESULT: Confidence too low ({best_match['confidence']*100:.2f}% < {self.threshold*100:.2f}%)")
            return {
                "success": False,
                "food": None,
                "confidence": 0,
                "message": "Confidence too low. Please try a clearer food image.",
                "raw_labels": raw_predictions[:5],
                "inference_time_ms": round((time.perf_counter() - started) * 1000, 2),
            }

        nutrition = NUTRITION_DATA[best_match["label"]]
        score = calculate_meal_quality_score(nutrition)
        
        logger.info(f"\nRESULT: SUCCESS")
        logger.info(f"  Food: {best_match['label']}")
        logger.info(f"  Confidence: {best_match['confidence']*100:.2f}%")
        logger.info(f"  Calories: {nutrition['calories']}")

        return {
            "success": True,
            "food": best_match["label"],
            "confidence": round(best_match["confidence"] * 100, 1),
            "calories": nutrition["calories"],
            "protein": nutrition["protein"],
            "carbs": nutrition["carbs"],
            "fats": nutrition["fats"],
            "fiber": nutrition["fiber"],
            "serving": nutrition["serving"],
            "meal_quality_score": score,
            "raw_labels": [{"label": item["label"], "confidence": round(item["confidence"] * 100, 1)} for item in raw_predictions[:5]],
            "inference_time_ms": round((time.perf_counter() - started) * 1000, 2),
        }
