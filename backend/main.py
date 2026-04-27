"""
MessFoodLens – FastAPI backend
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from model import classify_image
from nutrition_data import get_nutrition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App lifecycle: pre-load model on startup so the first request is fast
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Pre-loading ML model…")
    try:
        from model import load_model
        load_model()
        logger.info("Model ready.")
    except Exception as exc:
        logger.warning("Could not pre-load model: %s", exc)
    yield


app = FastAPI(
    title="MessFoodLens API",
    description="Upload a food image and get nutrition information.",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the Vite dev server (and any other origin during development) to call
# the API.  In production, restrict origins to your actual domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
}

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


@app.get("/")
async def root():
    return {"message": "MessFoodLens API is running. POST /analyze to detect food."}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Receive an uploaded food image, classify it, and return nutrition data.

    Returns JSON:
    {
        "food": "pizza",
        "confidence": 87.3,
        "calories": 285,
        "protein": "12g",
        "carbs": "36g",
        "fats": "10g",
        "fiber": "2g",
        "serving": "1 slice (107g)",
        "meal_quality_score": 55,
        "raw_labels": [...]
    }
    """
    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. "
                   "Please upload a JPEG, PNG, WEBP or GIF image.",
        )

    # Read & size-check
    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="File too large. Maximum allowed size is 10 MB.",
        )

    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    start = time.perf_counter()
    try:
        classification = classify_image(image_bytes)
    except Exception as exc:
        logger.exception("Model inference failed")
        raise HTTPException(status_code=500, detail=f"Model inference failed: {exc}") from exc

    elapsed = round((time.perf_counter() - start) * 1000, 1)
    logger.info(
        "Classified as '%s' (%.1f%%) in %s ms",
        classification["food_label"],
        classification["confidence"],
        elapsed,
    )

    nutrition = get_nutrition(classification["food_label"])

    return JSONResponse(
        content={
            **nutrition,
            "confidence": classification["confidence"],
            "raw_labels": classification["raw_labels"],
            "inference_time_ms": elapsed,
        }
    )
