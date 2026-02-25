import React from 'react';

interface NPKData {
    nutrient: string;
    value: number;
    color: string;
}

interface ComparisonData {
    parameter: string;
    current: number;
    optimal_min: number;
    optimal_max: number;
}

interface SoilHealthData {
    metric: string;
    value: number;
    optimal: number;
}

// NPK Bar Chart Component
export const NPKBarChart: React.FC<{ data: NPKData[] }> = ({ data }) => {
    const maxValue = 100;

    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-6">NPK Nutrient Levels</h3>
            <div className="space-y-6">
                {data.map((item, index) => (
                    <div key={index} className="space-y-2">
                        <div className="flex justify-between items-center">
                            <span className="text-sm font-semibold text-gray-700">{item.nutrient}</span>
                            <span className="text-sm font-bold" style={{ color: item.color }}>
                                {item.value.toFixed(1)}%
                            </span>
                        </div>
                        <div className="relative h-8 bg-gray-100 rounded-full overflow-hidden">
                            <div
                                className="absolute top-0 left-0 h-full rounded-full transition-all duration-1000 ease-out"
                                style={{
                                    width: `${(item.value / maxValue) * 100}%`,
                                    backgroundColor: item.color
                                }}
                            >
                                <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/20"></div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// Comparison Chart (Current vs Optimal)
export const ComparisonChart: React.FC<{ data: ComparisonData[] }> = ({ data }) => {
    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Current vs Optimal Range</h3>
            <div className="space-y-5">
                {data.map((item, index) => {
                    const isInRange = item.current >= item.optimal_min && item.current <= item.optimal_max;
                    const rangeWidth = item.optimal_max - item.optimal_min;
                    const rangeStart = (item.optimal_min / 100) * 100;
                    const rangeLength = (rangeWidth / 100) * 100;
                    const currentPosition = item.parameter === 'pH'
                        ? ((item.current / 14) * 100)
                        : item.current;

                    return (
                        <div key={index} className="space-y-2">
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-semibold text-gray-700">{item.parameter}</span>
                                <span className={`text-xs font-bold px-2 py-1 rounded-full ${isInRange ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`}>
                                    {item.current.toFixed(1)} {isInRange ? '✓' : '!'}
                                </span>
                            </div>
                            <div className="relative h-6 bg-gray-100 rounded-full overflow-hidden">
                                {/* Optimal range background */}
                                <div
                                    className="absolute top-0 h-full bg-green-100"
                                    style={{
                                        left: `${item.parameter === 'pH' ? (item.optimal_min / 14) * 100 : item.optimal_min}%`,
                                        width: `${item.parameter === 'pH' ? (rangeWidth / 14) * 100 : rangeWidth}%`
                                    }}
                                ></div>
                                {/* Current value marker */}
                                <div
                                    className="absolute top-0 h-full w-1 bg-blue-600 shadow-lg transition-all duration-1000"
                                    style={{ left: `${currentPosition}%` }}
                                >
                                    <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-3 h-3 bg-blue-600 rounded-full border-2 border-white"></div>
                                </div>
                            </div>
                            <div className="flex justify-between text-xs text-gray-400">
                                <span>{item.optimal_min}</span>
                                <span className="text-green-600 font-medium">Optimal</span>
                                <span>{item.optimal_max}</span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

// Radar/Spider Chart for Soil Health
export const SoilHealthRadar: React.FC<{ data: SoilHealthData[] }> = ({ data }) => {
    const size = 300;
    const center = size / 2;
    const maxRadius = size / 2 - 40;
    const numPoints = data.length;

    // Calculate polygon points
    const getPoint = (index: number, value: number) => {
        const angle = (Math.PI * 2 * index) / numPoints - Math.PI / 2;
        const radius = (value / 100) * maxRadius;
        return {
            x: center + radius * Math.cos(angle),
            y: center + radius * Math.sin(angle)
        };
    };

    const optimalPoints = data.map((item, i) => getPoint(i, item.optimal)).map(p => `${p.x},${p.y}`).join(' ');
    const currentPoints = data.map((item, i) => getPoint(i, item.value)).map(p => `${p.x},${p.y}`).join(' ');

    // Grid circles
    const gridLevels = [20, 40, 60, 80, 100];

    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Soil Health Overview</h3>
            <div className="flex items-center justify-center">
                <svg width={size} height={size} className="overflow-visible">
                    {/* Grid circles */}
                    {gridLevels.map((level, i) => (
                        <circle
                            key={i}
                            cx={center}
                            cy={center}
                            r={(level / 100) * maxRadius}
                            fill="none"
                            stroke="#e5e7eb"
                            strokeWidth="1"
                        />
                    ))}

                    {/* Grid lines */}
                    {data.map((_, index) => {
                        const point = getPoint(index, 100);
                        return (
                            <line
                                key={index}
                                x1={center}
                                y1={center}
                                x2={point.x}
                                y2={point.y}
                                stroke="#e5e7eb"
                                strokeWidth="1"
                            />
                        );
                    })}

                    {/* Optimal range polygon */}
                    <polygon
                        points={optimalPoints}
                        fill="#22c55e"
                        fillOpacity="0.1"
                        stroke="#22c55e"
                        strokeWidth="2"
                        strokeDasharray="5,5"
                    />

                    {/* Current values polygon */}
                    <polygon
                        points={currentPoints}
                        fill="#3b82f6"
                        fillOpacity="0.3"
                        stroke="#3b82f6"
                        strokeWidth="2"
                    />

                    {/* Data points */}
                    {data.map((item, index) => {
                        const point = getPoint(index, item.value);
                        return (
                            <circle
                                key={index}
                                cx={point.x}
                                cy={point.y}
                                r="4"
                                fill="#3b82f6"
                                stroke="white"
                                strokeWidth="2"
                            />
                        );
                    })}

                    {/* Labels */}
                    {data.map((item, index) => {
                        const labelPoint = getPoint(index, 110);
                        return (
                            <text
                                key={index}
                                x={labelPoint.x}
                                y={labelPoint.y}
                                textAnchor="middle"
                                fontSize="12"
                                fill="#374151"
                                fontWeight="600"
                            >
                                {item.metric}
                            </text>
                        );
                    })}
                </svg>
            </div>
            <div className="flex justify-center gap-6 mt-4">
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full bg-blue-500"></div>
                    <span className="text-xs text-gray-600">Current</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full border-2 border-green-500 border-dashed"></div>
                    <span className="text-xs text-gray-600">Optimal</span>
                </div>
            </div>
        </div>
    );
};

// Horizontal Bar Chart for Crop Recommendations
interface CropData {
    crop_name: string;
    suitability_score: number;
    is_optimal: boolean;
    crop_type: string;
}

export const CropSuitabilityChart: React.FC<{ crops: CropData[] }> = ({ crops }) => {
    const maxScore = 100;

    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Crop Suitability Scores</h3>
            <div className="space-y-4">
                {crops.map((crop, index) => (
                    <div key={index} className="space-y-2">
                        <div className="flex justify-between items-center">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-semibold text-gray-700">{crop.crop_name}</span>
                                {crop.is_optimal && (
                                    <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-bold">
                                        ★ OPTIMAL
                                    </span>
                                )}
                            </div>
                            <span className="text-sm font-bold text-green-600">{crop.suitability_score.toFixed(0)}%</span>
                        </div>
                        <div className="relative h-10 bg-gray-100 rounded-full overflow-hidden">
                            <div
                                className={`absolute top-0 left-0 h-full rounded-full transition-all duration-1000 ease-out ${crop.is_optimal ? 'bg-gradient-to-r from-green-500 to-green-600' : 'bg-gradient-to-r from-blue-400 to-blue-500'
                                    }`}
                                style={{ width: `${(crop.suitability_score / maxScore) * 100}%` }}
                            >
                                <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/20"></div>
                            </div>
                            <div className="absolute inset-0 flex items-center px-3">
                                <span className="text-xs font-medium text-gray-500">{crop.crop_type}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// Mini Donut Chart for Single Metric
interface DonutChartProps {
    value: number;
    maxValue: number;
    label: string;
    color: string;
}

export const DonutChart: React.FC<DonutChartProps> = ({ value, maxValue, label, color }) => {
    const percentage = (value / maxValue) * 100;
    const circumference = 2 * Math.PI * 45;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;

    return (
        <div className="flex flex-col items-center">
            <svg width="120" height="120" className="transform -rotate-90">
                <circle
                    cx="60"
                    cy="60"
                    r="45"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="10"
                />
                <circle
                    cx="60"
                    cy="60"
                    r="45"
                    fill="none"
                    stroke={color}
                    strokeWidth="10"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    className="transition-all duration-1000"
                />
            </svg>
            <div className="text-center -mt-20">
                <div className="text-2xl font-bold text-gray-900">{value.toFixed(1)}</div>
                <div className="text-xs text-gray-500">{label}</div>
            </div>
        </div>
    );
};

// Sensor Availability Chart
interface SensorTypeData {
    sensor_type: string;
    count: number;
    percentage: number;
}

interface SensorAvailabilityData {
    total_sensors: number;
    sensors_by_type: SensorTypeData[];
}

export const SensorAvailabilityChart: React.FC<{ data: SensorAvailabilityData }> = ({ data }) => {
    const colors = ['#3b82f6', '#22c55e', '#f59e0b', '#ec4899', '#8b5cf6', '#06b6d4'];

    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Sensor Availability</h3>
            <div className="space-y-4">
                <div className="flex items-center justify-center mb-6">
                    <div className="text-center">
                        <div className="text-4xl font-bold text-blue-600">{data.total_sensors}</div>
                        <div className="text-sm text-gray-500">Total Sensors</div>
                    </div>
                </div>
                <div className="space-y-3">
                    {data.sensors_by_type.map((sensor, index) => (
                        <div key={index} className="space-y-2">
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-semibold text-gray-700">{sensor.sensor_type}</span>
                                <span className="text-xs font-bold text-gray-500">{sensor.count} ({sensor.percentage}%)</span>
                            </div>
                            <div className="relative h-6 bg-gray-100 rounded-full overflow-hidden">
                                <div
                                    className="absolute top-0 left-0 h-full rounded-full transition-all duration-1000"
                                    style={{
                                        width: `${sensor.percentage}%`,
                                        backgroundColor: colors[index % colors.length]
                                    }}
                                >
                                    <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/20"></div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Water Levels Chart
interface WaterLevelData {
    sensor_id: number;
    sensor_type: string;
    water_level: number;
}

interface WaterLevelsData {
    water_levels: WaterLevelData[];
    average_water_level: number;
}

export const WaterLevelsChart: React.FC<{ data: WaterLevelsData }> = ({ data }) => {
    const getStatusColor = (level: number) => {
        if (level < 30) return '#ef4444'; // Red - Low
        if (level > 80) return '#f59e0b'; // Orange - High
        return '#22c55e'; // Green - Normal
    };

    const getStatusText = (level: number) => {
        if (level < 30) return 'Low';
        if (level > 80) return 'High';
        return 'Normal';
    };

    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Water Levels</h3>
            <div className="space-y-4">
                <div className="flex items-center justify-center mb-6 bg-blue-50 rounded-2xl p-4">
                    <div className="text-center">
                        <div className="text-3xl font-bold text-blue-600">{data.average_water_level.toFixed(1)}%</div>
                        <div className="text-sm text-gray-500">Average Level</div>
                    </div>
                </div>
                <div className="space-y-3">
                    {data.water_levels.map((sensor, index) => (
                        <div key={index} className="space-y-2">
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-semibold text-gray-700">{sensor.sensor_type} #{sensor.sensor_id}</span>
                                <span
                                    className="text-xs font-bold px-2 py-1 rounded-full"
                                    style={{
                                        backgroundColor: `${getStatusColor(sensor.water_level)}20`,
                                        color: getStatusColor(sensor.water_level)
                                    }}
                                >
                                    {sensor.water_level.toFixed(1)}% • {getStatusText(sensor.water_level)}
                                </span>
                            </div>
                            <div className="relative h-6 bg-gray-100 rounded-full overflow-hidden">
                                <div
                                    className="absolute top-0 left-0 h-full rounded-full transition-all duration-1000"
                                    style={{
                                        width: `${sensor.water_level}%`,
                                        backgroundColor: getStatusColor(sensor.water_level)
                                    }}
                                >
                                    <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/30"></div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Sensor Readings Trend Chart (Line Chart)
interface ReadingData {
    timestamp: string;
    value: number;
    sensor_id: number;
}

interface SensorReadingsData {
    moisture_trend: ReadingData[];
    temperature_trend: ReadingData[];
    statistics: {
        moisture: { average: number; min: number; max: number };
        temperature: { average: number; min: number; max: number };
    };
}

export const SensorReadingsTrendChart: React.FC<{ data: SensorReadingsData }> = ({ data }) => {
    const width = 600;
    const height = 200;
    const padding = 40;

    // Helper to create line path
    const createLinePath = (readings: ReadingData[], maxValue: number) => {
        if (readings.length === 0) return '';

        const xStep = (width - 2 * padding) / (readings.length - 1 || 1);
        const yScale = (height - 2 * padding) / maxValue;

        return readings.map((reading, i) => {
            const x = padding + i * xStep;
            const y = height - padding - (reading.value * yScale);
            return i === 0 ? `M ${x} ${y}` : `L ${x} ${y}`;
        }).join(' ');
    };

    const moistureMax = Math.max(...data.moisture_trend.map(r => r.value), 100);
    const temperatureMax = Math.max(...data.temperature_trend.map(r => r.value), 50);

    return (
        <div className="bg-white p-6 rounded-3xl shadow-sm">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Sensor Readings Trend</h3>

            {/* Statistics Cards */}
            <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-blue-50 rounded-2xl p-4">
                    <div className="text-xs text-gray-500 mb-1">Moisture</div>
                    <div className="text-2xl font-bold text-blue-600">{data.statistics.moisture.average.toFixed(1)}%</div>
                    <div className="text-xs text-gray-500 mt-1">
                        Range: {data.statistics.moisture.min.toFixed(0)} - {data.statistics.moisture.max.toFixed(0)}%
                    </div>
                </div>
                <div className="bg-orange-50 rounded-2xl p-4">
                    <div className="text-xs text-gray-500 mb-1">Temperature</div>
                    <div className="text-2xl font-bold text-orange-600">{data.statistics.temperature.average.toFixed(1)}°C</div>
                    <div className="text-xs text-gray-500 mt-1">
                        Range: {data.statistics.temperature.min.toFixed(0)} - {data.statistics.temperature.max.toFixed(0)}°C
                    </div>
                </div>
            </div>

            {/* Moisture Trend */}
            <div className="mb-6">
                <div className="text-sm font-semibold text-gray-700 mb-2">Moisture Trend</div>
                <svg width="100%" height="200" viewBox={`0 0 ${width} ${height}`} className="border border-gray-100 rounded-lg">
                    {/* Grid */}
                    {[0, 25, 50, 75, 100].map(val => {
                        const y = height - padding - (val / moistureMax) * (height - 2 * padding);
                        return (
                            <g key={val}>
                                <line x1={padding} y1={y} x2={width - padding} y2={y} stroke="#e5e7eb" strokeWidth="1" />
                                <text x={padding - 10} y={y + 4} fontSize="10" fill="#9ca3af" textAnchor="end">{val}%</text>
                            </g>
                        );
                    })}
                    {/* Line */}
                    <path
                        d={createLinePath(data.moisture_trend, moistureMax)}
                        fill="none"
                        stroke="#3b82f6"
                        strokeWidth="2"
                    />
                    {/* Points */}
                    {data.moisture_trend.map((reading, i) => {
                        const xStep = (width - 2 * padding) / (data.moisture_trend.length - 1 || 1);
                        const yScale = (height - 2 * padding) / moistureMax;
                        const x = padding + i * xStep;
                        const y = height - padding - (reading.value * yScale);
                        return <circle key={i} cx={x} cy={y} r="3" fill="#3b82f6" />;
                    })}
                </svg>
            </div>

            {/* Temperature Trend */}
            <div>
                <div className="text-sm font-semibold text-gray-700 mb-2">Temperature Trend</div>
                <svg width="100%" height="200" viewBox={`0 0 ${width} ${height}`} className="border border-gray-100 rounded-lg">
                    {/* Grid */}
                    {[0, 10, 20, 30, 40].map(val => {
                        const y = height - padding - (val / temperatureMax) * (height - 2 * padding);
                        return (
                            <g key={val}>
                                <line x1={padding} y1={y} x2={width - padding} y2={y} stroke="#e5e7eb" strokeWidth="1" />
                                <text x={padding - 10} y={y + 4} fontSize="10" fill="#9ca3af" textAnchor="end">{val}°C</text>
                            </g>
                        );
                    })}
                    {/* Line */}
                    <path
                        d={createLinePath(data.temperature_trend, temperatureMax)}
                        fill="none"
                        stroke="#f59e0b"
                        strokeWidth="2"
                    />
                    {/* Points */}
                    {data.temperature_trend.map((reading, i) => {
                        const xStep = (width - 2 * padding) / (data.temperature_trend.length - 1 || 1);
                        const yScale = (height - 2 * padding) / temperatureMax;
                        const x = padding + i * xStep;
                        const y = height - padding - (reading.value * yScale);
                        return <circle key={i} cx={x} cy={y} r="3" fill="#f59e0b" />;
                    })}
                </svg>
            </div>
        </div>
    );
};

