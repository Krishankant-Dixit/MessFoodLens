#!/usr/bin/env python3
"""
Independent food classifier test - directly test model predictions without API.

Usage:
    python test_model_debug.py image1.jpg image2.png image3.webp
    
This script bypasses the API and directly tests the classifier to verify:
1. Different images produce different predictions
2. Model predictions are consistent
3. Label mapping works correctly
"""

import sys
import logging
from pathlib import Path
from PIL import Image

from model import FoodClassifier
from nutrition_data import NUTRITION_DATA

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def test_image(image_path: str, classifier: FoodClassifier) -> dict:
    """Test a single image with the classifier."""
    logger.info(f"\n{'='*70}")
    logger.info(f"TESTING IMAGE: {image_path}")
    logger.info(f"{'='*70}")
    
    path = Path(image_path)
    if not path.exists():
        logger.error(f"File not found: {image_path}")
        return {}
    
    if not path.is_file():
        logger.error(f"Not a file: {image_path}")
        return {}
    
    logger.info(f"File size: {path.stat().st_size} bytes")
    logger.info(f"File path: {path.absolute()}")
    
    try:
        with Image.open(image_path) as pil_image:
            rgb_image = pil_image.convert("RGB")
            logger.info(f"Image loaded: {rgb_image.size} {rgb_image.mode}")
            
            result = classifier.predict(rgb_image)
            
            logger.info(f"\n{'='*70}")
            if result["success"]:
                logger.info(f"✓ SUCCESS")
                logger.info(f"  Food: {result['food']}")
                logger.info(f"  Confidence: {result['confidence']}%")
                logger.info(f"  Calories: {result['calories']} kcal")
                logger.info(f"  Protein: {result['protein']}g | Carbs: {result['carbs']}g | Fats: {result['fats']}g")
                logger.info(f"  Meal Quality Score: {result['meal_quality_score']}/100")
            else:
                logger.info(f"✗ FAILED")
                logger.info(f"  Message: {result['message']}")
            
            logger.info(f"  Inference time: {result['inference_time_ms']}ms")
            logger.info(f"{'='*70}\n")
            
            return result
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return {}


def main():
    if len(sys.argv) < 2:
        logger.error("Usage: python test_model_debug.py image1.jpg [image2.jpg ...]")
        logger.error("\nExample:")
        logger.error("  python test_model_debug.py pizza.jpg burger.png salad.webp")
        sys.exit(1)
    
    image_paths = sys.argv[1:]
    
    logger.info("\nInitializing FoodClassifier...")
    classifier = FoodClassifier()
    logger.info("✓ Classifier loaded\n")
    
    results = []
    for image_path in image_paths:
        result = test_image(image_path, classifier)
        if result:
            results.append({
                "file": image_path,
                "food": result.get("food"),
                "confidence": result.get("confidence"),
                "success": result.get("success"),
                "raw_labels": result.get("raw_labels", [])
            })
    
    # Summary
    if results:
        logger.info("\n" + "="*70)
        logger.info("SUMMARY")
        logger.info("="*70)
        for i, r in enumerate(results, 1):
            status = "✓" if r["success"] else "✗"
            logger.info(f"{i}. {r['file']}: {status} {r['food']} ({r['confidence']}%)")
        
        # Verify different images produce different results
        foods_detected = [r["food"] for r in results if r["success"]]
        if len(foods_detected) > 1:
            unique_foods = len(set(foods_detected))
            logger.info(f"\nUnique foods detected: {unique_foods}/{len(foods_detected)}")
            if unique_foods == len(foods_detected):
                logger.info("✓ GOOD: Each image produced different results")
            else:
                logger.warning(f"⚠ WARNING: Multiple images produced identical results!")
                logger.warning(f"  Results: {foods_detected}")
        logger.info("="*70)


if __name__ == "__main__":
    main()
