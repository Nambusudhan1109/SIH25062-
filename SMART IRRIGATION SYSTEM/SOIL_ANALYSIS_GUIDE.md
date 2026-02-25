# Soil Analysis Feature - Setup Guide

## Overview
The Soil Analysis feature provides comprehensive soil health monitoring and crop recommendations based on real-time soil data. This guide will help you set up and use this feature.

## Features
- **Real-time Soil Metrics**: pH levels, moisture content, NPK (Nitrogen, Phosphorus, Potassium) values
- **Dynamic Crop Recommendations**: AI-driven suggestions based on soil analysis
- **Land-specific Analysis**: Each land parcel has its own analysis and recommendations
- **Historical Tracking**: Monitor soil health over time

## Database Setup

### 1. Create Database Tables
Run the SQL script in your Supabase SQL Editor:

```bash
# File location:
database_schema_soil_analysis.sql
```

This will create:
- `soil_analysis` table - stores soil health data
- `crop_recommendations` table - stores crop suggestions
- Necessary indexes for performance
- Row Level Security (RLS) policies

### 2. Configure Your Land IDs
Make sure you have land entries in your database. The URL pattern is `/analysis/L-{land_id}`.

Example:
- `/analysis/L-8` → fetches data for land_id = 8
- `/analysis/L-1` → fetches data for land_id = 1

## Adding Sample Data

### Method 1: Using SQL (Recommended for testing)
The SQL file includes sample INSERT statements. Just adjust the `land_id` values to match your database:

```sql
-- Update the land_id (8) to match your actual land IDs
INSERT INTO soil_analysis (land_id, ph_level, moisture_level, nitrogen, phosphorus, potassium, organic_matter)
VALUES (8, 6.8, 42, 80, 60, 90, 3.5);
```

### Method 2: Using the Service Function
Use the `seedSoilAnalysisData()` function from your frontend:

```typescript
import { seedSoilAnalysisData } from '../services/supabaseService';

// Add data for land_id 8
await seedSoilAnalysisData(8);
```

## Using the Feature

### Accessing Soil Analysis
Navigate to: `http://localhost:5173/analysis/L-{land_id}`

Example: `http://localhost:5173/analysis/L-8`

### What You'll See
1. **Left Panel**: Soil Statistics
   - pH levels with optimal range indicator
   - Moisture percentage
   - NPK nutrient levels
   - Soil insights and recommendations

2. **Center Panel**: Crop Recommendations
   - Top 2 recommendations displayed as cards
   - Third recommendation in expanded view
   - Suitability scores, growth duration, yield estimates
   - Market prices for planning

3. **Right Panel**: Voice Assistant
   - Voice commands for hands-free operation
   - Recent command history

### Refresh Data
Click the "Refresh Sensors" button to reload soil analysis data.

## Database Schema

### soil_analysis Table
| Column | Type | Description |
|--------|------|-------------|
| analysis_id | BIGSERIAL | Primary key |
| land_id | BIGINT | Foreign key to land table |
| ph_level | DECIMAL(4,2) | Soil pH (0-14 scale) |
| moisture_level | DECIMAL(5,2) | Moisture percentage (0-100) |
| nitrogen | DECIMAL(5,2) | Nitrogen percentage |
| phosphorus | DECIMAL(5,2) | Phosphorus percentage |
| potassium | DECIMAL(5,2) | Potassium percentage |
| organic_matter | DECIMAL(5,2) | Organic matter percentage |
| recorded_at | TIMESTAMP | When measurement was taken |

### crop_recommendations Table
| Column | Type | Description |
|--------|------|-------------|
| recommendation_id | BIGSERIAL | Primary key |
| land_id | BIGINT | Foreign key to land table |
| crop_name | VARCHAR(255) | Name of the crop |
| crop_type | VARCHAR(100) | Type/category of crop |
| suitability_score | DECIMAL(5,2) | Score out of 100 |
| growth_duration_days | INTEGER | Days to maturity |
| estimated_yield | VARCHAR(100) | Expected yield description |
| market_price | VARCHAR(100) | Current market price |
| image_url | TEXT | Crop image URL |
| description | TEXT | Detailed recommendation |
| is_optimal | BOOLEAN | Mark as optimal choice |

## Customization

### Adding More Metrics
To add additional soil metrics:

1. Add column to `soil_analysis` table:
```sql
ALTER TABLE soil_analysis ADD COLUMN new_metric DECIMAL(5,2);
```

2. Update TypeScript interface in `supabaseService.ts`:
```typescript
export interface SoilAnalysis {
    // ... existing fields
    new_metric?: number;
}
```

3. Update the UI in `SoilAnalysis.tsx` to display the new metric.

### Customizing Recommendations
Modify the crop recommendation algorithm by:
1. Adjusting suitability scores based on soil conditions
2. Adding more crop varieties to the database
3. Implementing ML models for better predictions

## Troubleshooting

### "No Data Available" Error
- Check if land_id exists in the database
- Verify soil_analysis table has data for that land_id
- Check browser console for detailed error messages

### Data Not Updating
- Click "Refresh Sensors" button
- Check Supabase RLS policies
- Verify network connection to Supabase

### Images Not Loading
- Ensure image URLs are accessible
- Check CORS settings if using custom image hosting

## API Endpoints (Services)

### Soil Analysis
- `soilAnalysisService.getByLand(landId)` - Get latest analysis for a land
- `soilAnalysisService.create(analysis)` - Add new soil analysis
- `soilAnalysisService.update(id, analysis)` - Update existing analysis

### Crop Recommendations
- `cropRecommendationService.getByLand(landId)` - Get all recommendations for a land
- `cropRecommendationService.getOptimalForLand(landId)` - Get only optimal recommendations
- `cropRecommendationService.create(recommendation)` - Add new recommendation

## Future Enhancements
- [ ] Real-time sensor integration
- [ ] Historical trend charts
- [ ] Weather-based recommendations
- [ ] Mobile app support
- [ ] Export reports as PDF
- [ ] Multi-season planning
- [ ] Cost-benefit analysis

## Support
For issues or questions, check the main project README or create an issue in the repository.
