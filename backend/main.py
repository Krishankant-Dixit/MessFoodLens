from __future__ import annotations

import os
from io import BytesIO
from typing import Any
import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from model import FoodClassifier

# Configure debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

app = FastAPI(title="MessFoodLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|0\.0\.0\.0):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = FoodClassifier()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "MessFoodLens API is running"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


def validate_uploaded_file(file: UploadFile, file_bytes: bytes) -> None:
    if file.filename is None or file.filename.strip() == "":
        raise HTTPException(status_code=400, detail="No file selected.")

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB size limit.")

    extension = os.path.splitext(file.filename)[1].lower()
    content_type = file.content_type or ""

    if content_type not in ALLOWED_IMAGE_TYPES and extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported file type. Please upload a JPEG, PNG, or WEBP image.")

    try:
        with Image.open(BytesIO(file_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)) -> dict[str, Any]:
    try:
        file_bytes = await file.read()
        validate_uploaded_file(file, file_bytes)

        # DEBUG: Log file information
        logger.info(f"\n{'='*60}")
        logger.info(f"ANALYZE REQUEST")
        logger.info(f"Filename: {file.filename}")
        logger.info(f"Content-Type: {file.content_type}")
        logger.info(f"File size (bytes): {len(file_bytes)}")
        logger.info(f"File hash (first 20 bytes): {file_bytes[:20].hex()}")

        with Image.open(BytesIO(file_bytes)) as pil_image:
            rgb_image = pil_image.convert("RGB")
            
            # DEBUG: Log image properties
            logger.info(f"Image mode: {rgb_image.mode}")
            logger.info(f"Image size: {rgb_image.size}")
            logger.info(f"Image format: {rgb_image.format}")
            
            result = classifier.predict(rgb_image)
            
            # DEBUG: Log results
            logger.info(f"Prediction success: {result['success']}")
            logger.info(f"Detected food: {result.get('food', 'N/A')}")
            logger.info(f"Confidence: {result.get('confidence', 'N/A')}%")
            logger.info(f"Raw labels: {result.get('raw_labels', [])[:3]}")
            logger.info(f"{'='*60}\n")

        if not result["success"]:
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "food": None,
                    "confidence": 0,
                    "message": result["message"],
                    "raw_labels": result["raw_labels"],
                    "inference_time_ms": result["inference_time_ms"],
                },
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to analyze the uploaded image.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
