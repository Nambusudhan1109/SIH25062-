-- SQL Schema for Soil Analysis and Crop Recommendations
-- Run this in your Supabase SQL Editor
-- Compatible with existing database schema

-- Create sequences for auto-increment IDs
CREATE SEQUENCE IF NOT EXISTS soil_analysis_analysis_id_seq;
CREATE SEQUENCE IF NOT EXISTS crop_recommendations_recommendation_id_seq;

-- Create soil_analysis table
CREATE TABLE IF NOT EXISTS public.soil_analysis (
    analysis_id integer NOT NULL DEFAULT nextval('soil_analysis_analysis_id_seq'::regclass),
    land_id integer,
    ph_level double precision,
    moisture_level double precision,
    nitrogen double precision,
    phosphorus double precision,
    potassium double precision,
    organic_matter double precision,
    recorded_at timestamp with time zone DEFAULT now(),
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    CONSTRAINT soil_analysis_pkey PRIMARY KEY (analysis_id),
    CONSTRAINT soil_analysis_land_id_fkey FOREIGN KEY (land_id) REFERENCES public.land(land_id) ON DELETE CASCADE
);

-- Create crop_recommendations table
CREATE TABLE IF NOT EXISTS public.crop_recommendations (
    recommendation_id integer NOT NULL DEFAULT nextval('crop_recommendations_recommendation_id_seq'::regclass),
    land_id integer,
    crop_name character varying(255),
    crop_type character varying(100),
    suitability_score double precision,
    growth_duration_days integer,
    estimated_yield character varying(100),
    market_price character varying(100),
    image_url text,
    description text,
    is_optimal boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    CONSTRAINT crop_recommendations_pkey PRIMARY KEY (recommendation_id),
    CONSTRAINT crop_recommendations_land_id_fkey FOREIGN KEY (land_id) REFERENCES public.land(land_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_soil_analysis_land_id ON public.soil_analysis(land_id);
CREATE INDEX IF NOT EXISTS idx_soil_analysis_recorded_at ON public.soil_analysis(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_crop_recommendations_land_id ON public.crop_recommendations(land_id);
CREATE INDEX IF NOT EXISTS idx_crop_recommendations_suitability ON public.crop_recommendations(suitability_score DESC);
CREATE INDEX IF NOT EXISTS idx_crop_recommendations_optimal ON public.crop_recommendations(is_optimal);

-- Enable Row Level Security (RLS)
ALTER TABLE public.soil_analysis ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_recommendations ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Enable read access for all users" ON public.soil_analysis;
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON public.soil_analysis;
DROP POLICY IF EXISTS "Enable update for authenticated users" ON public.soil_analysis;
DROP POLICY IF EXISTS "Enable delete for authenticated users" ON public.soil_analysis;

DROP POLICY IF EXISTS "Enable read access for all users" ON public.crop_recommendations;
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON public.crop_recommendations;
DROP POLICY IF EXISTS "Enable update for authenticated users" ON public.crop_recommendations;
DROP POLICY IF EXISTS "Enable delete for authenticated users" ON public.crop_recommendations;

-- Create RLS policies (permissive for development - adjust for production)
CREATE POLICY "Enable read access for all users" ON public.soil_analysis FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON public.soil_analysis FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON public.soil_analysis FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON public.soil_analysis FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON public.crop_recommendations FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users" ON public.crop_recommendations FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for authenticated users" ON public.crop_recommendations FOR UPDATE USING (true);
CREATE POLICY "Enable delete for authenticated users" ON public.crop_recommendations FOR DELETE USING (true);

-- Sample data insertion (optional - comment out if not needed)
-- IMPORTANT: Check which land_id values exist in your 'land' table first!
-- Run this query to see your existing land IDs: SELECT land_id FROM public.land;
-- Then adjust the INSERT statements below to match your existing land_id values.

-- Insert sample soil analysis data
INSERT INTO public.soil_analysis (land_id, ph_level, moisture_level, nitrogen, phosphorus, potassium, organic_matter)
VALUES 
    (1, 7.2, 38, 75, 55, 85, 4.0),
    (2, 6.5, 45, 70, 65, 80, 3.2),
    (3, 6.8, 42, 80, 60, 90, 3.5),
    (4, 7.0, 40, 82, 58, 87, 3.7),
    (5, 6.6, 46, 76, 62, 85, 3.3),
    (8, 6.9, 44, 78, 62, 88, 3.8)
ON CONFLICT DO NOTHING;  -- Skip if data already exists

-- Insert sample crop recommendations
INSERT INTO public.crop_recommendations (land_id, crop_name, crop_type, suitability_score, growth_duration_days, estimated_yield, market_price, image_url, description, is_optimal)
VALUES 
    -- Recommendations for land_id = 3
    (3, 'Winter Wheat', 'Cereal', 95, 120, 'High Yield', '$250/Ton', 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&q=80&w=1000', 'Winter wheat is highly suitable for this soil type with excellent pH levels and NPK balance.', true),
    (3, 'Rice', 'Wetland', 88, 135, 'Medium-High', '$280/Ton', 'https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=1000', 'Paddy rice cultivation is compatible with current moisture levels and soil composition.', true),
    (3, 'Sweet Corn', 'Organic', 82, 90, 'Medium', '$340/Ton', 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&q=80&w=1000', 'Sweet corn offers good returns with moderate soil requirements. Suitable as an alternative cash crop with shorter growing season.', false),
    -- Recommendations for land_id = 4
    (4, 'Barley', 'Cereal', 93, 100, 'High', '$220/Ton', 'https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&q=80&w=1000', 'Barley thrives in these conditions with excellent drainage and nutrient levels.', true),
    (4, 'Soybeans', 'Legume', 89, 120, 'High', '$320/Ton', 'https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&q=80&w=1000', 'Soybeans are excellent for nitrogen fixation and have good market demand.', true),
    (4, 'Canola', 'Oilseed', 84, 95, 'Medium-High', '$360/Ton', 'https://images.unsplash.com/photo-1597848212624-e450c4b55d5d?auto=format&fit=crop&q=80&w=1000', 'Canola offers good yields with moderate water needs and strong market prices.', false),
    -- Recommendations for land_id = 8
    (8, 'Oats', 'Cereal', 91, 100, 'High', '$220/Ton', 'https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&q=80&w=1000', 'Oats thrive in these conditions with excellent drainage and nutrient levels.', true),
    (8, 'Sunflower', 'Oilseed', 85, 110, 'Medium-High', '$380/Ton', 'https://images.unsplash.com/photo-1597848212624-e450c4b55d5d?auto=format&fit=crop&q=80&w=1000', 'Sunflower is a good cash crop option with moderate water requirements.', false)
ON CONFLICT DO NOTHING;  -- Skip if data already exists

-- ==========================================
-- SETUP INSTRUCTIONS
-- ==========================================
-- 
-- 1. Make sure you have 'land' records in your database
--    Run this to check: SELECT land_id, land_name FROM public.land;
-- 
-- 2. Open your Supabase project dashboard
--    URL: https://supabase.com/dashboard/project/enjjjqprgihcsmubvxyh
-- 
-- 3. Go to SQL Editor and create a new query
-- 
-- 4. Copy and paste this entire file and click "Run"
-- 
-- 5. Verify the tables were created:
--    - Go to Table Editor
--    - Check for 'soil_analysis' and 'crop_recommendations' tables
-- 
-- 6. Test in your app:
--    - Navigate to: http://localhost:5173/analysis/L-3
--    - Should display soil data and crop recommendations
-- 
-- 7. Adjust sample data:
--    - If you get foreign key errors, update the land_id values above
--    - Use land_id values that exist in your 'land' table
-- 
-- The RLS policies are permissive (allow all) - tighten for production!
-- You can use seedSoilAnalysisData() function in supabaseService.ts to add more data programmatically
--
-- ==========================================
