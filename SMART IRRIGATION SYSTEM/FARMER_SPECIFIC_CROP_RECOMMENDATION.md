# Farmer-Specific Crop Recommendation Feature

## Overview
The crop recommendation system now supports farmer-specific personalized recommendations. Each farmer can see AI-powered crop suggestions based exclusively on their own lands' soil and sensor data.

## Features

### 1. **Farmer Selector Dropdown**
- Located in the Auto Analysis tab
- Shows all registered farmers with their IDs
- Default option: "All Farmers (Global Analysis)" - analyzes all lands in database
- When farmer selected: Analyzes only that farmer's lands

### 2. **Personalized Analysis**
- Filters soil analysis records by farmer's lands
- Filters sensor readings by farmer's lands
- Calculates averages from farmer's data only
- Returns top 5 crop recommendations specific to farmer

### 3. **Visual Farmer Information Display**
- Displays when farmer-specific analysis is performed
- Shows:
  - **Farmer ID**: The selected farmer's unique identifier
  - **Total Lands**: Number of lands owned by the farmer
  - **Lands**: Comma-separated list of land names

## API Endpoints

### Get Farmers List
```http
GET /api/farmers/list
```

**Response:**
```json
{
  "farmers": [
    {
      "farmer_id": 1,
      "name": "Rajesh Kumar"
    },
    {
      "farmer_id": 2,
      "name": "Priya Sharma"
    }
  ]
}
```

### Farmer-Specific Auto Analysis
```http
GET /api/crop-recommendation/auto-analyze-farmer/{farmer_id}
```

**Parameters:**
- `farmer_id` (path parameter): The ID of the farmer

**Response:**
```json
{
  "analysis_type": "Farmer-Specific Auto-Analysis",
  "farmer_id": 1,
  "total_lands": 3,
  "land_names": ["North Field", "South Field", "East Orchard"],
  "total_soil_records": 15,
  "total_sensor_readings": 120,
  "recommended_crop": "rice",
  "confidence": 89.45,
  "top_5_recommendations": [
    {
      "rank": 1,
      "crop_name": "rice",
      "probability": 89.45
    },
    {
      "rank": 2,
      "crop_name": "wheat",
      "probability": 85.23
    }
  ],
  "average_parameters": {
    "nitrogen": 45.6,
    "phosphorus": 38.2,
    "potassium": 42.8,
    "temperature": 28.5,
    "humidity": 75.3,
    "ph_level": 6.8,
    "rainfall": 120.5
  }
}
```

## Database Schema Relationships

```
farm table
├── farmer_id (primary key)
└── name

land table
├── land_id (primary key)
├── farmer_id (foreign key → farm.farmer_id)
└── name

soil_analysis table
├── analysis_id (primary key)
├── land_id (foreign key → land.land_id)
├── nitrogen
├── phosphorus
├── potassium
└── ph_level

sensor table
├── sensor_id (primary key)
└── land_id (foreign key → land.land_id)

sensor_readings table
├── reading_id (primary key)
├── sensor_id (foreign key → sensor.sensor_id)
├── temperature
└── moisture (used as humidity)
```

## How It Works

### Backend Logic
1. **Fetch Farmer's Lands**
   - Query `land` table filtered by `farmer_id`
   - Get all `land_id` values for the farmer

2. **Get Soil Analysis Data**
   - Query `soil_analysis` table
   - Filter by farmer's `land_id` list
   - Calculate averages: N, P, K, pH

3. **Get Sensor Data**
   - Query `sensor` table to get farmer's sensors
   - Join with `sensor_readings` table
   - Calculate averages: temperature, humidity (moisture)

4. **Run ML Model**
   - Combine averages: [N, P, K, temperature, humidity, pH, rainfall]
   - Predict using Random Forest model
   - Return top 5 crops with confidence scores

### Frontend Flow
1. **Page Load**
   - Fetch farmers list from `/api/farmers/list`
   - Populate dropdown with farmer names and IDs

2. **Farmer Selection**
   - User selects farmer from dropdown
   - `selectedFarmer` state updated with farmer_id

3. **Start Auto Analysis**
   - Button click triggers `handleAutoAnalyze()`
   - If `selectedFarmer` is null → Global analysis (all lands)
   - If `selectedFarmer` has value → Farmer-specific analysis

4. **Display Results**
   - If farmer-specific: Show farmer info card (ID, lands, count)
   - Display top recommended crop with emoji
   - Show top 5 recommendations with images
   - Display average parameters used

## Usage Instructions

### For All Farmers Analysis (Default)
1. Navigate to Crop Recommendation page
2. Stay on "Auto Analysis" tab
3. Leave dropdown at "All Farmers (Global Analysis)"
4. Click "🚀 Start Auto Analysis"
5. View recommendations based on all database records

### For Individual Farmer Analysis
1. Navigate to Crop Recommendation page
2. Stay on "Auto Analysis" tab
3. Select farmer from dropdown (e.g., "Rajesh Kumar (ID: 1)")
4. Click "🚀 Start Auto Analysis"
5. View personalized recommendations
6. See farmer information card showing:
   - Farmer ID
   - Number of lands owned
   - Names of all lands
7. Recommendations based only on selected farmer's data

## Visual Components

### Farmer Selector
```tsx
<select value={selectedFarmer || ''}>
  <option value="">All Farmers (Global Analysis)</option>
  <option value="1">Rajesh Kumar (ID: 1)</option>
  <option value="2">Priya Sharma (ID: 2)</option>
</select>
```

### Farmer Information Card
- **Background**: Blue gradient (from-blue-50 to-indigo-50)
- **Border**: 2px blue border
- **Layout**: 3-column grid on desktop
- **Content**: Farmer ID, Total Lands, Land Names

### Crop Display
- Top recommendation with large emoji (9xl size)
- Confidence score with color coding
- Top 5 list with rank badges and emojis
- Parameter cards with color gradients

## Testing Checklist

### Backend Testing
- [ ] `/api/farmers/list` returns all farmers
- [ ] `/api/crop-recommendation/auto-analyze-farmer/1` works for valid farmer
- [ ] Returns 404 for non-existent farmer
- [ ] Correctly filters data by farmer's lands
- [ ] Averages calculated correctly

### Frontend Testing
- [ ] Dropdown populates with farmers on page load
- [ ] Selecting farmer updates state
- [ ] Global analysis works (no farmer selected)
- [ ] Farmer-specific analysis works (farmer selected)
- [ ] Farmer info card displays correctly
- [ ] Results display with crop images
- [ ] No console errors

### Integration Testing
- [ ] Test with multiple farmers
- [ ] Test farmer with single land
- [ ] Test farmer with multiple lands
- [ ] Verify data isolation between farmers
- [ ] Check average calculations accuracy

## Configuration

### Backend Configuration
- **Model File**: `backend/crop_model.pkl`
- **API Base URL**: `http://localhost:8000`
- **Database**: Supabase (configured in `backend/main.py`)

### Frontend Configuration
- **API Base URL**: `http://localhost:8000` (hardcoded in fetch calls)
- **Crop Images**: Emoji-based mapping (22 crops)
- **Page Route**: `/crop-recommendation`

## Error Handling

### Backend Errors
- **No Data Found**: Returns 404 if farmer has no lands
- **No Soil/Sensor Data**: Returns 404 if no records found
- **Invalid Farmer ID**: Returns 404 for non-existent farmer
- **Model Error**: Returns 500 with error message

### Frontend Errors
- **Network Error**: Displays error message below button
- **Empty Response**: Shows "No data" message
- **Invalid Data**: Console error logged

## Best Practices

### For Farmers
- Ensure at least one land is registered
- Add soil analysis records regularly
- Install sensors for accurate temperature/humidity readings
- Keep sensor data up-to-date

### For Administrators
- Verify all farmer-land relationships in database
- Check soil_analysis records completeness
- Monitor sensor readings freshness
- Review recommendation accuracy

### For Developers
- Always test with real farmer data
- Verify database relationships
- Check average calculations
- Monitor API response times
- Keep model updated with latest training data

## Troubleshooting

### "No farmers found" in dropdown
- Check if `farm` table has records
- Verify `/api/farmers/list` endpoint response
- Check browser console for fetch errors

### "No data found for farmer" error
- Verify farmer has lands in `land` table
- Check soil_analysis records exist for farmer's lands
- Verify sensor readings exist for farmer's sensors

### Incorrect recommendations
- Check if soil data is current (not outdated)
- Verify sensor readings are accurate
- Ensure pH values are in valid range (0-14)
- Check N, P, K values are realistic

### Farmer info not displaying
- Verify farmer_id is in API response
- Check if `autoAnalysis.farmer_id` exists
- Inspect browser developer tools for rendering issues

## Future Enhancements

### Potential Features
1. **Historical Tracking**: Show past recommendations for farmer
2. **Comparison View**: Compare current vs previous analysis
3. **Land-Level Details**: Break down by individual lands
4. **Seasonal Recommendations**: Factor in current season
5. **Market Price Integration**: Show expected profits
6. **Weather Forecast**: Include upcoming weather predictions
7. **Crop Rotation Suggestions**: Recommend rotation patterns
8. **Export Reports**: PDF download of recommendations

### Technical Improvements
1. **Caching**: Cache farmer data to reduce database queries
2. **Real-time Updates**: WebSocket for live sensor data
3. **Batch Processing**: Analyze all farmers at once
4. **Performance Optimization**: Index database tables
5. **API Rate Limiting**: Prevent abuse
6. **Authentication**: Farmer login/JWT tokens
7. **Mobile App**: Native iOS/Android apps
8. **Multi-language Support**: Translations

## Support

For issues or questions:
1. Check database schema documentation
2. Review API endpoint guide
3. Inspect browser console for errors
4. Check backend logs for API errors
5. Verify Supabase connection
6. Test with Postman/Insomnia first

## Version History

### v1.2.0 (Current)
- ✅ Added farmer-specific filtering
- ✅ Created farmers list endpoint
- ✅ Added farmer selector dropdown
- ✅ Implemented farmer info display card
- ✅ Updated AutoAnalysisResult interface

### v1.1.0
- ✅ Auto-analysis with database averages
- ✅ Crop image emojis (22 varieties)
- ✅ Visual parameter display
- ✅ Top 5 recommendations list

### v1.0.0
- ✅ Basic ML model integration
- ✅ Manual input prediction
- ✅ Land-specific prediction
- ✅ Model info endpoint

## License
Part of Smart Irrigation System - SIH25062
