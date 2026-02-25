import { supabase } from '../lib/supabase';

// Types based on the database schema
export interface Farm {
    farmer_id?: number;
    name: string;
    mobile_number?: string;
    village?: string;
    farm_image?: string;
}

export interface Land {
    land_id?: number;
    farmer_id?: number;
    land_name?: string;
    area_acres?: number;
    soil_type?: string;
    village?: string;
}

export interface Crop {
    crop_id?: number;
    farmer_id?: number;
    growth_stage?: string;
    water_need?: number;
}

export interface Sensor {
    sensor_id?: number;
    farmer_id?: number;
    sensor_type?: string;
    land_id?: number;
}

export interface SensorReading {
    reading_id?: number;
    sensor_id?: number;
    moisture: number;
    temperature: number;
    recorded_at?: string;
}

export interface WaterResource {
    water_id?: number;
    sensor_id?: number;
    water_level?: number;
}

export interface Irrigation {
    event_id?: number;
    crop_id?: number;
    valve_status?: string;
    water_used?: number;
}

export interface IrrigationControl {
    control_id?: number;
    water_id?: number;
    valve_status?: 'OPEN' | 'CLOSED';
    water_used?: number;
}

export interface Weather {
    weather_id?: number;
    sensor_id?: number;
    water_resource?: string;
}

export interface SoilAnalysis {
    analysis_id?: number;
    land_id?: number;
    ph_level?: number;
    moisture_level?: number;
    nitrogen?: number;
    phosphorus?: number;
    potassium?: number;
    organic_matter?: number;
    recorded_at?: string;
    created_at?: string;
}

export interface CropRecommendation {
    recommendation_id?: number;
    land_id?: number;
    crop_name?: string;
    crop_type?: string;
    suitability_score?: number;
    growth_duration_days?: number;
    estimated_yield?: string;
    market_price?: string;
    image_url?: string;
    description?: string;
    is_optimal?: boolean;
}

// ============= FARM (Farmer) CRUD =============
export const farmService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('farm')
            .select('*')
            .order('farmer_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('farm')
            .select('*')
            .eq('farmer_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (farm: Farm) => {
        const { data, error } = await supabase
            .from('farm')
            .insert(farm)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, farm: Partial<Farm>) => {
        const { data, error } = await supabase
            .from('farm')
            .update(farm)
            .eq('farmer_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('farm')
            .delete()
            .eq('farmer_id', id);
        if (error) throw error;
    }
};

// ============= LAND CRUD =============
export const landService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('land')
            .select('*, farm(*)')
            .order('land_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('land')
            .select('*, farm(*)')
            .eq('land_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    getByFarmer: async (farmerId: number) => {
        const { data, error } = await supabase
            .from('land')
            .select('*')
            .eq('farmer_id', farmerId);
        if (error) throw error;
        return data;
    },

    create: async (land: Land) => {
        const { data, error } = await supabase
            .from('land')
            .insert(land)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, land: Partial<Land>) => {
        const { data, error } = await supabase
            .from('land')
            .update(land)
            .eq('land_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('land')
            .delete()
            .eq('land_id', id);
        if (error) throw error;
    }
};

// ============= CROP CRUD =============
export const cropService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('crop')
            .select('*, farm(*)')
            .order('crop_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('crop')
            .select('*, farm(*)')
            .eq('crop_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (crop: Crop) => {
        const { data, error } = await supabase
            .from('crop')
            .insert(crop)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, crop: Partial<Crop>) => {
        const { data, error } = await supabase
            .from('crop')
            .update(crop)
            .eq('crop_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('crop')
            .delete()
            .eq('crop_id', id);
        if (error) throw error;
    }
};

// ============= SENSOR CRUD =============
export const sensorService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('sensor')
            .select('*, land(*)')
            .order('sensor_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('sensor')
            .select('*, land(*)')
            .eq('sensor_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (sensor: Sensor) => {
        const { data, error } = await supabase
            .from('sensor')
            .insert(sensor)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, sensor: Partial<Sensor>) => {
        const { data, error } = await supabase
            .from('sensor')
            .update(sensor)
            .eq('sensor_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('sensor')
            .delete()
            .eq('sensor_id', id);
        if (error) throw error;
    }
};

// ============= SENSOR READINGS CRUD =============
export const sensorReadingService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('sensor_readings')
            .select('*, sensor(*)')
            .order('recorded_at', { ascending: false })
            .limit(100);
        if (error) throw error;
        return data;
    },

    getBySensor: async (sensorId: number, limit = 50) => {
        const { data, error } = await supabase
            .from('sensor_readings')
            .select('*')
            .eq('sensor_id', sensorId)
            .order('recorded_at', { ascending: false })
            .limit(limit);
        if (error) throw error;
        return data;
    },

    create: async (reading: SensorReading) => {
        const { data, error } = await supabase
            .from('sensor_readings')
            .insert(reading)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('sensor_readings')
            .delete()
            .eq('reading_id', id);
        if (error) throw error;
    }
};

// ============= WATER RESOURCE CRUD =============
export const waterResourceService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('water_resource')
            .select('*, sensor(*)')
            .order('water_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('water_resource')
            .select('*, sensor(*)')
            .eq('water_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (resource: WaterResource) => {
        const { data, error } = await supabase
            .from('water_resource')
            .insert(resource)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, resource: Partial<WaterResource>) => {
        const { data, error } = await supabase
            .from('water_resource')
            .update(resource)
            .eq('water_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('water_resource')
            .delete()
            .eq('water_id', id);
        if (error) throw error;
    }
};

// ============= IRRIGATION CRUD =============
export const irrigationService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('irrigation')
            .select('*, crop(*)')
            .order('event_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('irrigation')
            .select('*, crop(*)')
            .eq('event_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (irrigation: Irrigation) => {
        const { data, error } = await supabase
            .from('irrigation')
            .insert(irrigation)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, irrigation: Partial<Irrigation>) => {
        const { data, error } = await supabase
            .from('irrigation')
            .update(irrigation)
            .eq('event_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('irrigation')
            .delete()
            .eq('event_id', id);
        if (error) throw error;
    }
};

// ============= IRRIGATION CONTROL CRUD =============
export const irrigationControlService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('irrigation_control')
            .select('*, water_resource(*)')
            .order('control_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('irrigation_control')
            .select('*, water_resource(*)')
            .eq('control_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (control: IrrigationControl) => {
        const { data, error } = await supabase
            .from('irrigation_control')
            .insert(control)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, control: Partial<IrrigationControl>) => {
        const { data, error } = await supabase
            .from('irrigation_control')
            .update(control)
            .eq('control_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('irrigation_control')
            .delete()
            .eq('control_id', id);
        if (error) throw error;
    }
};

// ============= WEATHER CRUD =============
export const weatherService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('weather')
            .select('*, sensor(*)')
            .order('weather_id', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('weather')
            .select('*, sensor(*)')
            .eq('weather_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    create: async (weather: Weather) => {
        const { data, error } = await supabase
            .from('weather')
            .insert(weather)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, weather: Partial<Weather>) => {
        const { data, error } = await supabase
            .from('weather')
            .update(weather)
            .eq('weather_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('weather')
            .delete()
            .eq('weather_id', id);
        if (error) throw error;
    }
};

// ============= SOIL ANALYSIS CRUD =============
export const soilAnalysisService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('soil_analysis')
            .select('*, land(*)')
            .order('recorded_at', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('soil_analysis')
            .select('*, land(*)')
            .eq('analysis_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    getByLand: async (landId: number) => {
        const { data, error } = await supabase
            .from('soil_analysis')
            .select('*')
            .eq('land_id', landId)
            .order('recorded_at', { ascending: false })
            .limit(1)
            .maybeSingle();
        if (error) throw error;
        return data;
    },

    create: async (analysis: SoilAnalysis) => {
        const { data, error } = await supabase
            .from('soil_analysis')
            .insert(analysis)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, analysis: Partial<SoilAnalysis>) => {
        const { data, error } = await supabase
            .from('soil_analysis')
            .update(analysis)
            .eq('analysis_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('soil_analysis')
            .delete()
            .eq('analysis_id', id);
        if (error) throw error;
    }
};

// ============= CROP RECOMMENDATIONS CRUD =============
export const cropRecommendationService = {
    getAll: async () => {
        const { data, error } = await supabase
            .from('crop_recommendations')
            .select('*, land(*)')
            .order('suitability_score', { ascending: false });
        if (error) throw error;
        return data;
    },

    getById: async (id: number) => {
        const { data, error } = await supabase
            .from('crop_recommendations')
            .select('*, land(*)')
            .eq('recommendation_id', id)
            .single();
        if (error) throw error;
        return data;
    },

    getByLand: async (landId: number) => {
        const { data, error } = await supabase
            .from('crop_recommendations')
            .select('*')
            .eq('land_id', landId)
            .order('suitability_score', { ascending: false });
        if (error) throw error;
        return data;
    },

    getOptimalForLand: async (landId: number) => {
        const { data, error } = await supabase
            .from('crop_recommendations')
            .select('*')
            .eq('land_id', landId)
            .eq('is_optimal', true)
            .order('suitability_score', { ascending: false })
            .limit(3);
        if (error) throw error;
        return data;
    },

    create: async (recommendation: CropRecommendation) => {
        const { data, error } = await supabase
            .from('crop_recommendations')
            .insert(recommendation)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    update: async (id: number, recommendation: Partial<CropRecommendation>) => {
        const { data, error } = await supabase
            .from('crop_recommendations')
            .update(recommendation)
            .eq('recommendation_id', id)
            .select()
            .single();
        if (error) throw error;
        return data;
    },

    delete: async (id: number) => {
        const { error } = await supabase
            .from('crop_recommendations')
            .delete()
            .eq('recommendation_id', id);
        if (error) throw error;
    }
};

// ============= ANALYTICS / STATS =============
export const analyticsService = {
    getDashboardStats: async () => {
        const [farmers, lands, crops, sensors, readings] = await Promise.all([
            supabase.from('farm').select('farmer_id', { count: 'exact', head: true }),
            supabase.from('land').select('land_id', { count: 'exact', head: true }),
            supabase.from('crop').select('crop_id', { count: 'exact', head: true }),
            supabase.from('sensor').select('sensor_id', { count: 'exact', head: true }),
            supabase.from('sensor_readings').select('reading_id', { count: 'exact', head: true })
        ]);

        return {
            totalFarmers: farmers.count || 0,
            totalLands: lands.count || 0,
            totalCrops: crops.count || 0,
            totalSensors: sensors.count || 0,
            totalReadings: readings.count || 0
        };
    },

    getRecentActivity: async () => {
        const { data, error } = await supabase
            .from('sensor_readings')
            .select('*, sensor(sensor_type, land(land_name))')
            .order('recorded_at', { ascending: false })
            .limit(10);
        if (error) throw error;
        return data;
    }
};

// ============= SEED DEMO DATA =============
export const seedDemoData = async () => {
    const demoFarmers: Farm[] = [
        {
            name: 'Rajesh Kumar',
            mobile_number: '+91 98765 43210',
            village: 'Panchgani',
            farm_image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400'
        },
        {
            name: 'Priya Sharma',
            mobile_number: '+91 98765 43211',
            village: 'Mahabaleshwar',
            farm_image: 'https://images.unsplash.com/photo-1566328386401-b2980125f6b4?w=400'
        },
        {
            name: 'Amit Patel',
            mobile_number: '+91 98765 43212',
            village: 'Wai',
            farm_image: 'https://images.unsplash.com/photo-1595656302651-52c04f54affa?w=400'
        },
        {
            name: 'Kavita Deshmukh',
            mobile_number: '+91 98765 43213',
            village: 'Satara',
            farm_image: 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400'
        },
        {
            name: 'Suresh Jadhav',
            mobile_number: '+91 98765 43214',
            village: 'Karad',
            farm_image: 'https://images.unsplash.com/photo-1593113598332-cd288d649433?w=400'
        }
    ];

    const results = [];
    for (const farmer of demoFarmers) {
        try {
            const createdFarmer = await farmService.create(farmer);
            results.push({ success: true, farmer: createdFarmer });
        } catch (error: any) {
            results.push({ success: false, error: error.message, farmer });
        }
    }

    return results;
};

// ============= SEED SOIL ANALYSIS & CROP RECOMMENDATIONS =============
export const seedSoilAnalysisData = async (landId: number) => {
    try {
        // Create sample soil analysis data
        const soilAnalysis: SoilAnalysis = {
            land_id: landId,
            ph_level: 6.8,
            moisture_level: 42,
            nitrogen: 80,
            phosphorus: 60,
            potassium: 90,
            organic_matter: 3.5,
            recorded_at: new Date().toISOString()
        };

        const createdSoilAnalysis = await soilAnalysisService.create(soilAnalysis);

        // Create sample crop recommendations
        const cropRecommendations: CropRecommendation[] = [
            {
                land_id: landId,
                crop_name: 'Winter Wheat',
                crop_type: 'Cereal',
                suitability_score: 95,
                growth_duration_days: 120,
                estimated_yield: 'High Yield',
                market_price: '$250/Ton',
                image_url: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&q=80&w=1000',
                description: 'Winter wheat is highly suitable for this soil type with excellent pH levels and NPK balance.',
                is_optimal: true
            },
            {
                land_id: landId,
                crop_name: 'Rice',
                crop_type: 'Wetland',
                suitability_score: 88,
                growth_duration_days: 135,
                estimated_yield: 'Medium-High',
                market_price: '$280/Ton',
                image_url: 'https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=1000',
                description: 'Paddy rice cultivation is compatible with current moisture levels and soil composition.',
                is_optimal: true
            },
            {
                land_id: landId,
                crop_name: 'Sweet Corn',
                crop_type: 'Organic',
                suitability_score: 82,
                growth_duration_days: 90,
                estimated_yield: 'Medium',
                market_price: '$340/Ton',
                image_url: 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&q=80&w=1000',
                description: 'Sweet corn offers good returns with moderate soil requirements. Suitable as an alternative cash crop with shorter growing season.',
                is_optimal: false
            }
        ];

        const createdRecommendations = [];
        for (const rec of cropRecommendations) {
            const created = await cropRecommendationService.create(rec);
            createdRecommendations.push(created);
        }

        return {
            success: true,
            soilAnalysis: createdSoilAnalysis,
            recommendations: createdRecommendations
        };
    } catch (error: any) {
        console.error('Error seeding soil analysis data:', error);
        return {
            success: false,
            error: error.message
        };
    }
};
