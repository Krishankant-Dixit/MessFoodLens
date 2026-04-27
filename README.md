# MessFoodLens

> AI-powered food nutrition analyzer – upload a photo, detect the food, get nutrition info.

## Features

- 📷 **Drag-and-drop image upload** (JPEG / PNG / WEBP, up to 10 MB)
- 🤖 **AI Food Detection** using MobileNetV2 pre-trained on ImageNet
- 🥗 **Nutrition Info** – calories, protein, carbs, fats, fiber, serving size
- ⭐ **Meal Quality Score** (0–100)
- 📊 **Macro Breakdown** pie chart
- 📈 **Analytics Dashboard** with weekly calorie bar chart and quality trend line

## Project Structure

```
MessFoodLens/
├── backend/
│   ├── main.py            # FastAPI app, POST /analyze endpoint
│   ├── model.py           # MobileNetV2 image classification
│   ├── nutrition_data.py  # Nutrition dictionary (20+ foods)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx        # Router & navbar
    │   ├── Home.jsx       # Landing page
    │   ├── Upload.jsx     # Drag-and-drop upload + loading animation
    │   ├── Result.jsx     # Nutrition results + charts
    │   └── Dashboard.jsx  # Analytics dashboard
    └── vite.config.js
```

## How to Run

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## API

### `POST /analyze`

Upload a food image and receive nutrition data.

**Request**: `multipart/form-data` with field `file` (image).

**Response**:
```json
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
  "raw_labels": [
    { "label": "pizza", "confidence": 87.3 }
  ],
  "inference_time_ms": 142.5
}
```

## Supported Foods

pizza, burger, hot dog, french fries, ice cream, apple pie, donut, waffles,
pancakes, sushi, soup, steak, chicken, fish, rice, pasta, salad, sandwich,
tacos, nachos, omelette, fried rice, and more.
