# MessFoodLens

MessFoodLens is an AI-powered food nutrition analyzer. Users upload a food image, the backend estimates the likely food using MobileNetV2 pretrained on ImageNet, maps the label to a supported food, and returns estimated nutrition values plus a meal quality score.

> MessFoodLens provides estimated nutrition information and is not a medical or professional dietary assessment.

## Features

- Drag-and-drop image upload for JPEG, PNG, and WEBP files
- AI food detection using MobileNetV2 with ImageNet weights
- Nutrition estimation for common foods and mess-style meals
- Meal quality score from 0 to 100
- Macro breakdown chart and dashboard history
- Frontend and backend integration with clean validation and error handling

## Tech Stack

- Frontend: React, Vite, JavaScript, React Router, Axios, Recharts
- Backend: Python, FastAPI, Uvicorn, Pydantic, Pillow, NumPy, TensorFlow/Keras
- AI Model: MobileNetV2 pretrained on ImageNet

## Project Structure

```text
MessFoodLens/
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── nutrition_data.py
│   ├── requirements.txt
│   └── uploads/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Upload.jsx
│   │   │   ├── Result.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── README.md
├── Readme.md
└── backend/uploads/.gitkeep
```

## Architecture

1. The frontend sends a multipart image upload to the FastAPI backend.
2. The backend validates file type, file size, and image integrity.
3. MobileNetV2 runs on the uploaded image.
4. Labels are normalized and matched only to supported food entries.
5. Nutrition values are looked up from a local nutrition dictionary.
6. A transparent meal quality score is computed.
7. The UI shows the output and stores local dashboard data in browser localStorage.

## Installation

### Prerequisites

- Python 3.13
- Node.js 18+ and npm

### Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend setup

```bash
cd frontend
npm install
```

## Running the Project

### Start backend

```bash
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend is available at http://localhost:8000.

### Start frontend

```bash
cd frontend
npm run dev
```

The frontend is available at http://localhost:5173.

## API Endpoints

### GET /

Returns a simple health message.

```json
{"message": "MessFoodLens API is running"}
```

### GET /health

Returns:

```json
{"status": "healthy"}
```

### POST /analyze

Accepts multipart/form-data with a file field.

#### Success example

```json
{
  "success": true,
  "food": "pizza",
  "confidence": 87.3,
  "calories": 285,
  "protein": 12,
  "carbs": 36,
  "fats": 10,
  "fiber": 2,
  "serving": "1 slice (107g)",
  "meal_quality_score": 55,
  "raw_labels": [{ "label": "pizza", "confidence": 87.3 }],
  "inference_time_ms": 142.5
}
```

#### Low-confidence example

```json
{
  "success": false,
  "food": null,
  "confidence": 0,
  "message": "Food could not be identified confidently.",
  "raw_labels": [],
  "inference_time_ms": 0
}
```

## Supported Foods

The app includes a nutrition dataset for:

- pizza
- burger
- hot dog
- french fries
- ice cream
- apple pie
- donut
- waffles
- pancakes
- sushi
- soup
- steak
- chicken
- fish
- rice
- pasta
- salad
- sandwich
- tacos
- nachos
- omelette
- fried rice
- chapati
- vegetables
- apple

## AI Model Explanation

MobileNetV2 is loaded with ImageNet weights. This is useful for rough image classification and for a local demo, but it is not a specialized food-recognition model. The application intentionally checks whether the predicted class can be mapped to a supported food and enforces a confidence threshold. If the confidence is too low, it refuses to guess and returns a low-confidence error instead of inventing a result.

## Nutrition Estimation Explanation

Nutrition values are estimated from a local dictionary that uses standard serving sizes. These numbers are conservative estimates and are meant to help illustrate user experience and analytics rather than replace professional nutrition guidance.

## Meal Quality Scoring

The `calculate_meal_quality_score` function uses transparent heuristics:

- more protein helps the score
- more fiber helps the score
- very high calories, fats, and carbohydrates reduce the score
- the output is deterministic for the same food

The score is intended as an estimate only and should not be treated as a medical or dietary diagnosis.

## Limitations

- MobileNetV2 is not a dedicated food recognition model.
- Nutrition data is approximate and depends on serving assumptions.
- The app is intended for local demo/testing, not production-grade clinical nutrition analysis.
- Real-world food recognition may fail when dishes are mixed, partially visible, or visually ambiguous.

## Troubleshooting

### Backend fails to start

- Ensure the virtual environment is active.
- Confirm TensorFlow and FastAPI packages are installed.
- Check the terminal output for missing dependencies or incompatible Python version.

### Frontend cannot reach backend

- Confirm the backend is running on http://localhost:8000.
- Verify `VITE_API_URL` is set correctly if using a custom backend URL.

### Image upload rejected

- Ensure the image is JPEG, PNG, or WEBP.
- Keep file size under 10 MB.
- Avoid uploading corrupted or empty files.

## Future Improvements

- Replace ImageNet classification with a custom food dataset and fine-tuned model.
- Use a larger nutrition database with more dishes and regional meals.
- Add user accounts and persistent history with a real database.
- Improve image preprocessing and multi-label classification.
- Add better confidence handling and user feedback panels.

## Disclaimer

MessFoodLens provides estimated nutrition information and is not a medical or professional dietary assessment.

