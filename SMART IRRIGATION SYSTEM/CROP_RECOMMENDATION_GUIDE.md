# Crop Recommendation System Integration

## Overview
The Crop Recommendation System has been successfully integrated into the Smart Irrigation System. This AI-powered feature uses a Random Forest machine learning model to predict the best crops based on soil parameters and environmental conditions.

## ✨ New Features

### 🤖 **Auto Analysis Mode** (New!)
- **Automatic Data Fetching:** Fetches all soil analysis data and sensor readings from your database
- **Intelligent Averaging:** Automatically calculates average values for:
  - Nitrogen (N)
  - Phosphorus (P)
  - Potassium (K)
  - Temperature
  - Humidity
  - pH Level
  - Rainfall
- **One-Click Analysis:** Get crop recommendations with a single button click
- **Top 5 Recommendations:** Shows the top 5 most suitable crops with confidence scores
- **Visual Display:** Each crop recommendation includes colorful emoji icons
- **Data Summary:** Shows how many soil records and sensor readings were analyzed

### ✍️ Manual Input Mode
- Enter soil and environmental parameters manually
- Get instant AI-powered crop recommendations
- View top 3 crop suggestions with confidence scores

### 🖼️ **Crop Images** (New!)
- All crop recommendations now display with visual icons (emojis)
- Large visual display for the top recommended crop
- Smaller icons for alternative recommendations

### 📊 Visual Parameter Display
- Color-coded parameter cards
- Easy-to-read average values
- Beautiful gradient backgrounds

## API Endpoints

### 1. POST `/api/crop-recommendation/predict`
Predict crop based on manual input parameters.

**Request Body:**
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.8,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9,
  "land_id": 1 (optional)
}
```

**Response:**
```json
{
  "recommended_crop": "rice",
  "confidence": 95.5,
  "top_3_recommendations": [
    {"rank": 1, "crop_name": "rice", "probability": 95.5},
    {"rank": 2, "crop_name": "cotton", "probability": 3.2},
    {"rank": 3, "crop_name": "maize", "probability": 1.3}
  ],
  "input_parameters": {
    "nitrogen": 90,
    "phosphorus": 42,
    "potassium": 43,
    "temperature": 20.8,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.9
  }
}
```

### 2. GET `/api/crop-recommendation/auto-analyze` ⭐ NEW
Automatically fetch all soil and sensor data, calculate averages, and provide recommendations.

**Response:**
```json
{
  "analysis_type": "Auto Analysis - All Lands Average",
  "total_soil_records": 150,
  "total_sensor_readings": 500,
  "recommended_crop": "rice",
  "confidence": 92.5,
  "top_5_recommendations": [
    {"rank": 1, "crop_name": "rice", "probability": 92.5},
    {"rank": 2, "crop_name": "wheat", "probability": 4.2},
    {"rank": 3, "crop_name": "maize", "probability": 2.1},
    {"rank": 4, "crop_name": "cotton", "probability": 0.8},
    {"rank": 5, "crop_name": "jute", "probability": 0.4}
  ],
  "average_parameters": {
    "nitrogen": 85.50,
    "phosphorus": 45.30,
    "potassium": 50.20,
    "temperature": 25.60,
    "humidity": 75.40,
    "ph_level": 6.80,
    "rainfall": 150.00
  }
}
```

### 3. POST `/api/crop-recommendation/predict-from-soil/{land_id}`
Predict crop using existing soil analysis and sensor data for a specific land.

**Response:** Same as manual predict, plus `soil_data_used` field

### 4. GET `/api/crop-recommendation/model-info`
Get information about the ML model.

**Response:**
```json
{
  "status": "available",
  "model_type": "Random Forest Classifier",
  "supported_crops": ["rice", "maize", "cotton", ...],
  "total_crops": 22,
  "input_features": [
    "Nitrogen (N)",
    "Phosphorus (P)",
    "Potassium (K)",
    "Temperature (°C)",
    "Humidity (%)",
    "pH Level",
    "Rainfall (mm)"
  ],
  "feature_count": 7
}
```

## Frontend Usage

### Access the Feature
1. Start the backend server: `cd backend && python -m uvicorn main:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Navigate to: `http://localhost:5173/crop-recommendation`

### Using Auto Analysis (Recommended) 🌟
1. **Click on "Auto Analysis" Tab** (Default tab)
2. **Click "Start Auto Analysis" Button**
3. **Wait for Processing:** System will:
   - Fetch all soil analysis data from database
   - Fetch all sensor readings
   - Calculate average values
   - Run ML prediction
4. **View Results:**
   - Large crop icon and name for top recommendation
   - Confidence percentage
   - Top 5 crop alternatives with icons
   - Color-coded parameter cards showing averages used
   - Summary of data analyzed

### Using Manual Input
1. **Click on "Manual Input" Tab**
2. **Enter Parameters:** Fill in all 7 required fields
   - N, P, K values (soil nutrients)
   - Temperature, Humidity, pH, Rainfall
3. **Get Recommendation:** Click "Get Recommendation" button
4. **View Results:** 
   - Main recommended crop with large icon and confidence score
   - Top 3 alternatives with icons
   - Parameters used for prediction

### Supported Crops with Icons
- 🌾 Rice
- 🌽 Maize
- 🫘 Chickpea, Kidney Beans, Moth Beans, Black Gram, Lentil
- 🫛 Pigeon Peas, Mung Bean
- 🍎 Pomegranate, Apple
- 🍌 Banana
- 🥭 Mango
- 🍇 Grapes
- 🍉 Watermelon
- 🍈 Muskmelon, Papaya
- 🍊 Orange
- 🥥 Coconut
- ☁️ Cotton
- 🌿 Jute
- ☕ Coffee

### Input Ranges
- **Nitrogen (N):** 0-140
- **Phosphorus (P):** 5-145
- **Potassium (K):** 5-205
- **Temperature:** 8-44°C
- **Humidity:** 14-100%
- **pH Level:** 3.5-10
- **Rainfall:** 20-300mm

## Technical Details

### Model Information
- **Type:** Random Forest Classifier
- **Training Data:** Agricultural crop recommendation dataset
- **Features:** 7 input parameters (NPK, Temperature, Humidity, pH, Rainfall)
- **Supported Crops:** 22 varieties including rice, maize, wheat, cotton, etc.
- **Model File:** `backend/crop_model.pkl`

### Dependencies Added
- `scikit-learn` - Machine learning library
- `joblib` - Model serialization

### Files Modified/Created
1. **Backend:**
   - `backend/main.py` - Added 4 new endpoints (including auto-analyze)
   - `backend/requirements.txt` - Added ML dependencies
   - `backend/crop_model.pkl` - Trained model file

2. **Frontend:**
   - `frontend/src/pages/CropRecommendation.tsx` - Enhanced with auto-analysis and crop images
   - `frontend/src/App.tsx` - Added route

## Testing

### Test Auto Analysis
Simply navigate to `/crop-recommendation` and click "Start Auto Analysis"

### Test Manual Analysis with Sample Data
```bash
curl -X POST http://localhost:8000/api/crop-recommendation/predict \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.8,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 202.9
  }'
```

### Test Auto Analysis Endpoint
```bash
curl http://localhost:8000/api/crop-recommendation/auto-analyze
```

### Expected Behavior
- High confidence (>80%) indicates strong recommendation
- Medium confidence (60-80%) suggests suitable but not optimal
- Low confidence (<60%) means conditions don't strongly match any crop

## Integration with Existing Features

The crop recommendation system integrates seamlessly with:
- **Soil Analysis:** Fetches soil data automatically
- **Sensor Readings:** Uses temperature and humidity from sensors
- **Database:** Calculates averages across all records

## Troubleshooting

### Model Not Loading
- Check if `crop_model.pkl` exists in `backend/` folder
- Verify scikit-learn is installed: `pip list | grep scikit`

### No Data for Auto-Analysis
- Ensure you have soil analysis records in your database
- Add sensor readings for better accuracy
- Check database connection

### API Errors
- Ensure backend is running: `uvicorn main:app --reload`
- Check console for error messages
- Verify input values are within valid ranges

### Frontend Issues
- Check browser console for errors
- Verify backend URL is correct (http://localhost:8000)
- Ensure CORS is properly configured

## Future Enhancements
- Add actual crop images instead of emojis
- Include regional crop database
- Add seasonal recommendations
- Integrate weather forecast data
- Add historical yield predictions
- Mobile app integration
- Export recommendations as PDF

## Support
For issues or questions, refer to the main Smart Irrigation System documentation.
