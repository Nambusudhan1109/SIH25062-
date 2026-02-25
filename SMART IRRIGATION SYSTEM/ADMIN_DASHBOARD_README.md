# Admin Dashboard Documentation

## Overview
The Admin Dashboard provides full CRUD (Create, Read, Update, Delete) operations for managing the Smart Irrigation System's database through Supabase.

## Access
- **URL**: `http://localhost:5174/admin`
- **Route**: `/admin`

## Features

### 1. Analytics Dashboard
- **Total Farmers**: Count of all registered farmers
- **Total Lands**: Count of all land parcels
- **Total Crops**: Count of all crops being monitored
- **Total Sensors**: Count of all deployed sensors
- **Sensor Readings**: Total number of sensor readings recorded

### 2. Data Management
The admin can manage the following entities:

#### Farmers (farm table)
- View all farmers
- Add new farmer (name, mobile, village, farm image)
- Edit farmer details
- Delete farmer records

#### Lands (land table)
- View all land parcels with farmer info
- Add new land (farmer_id, land name, area in acres, soil type, village)
- Edit land details
- Delete land records

#### Crops (crop table)
- View all crops with farmer info
- Add new crop (farmer_id, growth stage, water need)
- Edit crop details
- Delete crop records

#### Sensors (sensor table)
- View all sensors with land info
- Add new sensor (farmer_id, sensor type, land_id)
- Edit sensor details
- Delete sensor records

#### Sensor Readings (sensor_readings table)
- View recent sensor readings (last 100)
- Add new readings (sensor_id, moisture %, temperature °C)
- Delete readings
- **Note**: Editing readings is disabled for data integrity

#### Water Resources (water_resource table)
- Manage water resource data
- Track water levels by sensor

#### Irrigation Events (irrigation table)
- Manage irrigation events
- Track water usage per crop

#### Irrigation Controls (irrigation_control table)
- Control valve status (OPEN/CLOSED)
- Monitor water usage

#### Weather (weather table)
- Manage weather data
- Link weather to sensors

## Usage

### Navigate Between Tabs
1. **Analytics**: View dashboard statistics
2. **Manage Data**: Perform CRUD operations

### Managing Data
1. Select entity type from the buttons (Farmers, Lands, Crops, etc.)
2. Click **"Add New"** to create a new record
3. Click **Edit icon** (✏️) to modify existing record
4. Click **Delete icon** (🗑️) to remove record
5. Use **Search** to filter records

### Form Fields
All forms are dynamically generated based on the entity type. Required fields are marked with *.

## Database Schema Integration

The admin dashboard is fully integrated with your Supabase database schema:

```
farm → land → sensor → sensor_readings
  ↓       ↓       ↓
crop   water_resource  weather
  ↓       ↓
irrigation  irrigation_control
```

## Technical Implementation

### Files Created:
1. **`src/services/supabaseService.ts`**: Complete CRUD service layer for all entities
2. **`src/pages/AdminDashboard.tsx`**: Full-featured admin interface
3. **`src/App.tsx`**: Updated with `/admin` route

### Key Features:
- Real-time data from Supabase
- Form validation
- Error handling
- Loading states
- Search and filter functionality
- Responsive design with Tailwind CSS
- Modal-based forms

## Environment Setup
Ensure your `.env` file in the frontend folder contains:
```
VITE_SUPABASE_URL=https://enjjjqprgihcsmubvxyh.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_pfFLEoIWFQmHYhjrqIGfrg_LQ5TMG7F
```

## Security Notes
- Current implementation uses the anon key for demonstration
- For production, implement:
  - Row Level Security (RLS) in Supabase
  - Admin authentication
  - Role-based access control
  - API key rotation

## Next Steps
1. Add authentication middleware for admin routes
2. Implement role-based permissions
3. Add data export functionality (CSV/PDF)
4. Add bulk operations
5. Implement data visualization charts
6. Add activity logs/audit trail
