from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from typing import Optional
from supabase import create_client, Client
from pydantic import BaseModel
import joblib
import numpy as np
import warnings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio
warnings.filterwarnings("ignore")

app = FastAPI(title="Smart Irrigation System API", version="1.0.0")

# Initialize scheduler for automatic refresh
scheduler = AsyncIOScheduler()

# Cache for dashboard statistics (refreshed every hour)
cache = {
    "last_refresh": None,
    "dashboard_stats": None,
    "sensor_status": None
}

# Load Crop Recommendation Model
try:
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "crop_model.pkl")
    crop_model = joblib.load(MODEL_PATH)
    print(f"✓ Crop recommendation model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"⚠️ Warning: Could not load crop model: {str(e)}")
    crop_model = None

# Pydantic models for request/response
class CropPredictionRequest(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    land_id: Optional[int] = None

class CropPredictionResponse(BaseModel):
    recommended_crop: str
    confidence: float
    top_3_recommendations: list
    input_parameters: dict

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://enjjjqprgihcsmubvxyh.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_pfFLEoIWFQmHYhjrqIGfrg_LQ5TMG7F")  # Replace with your actual key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

origins = [
    "http://localhost",
    "http://localhost:5173", # Vite Default
    "http://localhost:5174",
    "http://localhost:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== AUTOMATIC REFRESH FUNCTION ====================

async def refresh_system_data():
    """
    Automatic refresh function that runs every 1 hour
    Updates cached data, sensor status, and system health
    """
    try:
        print(f"\n🔄 [AUTO-REFRESH] Starting system refresh at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Refresh dashboard statistics
        try:
            response = supabase.table('land').select('*').execute()
            cache["dashboard_stats"] = {
                "total_lands": len(response.data) if response.data else 0,
                "last_updated": datetime.now().isoformat()
            }
            print(f"✓ Dashboard stats refreshed: {cache['dashboard_stats']['total_lands']} lands found")
        except Exception as e:
            print(f"⚠️ Error refreshing dashboard stats: {str(e)}")
        
        # Refresh sensor status
        try:
            sensor_response = supabase.table('soil_analysis').select('land_id, recorded_at').order('recorded_at', desc=True).limit(100).execute()
            if sensor_response.data:
                cache["sensor_status"] = {
                    "active_sensors": len(set([r['land_id'] for r in sensor_response.data])),
                    "last_reading": sensor_response.data[0]['recorded_at'] if sensor_response.data else None,
                    "last_updated": datetime.now().isoformat()
                }
                print(f"✓ Sensor status refreshed: {cache['sensor_status']['active_sensors']} active sensors")
        except Exception as e:
            print(f"⚠️ Error refreshing sensor status: {str(e)}")
        
        # Update last refresh time
        cache["last_refresh"] = datetime.now().isoformat()
        print(f"✅ [AUTO-REFRESH] Completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
    except Exception as e:
        print(f"❌ [AUTO-REFRESH] Error during refresh: {str(e)}")

# ==================== STARTUP & SHUTDOWN EVENTS ====================

@app.on_event("startup")
async def startup_event():
    """Initialize scheduler and run first refresh on startup"""
    print("🚀 Starting Smart Irrigation System API...")
    
    # Run initial refresh
    await refresh_system_data()
    
    # Schedule automatic refresh every 30 minutes
    scheduler.add_job(
        refresh_system_data,
        'interval',
        minutes=30,  # Runs every 30 minutes
        id='refresh_system_data',
        replace_existing=True
    )
    scheduler.start()
    print("✅ Scheduler started: Auto-refresh every 30 minutes")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler gracefully"""
    scheduler.shutdown()
    print("👋 Scheduler stopped")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Smart Irrigation System API",
        "version": "1.0.0",
        "auto_refresh": {
            "enabled": True,
            "interval": "30 minutes",
            "last_refresh": cache.get("last_refresh"),
            "next_refresh": scheduler.get_job('refresh_system_data').next_run_time.isoformat() if scheduler.get_job('refresh_system_data') else None
        }
    }

# ==================== SOIL ANALYSIS CHART ENDPOINTS ====================

@app.get("/api/soil-analysis/{land_id}/chart-data")
async def get_soil_chart_data(land_id: int):
    """
    Get soil analysis data formatted for charts
    Returns data for bar charts, line charts, and histograms
    """
    try:
        # Fetch latest soil analysis
        response = supabase.table('soil_analysis').select('*').eq('land_id', land_id).order('recorded_at', desc=True).limit(1).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail=f"No soil analysis data found for land_id {land_id}")
        
        soil_data = response.data[0]
        
        # Prepare data for different chart types
        chart_data = {
            "land_id": land_id,
            "recorded_at": soil_data.get('recorded_at'),
            
            # NPK Bar Chart Data
            "npk_bar_chart": [
                {"nutrient": "Nitrogen (N)", "value": soil_data.get('nitrogen', 0), "color": "#15803d"},
                {"nutrient": "Phosphorus (P)", "value": soil_data.get('phosphorus', 0), "color": "#16a34a"},
                {"nutrient": "Potassium (K)", "value": soil_data.get('potassium', 0), "color": "#22c55e"}
            ],
            
            # Soil Health Overview (Radar/Polar Chart Data)
            "soil_health_radar": [
                {"metric": "pH Level", "value": (soil_data.get('ph_level', 0) / 14) * 100, "optimal": 70},
                {"metric": "Moisture", "value": soil_data.get('moisture_level', 0), "optimal": 50},
                {"metric": "Nitrogen", "value": soil_data.get('nitrogen', 0), "optimal": 80},
                {"metric": "Phosphorus", "value": soil_data.get('phosphorus', 0), "optimal": 65},
                {"metric": "Potassium", "value": soil_data.get('potassium', 0), "optimal": 85},
                {"metric": "Organic Matter", "value": soil_data.get('organic_matter', 0) * 10, "optimal": 40}
            ],
            
            # Comparison with Optimal Values
            "comparison_chart": [
                {
                    "parameter": "pH",
                    "current": soil_data.get('ph_level', 0),
                    "optimal_min": 6.0,
                    "optimal_max": 7.5
                },
                {
                    "parameter": "Moisture",
                    "current": soil_data.get('moisture_level', 0),
                    "optimal_min": 30,
                    "optimal_max": 60
                },
                {
                    "parameter": "N",
                    "current": soil_data.get('nitrogen', 0),
                    "optimal_min": 70,
                    "optimal_max": 90
                },
                {
                    "parameter": "P",
                    "current": soil_data.get('phosphorus', 0),
                    "optimal_min": 50,
                    "optimal_max": 70
                },
                {
                    "parameter": "K",
                    "current": soil_data.get('potassium', 0),
                    "optimal_min": 75,
                    "optimal_max": 95
                }
            ],
            
            # Raw values
            "raw_data": {
                "ph_level": soil_data.get('ph_level', 0),
                "moisture_level": soil_data.get('moisture_level', 0),
                "nitrogen": soil_data.get('nitrogen', 0),
                "phosphorus": soil_data.get('phosphorus', 0),
                "potassium": soil_data.get('potassium', 0),
                "organic_matter": soil_data.get('organic_matter', 0)
            }
        }
        
        return JSONResponse(content=chart_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chart data: {str(e)}")


@app.get("/api/soil-analysis/{land_id}/history")
async def get_soil_history(land_id: int, limit: int = 10):
    """
    Get historical soil analysis data for trend charts
    """
    try:
        response = supabase.table('soil_analysis').select('*').eq('land_id', land_id).order('recorded_at', desc=True).limit(limit).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No historical data found for land_id {land_id}")
        
        # Reverse to show oldest first
        history_data = list(reversed(response.data))
        
        # Format for line chart
        trend_data = {
            "land_id": land_id,
            "data_points": len(history_data),
            "timeline": [
                {
                    "date": record.get('recorded_at'),
                    "ph_level": record.get('ph_level', 0),
                    "moisture": record.get('moisture_level', 0),
                    "nitrogen": record.get('nitrogen', 0),
                    "phosphorus": record.get('phosphorus', 0),
                    "potassium": record.get('potassium', 0),
                    "organic_matter": record.get('organic_matter', 0)
                }
                for record in history_data
            ]
        }
        
        return JSONResponse(content=trend_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@app.get("/api/crop-recommendations/{land_id}/chart-data")
async def get_crop_recommendations_chart(land_id: int):
    """
    Get crop recommendations formatted for charts
    """
    try:
        response = supabase.table('crop_recommendations').select('*').eq('land_id', land_id).order('suitability_score', desc=True).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No crop recommendations found for land_id {land_id}")
        
        # Format for horizontal bar chart
        recommendations_chart = {
            "land_id": land_id,
            "crops": [
                {
                    "crop_name": rec.get('crop_name'),
                    "suitability_score": rec.get('suitability_score', 0),
                    "growth_days": rec.get('growth_duration_days', 0),
                    "is_optimal": rec.get('is_optimal', False),
                    "crop_type": rec.get('crop_type', 'Other')
                }
                for rec in response.data
            ]
        }
        
        return JSONResponse(content=recommendations_chart)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crop recommendations: {str(e)}")


@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """
    Get overall statistics for dashboard charts
    """
    try:
        # Get counts from different tables
        farms_response = supabase.table('farm').select('farmer_id', count='exact').execute()
        lands_response = supabase.table('land').select('land_id', count='exact').execute()
        crops_response = supabase.table('crop').select('crop_id', count='exact').execute()
        sensors_response = supabase.table('sensor').select('sensor_id', count='exact').execute()
        readings_response = supabase.table('sensor_readings').select('reading_id', count='exact').execute()
        
        stats = {
            "total_farmers": farms_response.count or 0,
            "total_lands": lands_response.count or 0,
            "total_crops": crops_response.count or 0,
            "total_sensors": sensors_response.count or 0,
            "total_readings": readings_response.count or 0
        }
        
        return JSONResponse(content=stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


# ==================== SENSOR AVAILABILITY ENDPOINTS ====================

@app.get("/api/sensors/availability/{land_id}")
async def get_sensor_availability(land_id: int):
    """
    Get sensor availability and distribution by type for a specific land
    """
    try:
        # Get sensors for this land
        response = supabase.table('sensor').select('*, land(land_name)').eq('land_id', land_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"No sensors found for land_id {land_id}")
        
        # Count sensors by type
        sensor_types = {}
        for sensor in response.data:
            sensor_type = sensor.get('sensor_type', 'Unknown')
            sensor_types[sensor_type] = sensor_types.get(sensor_type, 0) + 1
        
        # Format for chart
        chart_data = {
            "land_id": land_id,
            "land_name": response.data[0].get('land', {}).get('land_name', 'Unknown'),
            "total_sensors": len(response.data),
            "sensors_by_type": [
                {
                    "sensor_type": sensor_type,
                    "count": count,
                    "percentage": round((count / len(response.data)) * 100, 1)
                }
                for sensor_type, count in sensor_types.items()
            ],
            "sensors": [
                {
                    "sensor_id": s.get('sensor_id'),
                    "sensor_type": s.get('sensor_type'),
                    "status": "Active"
                }
                for s in response.data
            ]
        }
        
        return JSONResponse(content=chart_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor availability: {str(e)}")


@app.get("/api/sensors/all-availability")
async def get_all_sensor_availability():
    """
    Get sensor availability across all lands
    """
    try:
        # Get all sensors with land info
        response = supabase.table('sensor').select('*, land(land_name, land_id)').execute()
        
        if not response.data:
            return JSONResponse(content={
                "total_sensors": 0,
                "sensors_by_type": [],
                "sensors_by_land": []
            })
        
        # Count by type
        sensor_types = {}
        for sensor in response.data:
            sensor_type = sensor.get('sensor_type', 'Unknown')
            sensor_types[sensor_type] = sensor_types.get(sensor_type, 0) + 1
        
        # Count by land
        sensors_by_land = {}
        for sensor in response.data:
            land_id = sensor.get('land_id')
            land_name = sensor.get('land', {}).get('land_name', f'Land {land_id}')
            if land_id:
                key = f"{land_name} (ID: {land_id})"
                sensors_by_land[key] = sensors_by_land.get(key, 0) + 1
        
        chart_data = {
            "total_sensors": len(response.data),
            "sensors_by_type": [
                {
                    "sensor_type": sensor_type,
                    "count": count,
                    "percentage": round((count / len(response.data)) * 100, 1),
                    "color": f"#{hash(sensor_type) % 0xFFFFFF:06x}"
                }
                for sensor_type, count in sorted(sensor_types.items(), key=lambda x: x[1], reverse=True)
            ],
            "sensors_by_land": [
                {
                    "land": land,
                    "count": count
                }
                for land, count in sorted(sensors_by_land.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
        }
        
        return JSONResponse(content=chart_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor availability: {str(e)}")


# ==================== WATER LEVELS ENDPOINTS ====================

@app.get("/api/water-levels/{land_id}")
async def get_water_levels_by_land(land_id: int):
    """
    Get water levels for sensors on a specific land
    """
    try:
        # Get sensors for this land
        sensors_response = supabase.table('sensor').select('sensor_id, sensor_type').eq('land_id', land_id).execute()
        
        if not sensors_response.data:
            raise HTTPException(status_code=404, detail=f"No sensors found for land_id {land_id}")
        
        sensor_ids = [s['sensor_id'] for s in sensors_response.data]
        
        # Get water resource data for these sensors
        water_response = supabase.table('water_resource').select('*').in_('sensor_id', sensor_ids).execute()
        
        water_levels_data = []
        for water in water_response.data:
            sensor_id = water.get('sensor_id')
            sensor_type = next((s['sensor_type'] for s in sensors_response.data if s['sensor_id'] == sensor_id), 'Unknown')
            water_levels_data.append({
                "sensor_id": sensor_id,
                "sensor_type": sensor_type,
                "water_level": water.get('water_level', 0)
            })
        
        chart_data = {
            "land_id": land_id,
            "water_levels": water_levels_data,
            "average_water_level": round(sum(w['water_level'] for w in water_levels_data) / len(water_levels_data), 2) if water_levels_data else 0
        }
        
        return JSONResponse(content=chart_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching water levels: {str(e)}")


@app.get("/api/water-levels/all")
async def get_all_water_levels():
    """
    Get water levels across all sensors
    """
    try:
        # Get all water resources with sensor info
        response = supabase.table('water_resource').select('*, sensor(sensor_type, land_id, land(land_name))').execute()
        
        if not response.data:
            return JSONResponse(content={
                "total_sensors": 0,
                "water_levels": [],
                "average_water_level": 0
            })
        
        water_levels = [
            {
                "sensor_id": w.get('sensor_id'),
                "sensor_type": w.get('sensor', {}).get('sensor_type', 'Unknown'),
                "land_id": w.get('sensor', {}).get('land_id'),
                "land_name": w.get('sensor', {}).get('land', {}).get('land_name', 'Unknown'),
                "water_level": w.get('water_level', 0),
                "status": "Normal" if 30 <= w.get('water_level', 0) <= 80 else ("Low" if w.get('water_level', 0) < 30 else "High")
            }
            for w in response.data
        ]
        
        avg_level = round(sum(w['water_level'] for w in water_levels) / len(water_levels), 2) if water_levels else 0
        
        chart_data = {
            "total_sensors": len(water_levels),
            "water_levels": water_levels,
            "average_water_level": avg_level,
            "by_status": {
                "low": len([w for w in water_levels if w['status'] == 'Low']),
                "normal": len([w for w in water_levels if w['status'] == 'Normal']),
                "high": len([w for w in water_levels if w['status'] == 'High'])
            }
        }
        
        return JSONResponse(content=chart_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching water levels: {str(e)}")


# ==================== SENSOR READINGS ANALYSIS ENDPOINTS ====================

@app.get("/api/sensor-readings/analysis/{land_id}")
async def get_sensor_readings_analysis(land_id: int, limit: int = 50):
    """
    Get sensor readings analysis (moisture & temperature trends) for a land
    """
    try:
        # Get sensors for this land
        sensors_response = supabase.table('sensor').select('sensor_id, sensor_type').eq('land_id', land_id).execute()
        
        if not sensors_response.data:
            raise HTTPException(status_code=404, detail=f"No sensors found for land_id {land_id}")
        
        sensor_ids = [s['sensor_id'] for s in sensors_response.data]
        
        # Get recent readings for these sensors
        readings_response = supabase.table('sensor_readings').select('*').in_('sensor_id', sensor_ids).order('recorded_at', desc=True).limit(limit).execute()
        
        if not readings_response.data:
            raise HTTPException(status_code=404, detail=f"No sensor readings found for land_id {land_id}")
        
        # Process data for charts
        readings = sorted(readings_response.data, key=lambda x: x.get('recorded_at', ''))
        
        moisture_data = []
        temperature_data = []
        
        for reading in readings:
            recorded_at = reading.get('recorded_at', '')
            moisture_data.append({
                "timestamp": recorded_at,
                "value": reading.get('moisture', 0),
                "sensor_id": reading.get('sensor_id')
            })
            temperature_data.append({
                "timestamp": recorded_at,
                "value": reading.get('temperature', 0),
                "sensor_id": reading.get('sensor_id')
            })
        
        # Calculate statistics
        moisture_values = [r.get('moisture', 0) for r in readings_response.data]
        temperature_values = [r.get('temperature', 0) for r in readings_response.data]
        
        chart_data = {
            "land_id": land_id,
            "moisture_trend": moisture_data[-20:],  # Last 20 readings
            "temperature_trend": temperature_data[-20:],
            "statistics": {
                "moisture": {
                    "average": round(sum(moisture_values) / len(moisture_values), 2) if moisture_values else 0,
                    "min": min(moisture_values) if moisture_values else 0,
                    "max": max(moisture_values) if moisture_values else 0
                },
                "temperature": {
                    "average": round(sum(temperature_values) / len(temperature_values), 2) if temperature_values else 0,
                    "min": min(temperature_values) if temperature_values else 0,
                    "max": max(temperature_values) if temperature_values else 0
                }
            },
            "total_readings": len(readings_response.data)
        }
        
        return JSONResponse(content=chart_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor readings analysis: {str(e)}")


# ==================== CROP RECOMMENDATION ML MODEL ENDPOINTS ====================

@app.post("/api/crop-recommendation/predict")
async def predict_crop(request: CropPredictionRequest):
    """
    Predict the best crop based on soil parameters and environmental conditions
    Uses Random Forest ML model trained on agricultural data
    """
    try:
        if crop_model is None:
            raise HTTPException(status_code=503, detail="Crop recommendation model not available")
        
        # Prepare input data
        input_data = np.array([[
            request.N,
            request.P,
            request.K,
            request.temperature,
            request.humidity,
            request.ph,
            request.rainfall
        ]])
        
        # Make prediction
        prediction = crop_model.predict(input_data)[0]
        prediction_proba = crop_model.predict_proba(input_data)[0]
        confidence = float(max(prediction_proba) * 100)
        
        # Get top 3 recommendations
        top_indices = prediction_proba.argsort()[-3:][::-1]
        top_3_recommendations = [
            {
                "rank": i + 1,
                "crop_name": crop_model.classes_[idx],
                "probability": float(prediction_proba[idx] * 100)
            }
            for i, idx in enumerate(top_indices)
        ]
        
        # Prepare response
        response_data = {
            "recommended_crop": prediction,
            "confidence": confidence,
            "top_3_recommendations": top_3_recommendations,
            "input_parameters": {
                "nitrogen": request.N,
                "phosphorus": request.P,
                "potassium": request.K,
                "temperature": request.temperature,
                "humidity": request.humidity,
                "ph": request.ph,
                "rainfall": request.rainfall
            }
        }
        
        # If land_id is provided, save recommendation to database
        if request.land_id:
            try:
                # Save to crop_recommendations table
                recommendation_data = {
                    "land_id": request.land_id,
                    "crop_name": prediction,
                    "suitability_score": int(confidence),
                    "is_optimal": confidence > 80,
                    "crop_type": "ML Predicted"
                }
                supabase.table('crop_recommendations').insert(recommendation_data).execute()
                response_data["saved_to_database"] = True
            except Exception as db_error:
                print(f"Warning: Could not save to database: {str(db_error)}")
                response_data["saved_to_database"] = False
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making crop prediction: {str(e)}")


@app.post("/api/crop-recommendation/predict-from-soil/{land_id}")
async def predict_crop_from_soil_analysis(land_id: int):
    """
    Predict crop based on existing soil analysis data for a land
    Automatically fetches soil parameters from database
    """
    try:
        if crop_model is None:
            raise HTTPException(status_code=503, detail="Crop recommendation model not available")
        
        # Fetch latest soil analysis for the land
        soil_response = supabase.table('soil_analysis').select('*').eq('land_id', land_id).order('recorded_at', desc=True).limit(1).execute()
        
        if not soil_response.data:
            raise HTTPException(status_code=404, detail=f"No soil analysis found for land_id {land_id}")
        
        soil_data = soil_response.data[0]
        
        # Fetch sensor readings for temperature and humidity
        sensors_response = supabase.table('sensor').select('sensor_id').eq('land_id', land_id).execute()
        
        if sensors_response.data:
            sensor_ids = [s['sensor_id'] for s in sensors_response.data]
            readings_response = supabase.table('sensor_readings').select('temperature, moisture').in_('sensor_id', sensor_ids).order('recorded_at', desc=True).limit(1).execute()
            
            if readings_response.data:
                temperature = readings_response.data[0].get('temperature', 25.0)
                humidity = readings_response.data[0].get('moisture', 50.0)
            else:
                temperature = 25.0
                humidity = 50.0
        else:
            temperature = 25.0
            humidity = 50.0
        
        # Prepare input (use default rainfall if not available)
        input_data = np.array([[
            soil_data.get('nitrogen', 50),
            soil_data.get('phosphorus', 50),
            soil_data.get('potassium', 50),
            temperature,
            humidity,
            soil_data.get('ph_level', 7.0),
            100.0  # Default rainfall
        ]])
        
        # Make prediction
        prediction = crop_model.predict(input_data)[0]
        prediction_proba = crop_model.predict_proba(input_data)[0]
        confidence = float(max(prediction_proba) * 100)
        
        # Get top 3 recommendations
        top_indices = prediction_proba.argsort()[-3:][::-1]
        top_3_recommendations = [
            {
                "rank": i + 1,
                "crop_name": crop_model.classes_[idx],
                "probability": float(prediction_proba[idx] * 100)
            }
            for i, idx in enumerate(top_indices)
        ]
        
        # Save to database
        try:
            for rec in top_3_recommendations:
                recommendation_data = {
                    "land_id": land_id,
                    "crop_name": rec["crop_name"],
                    "suitability_score": int(rec["probability"]),
                    "is_optimal": rec["probability"] > 80,
                    "crop_type": "ML Predicted"
                }
                supabase.table('crop_recommendations').upsert(recommendation_data).execute()
        except Exception as db_error:
            print(f"Warning: Could not save to database: {str(db_error)}")
        
        response_data = {
            "land_id": land_id,
            "recommended_crop": prediction,
            "confidence": confidence,
            "top_3_recommendations": top_3_recommendations,
            "soil_data_used": {
                "nitrogen": soil_data.get('nitrogen', 50),
                "phosphorus": soil_data.get('phosphorus', 50),
                "potassium": soil_data.get('potassium', 50),
                "ph_level": soil_data.get('ph_level', 7.0),
                "temperature": temperature,
                "humidity": humidity
            }
        }
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting crop from soil data: {str(e)}")


@app.get("/api/crop-recommendation/auto-analyze")
async def auto_analyze_all_lands():
    """
    Automatically fetch all lands, calculate average soil parameters, 
    and provide crop recommendations
    """
    try:
        if crop_model is None:
            raise HTTPException(status_code=503, detail="Crop recommendation model not available")
        
        # Fetch all soil analysis data
        soil_response = supabase.table('soil_analysis').select('*').execute()
        
        if not soil_response.data or len(soil_response.data) == 0:
            raise HTTPException(status_code=404, detail="No soil analysis data found")
        
        # Calculate averages
        total_records = len(soil_response.data)
        avg_nitrogen = sum(s.get('nitrogen', 0) for s in soil_response.data) / total_records
        avg_phosphorus = sum(s.get('phosphorus', 0) for s in soil_response.data) / total_records
        avg_potassium = sum(s.get('potassium', 0) for s in soil_response.data) / total_records
        avg_ph = sum(s.get('ph_level', 0) for s in soil_response.data) / total_records
        
        # Fetch all sensor readings for temperature and humidity
        readings_response = supabase.table('sensor_readings').select('temperature, moisture').order('recorded_at', desc=True).limit(100).execute()
        
        if readings_response.data and len(readings_response.data) > 0:
            avg_temperature = sum(r.get('temperature', 25.0) for r in readings_response.data) / len(readings_response.data)
            avg_humidity = sum(r.get('moisture', 50.0) for r in readings_response.data) / len(readings_response.data)
        else:
            avg_temperature = 25.0
            avg_humidity = 50.0
        
        # Default rainfall (could be added to database in future)
        avg_rainfall = 150.0
        
        # Prepare input for prediction
        input_data = np.array([[
            avg_nitrogen,
            avg_phosphorus,
            avg_potassium,
            avg_temperature,
            avg_humidity,
            avg_ph,
            avg_rainfall
        ]])
        
        # Make prediction
        prediction = crop_model.predict(input_data)[0]
        prediction_proba = crop_model.predict_proba(input_data)[0]
        confidence = float(max(prediction_proba) * 100)
        
        # Get top 5 recommendations
        top_indices = prediction_proba.argsort()[-5:][::-1]
        top_recommendations = [
            {
                "rank": i + 1,
                "crop_name": crop_model.classes_[idx],
                "probability": float(prediction_proba[idx] * 100)
            }
            for i, idx in enumerate(top_indices)
        ]
        
        response_data = {
            "analysis_type": "Auto Analysis - All Lands Average",
            "total_soil_records": total_records,
            "total_sensor_readings": len(readings_response.data) if readings_response.data else 0,
            "recommended_crop": prediction,
            "confidence": confidence,
            "top_5_recommendations": top_recommendations,
            "average_parameters": {
                "nitrogen": round(avg_nitrogen, 2),
                "phosphorus": round(avg_phosphorus, 2),
                "potassium": round(avg_potassium, 2),
                "temperature": round(avg_temperature, 2),
                "humidity": round(avg_humidity, 2),
                "ph_level": round(avg_ph, 2),
                "rainfall": round(avg_rainfall, 2)
            }
        }
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in auto-analysis: {str(e)}")


@app.get("/api/crop-recommendation/auto-analyze-farmer/{farmer_id}")
async def auto_analyze_farmer_lands(farmer_id: int):
    """
    Automatically fetch all lands for specific farmer, calculate average soil parameters, 
    and provide personalized crop recommendations
    """
    try:
        if crop_model is None:
            raise HTTPException(status_code=503, detail="Crop recommendation model not available")
        
        # Get all lands for this farmer
        lands_response = supabase.table('land').select('land_id, land_name').eq('farmer_id', farmer_id).execute()
        
        if not lands_response.data or len(lands_response.data) == 0:
            raise HTTPException(status_code=404, detail=f"No lands found for farmer_id {farmer_id}")
        
        land_ids = [land['land_id'] for land in lands_response.data]
        land_names = [land['land_name'] for land in lands_response.data]
        
        # Fetch soil analysis data for farmer's lands
        soil_response = supabase.table('soil_analysis').select('*').in_('land_id', land_ids).execute()
        
        if not soil_response.data or len(soil_response.data) == 0:
            raise HTTPException(status_code=404, detail=f"No soil analysis data found for farmer_id {farmer_id}")
        
        # Calculate averages for farmer's lands
        total_records = len(soil_response.data)
        avg_nitrogen = sum(s.get('nitrogen', 0) for s in soil_response.data) / total_records
        avg_phosphorus = sum(s.get('phosphorus', 0) for s in soil_response.data) / total_records
        avg_potassium = sum(s.get('potassium', 0) for s in soil_response.data) / total_records
        avg_ph = sum(s.get('ph_level', 0) for s in soil_response.data) / total_records
        
        # Fetch sensor readings for farmer's lands
        sensors_response = supabase.table('sensor').select('sensor_id').in_('land_id', land_ids).execute()
        
        if sensors_response.data and len(sensors_response.data) > 0:
            sensor_ids = [s['sensor_id'] for s in sensors_response.data]
            readings_response = supabase.table('sensor_readings').select('temperature, moisture').in_('sensor_id', sensor_ids).order('recorded_at', desc=True).limit(100).execute()
            
            if readings_response.data and len(readings_response.data) > 0:
                avg_temperature = sum(r.get('temperature', 25.0) for r in readings_response.data) / len(readings_response.data)
                avg_humidity = sum(r.get('moisture', 50.0) for r in readings_response.data) / len(readings_response.data)
                sensor_reading_count = len(readings_response.data)
            else:
                avg_temperature = 25.0
                avg_humidity = 50.0
                sensor_reading_count = 0
        else:
            avg_temperature = 25.0
            avg_humidity = 50.0
            sensor_reading_count = 0
        
        # Default rainfall
        avg_rainfall = 150.0
        
        # Prepare input for prediction
        input_data = np.array([[
            avg_nitrogen,
            avg_phosphorus,
            avg_potassium,
            avg_temperature,
            avg_humidity,
            avg_ph,
            avg_rainfall
        ]])
        
        # Make prediction
        prediction = crop_model.predict(input_data)[0]
        prediction_proba = crop_model.predict_proba(input_data)[0]
        confidence = float(max(prediction_proba) * 100)
        
        # Get top 5 recommendations
        top_indices = prediction_proba.argsort()[-5:][::-1]
        top_recommendations = [
            {
                "rank": i + 1,
                "crop_name": crop_model.classes_[idx],
                "probability": float(prediction_proba[idx] * 100)
            }
            for i, idx in enumerate(top_indices)
        ]
        
        response_data = {
            "analysis_type": f"Farmer-Specific Analysis (Farmer ID: {farmer_id})",
            "farmer_id": farmer_id,
            "total_lands": len(land_ids),
            "land_names": land_names,
            "total_soil_records": total_records,
            "total_sensor_readings": sensor_reading_count,
            "recommended_crop": prediction,
            "confidence": confidence,
            "top_5_recommendations": top_recommendations,
            "average_parameters": {
                "nitrogen": round(avg_nitrogen, 2),
                "phosphorus": round(avg_phosphorus, 2),
                "potassium": round(avg_potassium, 2),
                "temperature": round(avg_temperature, 2),
                "humidity": round(avg_humidity, 2),
                "ph_level": round(avg_ph, 2),
                "rainfall": round(avg_rainfall, 2)
            }
        }
        
        return JSONResponse(content=response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in farmer-specific analysis: {str(e)}")


@app.get("/api/farmers/list")
async def get_farmers_list():
    """
    Get list of all farmers for dropdown selection
    """
    try:
        response = supabase.table('farm').select('farmer_id, name').order('farmer_id').execute()
        
        if not response.data:
            return JSONResponse(content={"farmers": []})
        
        farmers_list = [
            {
                "farmer_id": farmer.get('farmer_id'),
                "name": farmer.get('name', f"Farmer {farmer.get('farmer_id')}")
            }
            for farmer in response.data
        ]
        
        return JSONResponse(content={"farmers": farmers_list})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching farmers list: {str(e)}")


@app.get("/api/crop-recommendation/model-info")
async def get_model_info():
    """
    Get information about the crop recommendation model
    """
    try:
        if crop_model is None:
            return JSONResponse(content={
                "status": "unavailable",
                "message": "Crop recommendation model is not loaded"
            })
        
        model_info = {
            "status": "available",
            "model_type": "Random Forest Classifier",
            "supported_crops": list(crop_model.classes_),
            "total_crops": len(crop_model.classes_),
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
        
        return JSONResponse(content=model_info)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching model info: {str(e)}")
