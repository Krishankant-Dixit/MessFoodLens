"""
Food classification model using MobileNetV2 pre-trained on ImageNet.

The model predicts ImageNet class labels; we then map those labels to
our supported food categories so we can return nutrition data.
"""

from __future__ import annotations

import io
import logging
from functools import lru_cache
from typing import Optional

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ImageNet class labels that belong to each of our food categories.
# Keeping only the labels most relevant to food classification.
# ---------------------------------------------------------------------------

FOOD_LABEL_MAPPING: dict[str, list[str]] = {
    "pizza": ["pizza"],
    "burger": ["hamburger", "cheeseburger", "hotdog", "hot dog"],
    "hot dog": ["hotdog", "hot dog"],
    "french fries": ["french loaf", "french fries"],
    "ice cream": ["ice cream", "ice lolly", "popsicle"],
    "apple pie": ["apple pie"],
    "donut": ["doughnut", "donut"],
    "waffles": ["waffle"],
    "pancakes": ["pancake"],
    "sushi": ["sushi"],
    "soup": ["consomme", "chowder", "hotpot", "soup bowl"],
    "steak": ["beef", "steak", "meat loaf", "meatloaf"],
    "chicken": ["hen", "chicken", "cock", "drumstick", "fried chicken"],
    "fish": ["fish", "tench", "goldfish", "shark", "ray"],
    "rice": ["rice", "pilaf"],
    "pasta": ["spaghetti", "pasta", "lasagna", "carbonara"],
    "salad": ["salad", "broccoli", "spinach", "cauliflower", "head cabbage"],
    "sandwich": ["sandwich", "club sandwich", "submarine", "hoagie"],
    "tacos": ["taco", "burrito"],
    "nachos": ["nacho"],
    "omelette": ["omelette", "omelet"],
    "fried rice": ["fried rice"],
}

# Reverse mapping: imagenet_label_fragment -> food_category
_REVERSE_MAP: dict[str, str] = {}
for food_cat, imagenet_labels in FOOD_LABEL_MAPPING.items():
    for lbl in imagenet_labels:
        _REVERSE_MAP[lbl.lower()] = food_cat


def _build_imagenet_labels() -> list[str]:
    """Load ImageNet 1k class labels bundled with torchvision."""
    try:
        from torchvision.models import MobileNet_V2_Weights
        weights = MobileNet_V2_Weights.DEFAULT
        meta = weights.meta
        return [v.lower() for v in meta["categories"]]
    except Exception:
        # Fallback – return empty list; we will handle gracefully
        return []


@lru_cache(maxsize=1)
def load_model() -> tuple:
    """
    Load MobileNetV2 pretrained on ImageNet.
    Returns (model, transform, imagenet_labels).
    Cached so we only load once.
    """
    logger.info("Loading MobileNetV2 model…")
    try:
        weights = models.MobileNet_V2_Weights.DEFAULT
        model = models.mobilenet_v2(weights=weights)
        model.eval()
        transform = weights.transforms()
        imagenet_labels = [v.lower() for v in weights.meta["categories"]]
        logger.info("MobileNetV2 loaded successfully.")
        return model, transform, imagenet_labels
    except Exception as exc:
        logger.error("Failed to load MobileNetV2: %s", exc)
        raise


def _map_imagenet_to_food(label: str) -> Optional[str]:
    """Map an ImageNet label string to a food category, or return None."""
    label_lower = label.lower()
    # Exact / substring match against our reverse map
    for key, food_cat in _REVERSE_MAP.items():
        if key in label_lower or label_lower in key:
            return food_cat
    return None


def classify_image(image_bytes: bytes, top_k: int = 5) -> dict:
    """
    Classify a food image.

    Parameters
    ----------
    image_bytes : bytes
        Raw image data.
    top_k : int
        Number of top predictions to consider when mapping to food category.

    Returns
    -------
    dict with keys: food_label (str), confidence (float), raw_labels (list)
    """
    model, transform, imagenet_labels = load_model()

    # Pre-process image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0)  # shape: (1, 3, H, W)

    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0]

    top_probs, top_indices = torch.topk(probabilities, k=min(top_k, len(imagenet_labels)))
    top_labels = [imagenet_labels[idx.item()] for idx in top_indices]
    top_confidences = [float(p) for p in top_probs]

    raw_labels = [
        {"label": lbl, "confidence": round(conf * 100, 2)}
        for lbl, conf in zip(top_labels, top_confidences)
    ]

    # Find the first top prediction that maps to a food category
    food_label = None
    confidence = 0.0
    for lbl, conf in zip(top_labels, top_confidences):
        mapped = _map_imagenet_to_food(lbl)
        if mapped:
            food_label = mapped
            confidence = round(conf * 100, 2)
            break

    # Fallback: use the highest-confidence raw label even if unmapped
    if food_label is None:
        food_label = top_labels[0] if top_labels else "unknown"
        confidence = top_confidences[0] * 100 if top_confidences else 0.0
        confidence = round(confidence, 2)

    return {
        "food_label": food_label,
        "confidence": confidence,
        "raw_labels": raw_labels,
    }
