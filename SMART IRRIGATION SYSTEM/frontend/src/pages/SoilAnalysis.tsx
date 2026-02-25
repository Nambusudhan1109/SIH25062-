import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Mic, HelpCircle, User, BarChart3, TrendingUp } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useUser } from '../context/UserContext';
import { soilAnalysisService, cropRecommendationService, landService } from '../services/supabaseService';
import type { SoilAnalysis as SoilAnalysisType, CropRecommendation } from '../services/supabaseService';
import {
    NPKBarChart,
    ComparisonChart,
    SoilHealthRadar,
    CropSuitabilityChart,
    DonutChart,
    SensorAvailabilityChart,
    WaterLevelsChart,
    SensorReadingsTrendChart
} from '../components/SoilCharts';

const SoilAnalysis: React.FC = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { t } = useLanguage();
    const { currentUser } = useUser();
    const [refreshing, setRefreshing] = React.useState(false);
    const [listening, setListening] = React.useState(false);
    const [loading, setLoading] = React.useState(true);
    const [soilData, setSoilData] = React.useState<SoilAnalysisType | null>(null);
    const [recommendations, setRecommendations] = React.useState<CropRecommendation[]>([]);
    const [landInfo, setLandInfo] = React.useState<any>(null);
    const [error, setError] = React.useState<string | null>(null);
    const [chartData, setChartData] = React.useState<any>(null);
    const [cropChartData, setCropChartData] = React.useState<any>(null);
    const [sensorData, setSensorData] = React.useState<any>(null);
    const [waterData, setWaterData] = React.useState<any>(null);
    const [readingsData, setReadingsData] = React.useState<any>(null);
    const [showCharts, setShowCharts] = React.useState(true);

    // Extract land_id from the URL parameter (e.g., "L-8" -> 8)
    const getLandId = () => {
        if (!id) return null;
        const match = id.match(/\d+/);
        return match ? parseInt(match[0]) : null;
    };

    const fetchChartData = async (landId: number) => {
        try {
            // Fetch chart data from Python backend
            const response = await fetch(`http://localhost:8000/api/soil-analysis/${landId}/chart-data`);
            if (response.ok) {
                const data = await response.json();
                setChartData(data);
            }

            // Fetch crop recommendation chart data
            const cropResponse = await fetch(`http://localhost:8000/api/crop-recommendations/${landId}/chart-data`);
            if (cropResponse.ok) {
                const cropData = await cropResponse.json();
                setCropChartData(cropData);
            }

            // Fetch sensor availability data
            const sensorResponse = await fetch(`http://localhost:8000/api/sensors/availability/${landId}`);
            if (sensorResponse.ok) {
                const sensorChartData = await sensorResponse.json();
                setSensorData(sensorChartData);
            }

            // Fetch water levels data
            const waterResponse = await fetch(`http://localhost:8000/api/water-levels/${landId}`);
            if (waterResponse.ok) {
                const waterChartData = await waterResponse.json();
                setWaterData(waterChartData);
            }

            // Fetch sensor readings trend data
            const readingsResponse = await fetch(`http://localhost:8000/api/sensor-readings/analysis/${landId}`);
            if (readingsResponse.ok) {
                const readingsChartData = await readingsResponse.json();
                setReadingsData(readingsChartData);
            }
        } catch (err) {
            console.error('Error fetching chart data:', err);
            // Chart data is optional, so don't throw error
        }
    };

    const fetchSoilData = async () => {
        const landId = getLandId();
        if (!landId) {
            setError('Invalid land ID');
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            setError(null);

            // Fetch land information
            const landData = await landService.getById(landId);
            setLandInfo(landData);

            // Fetch soil analysis data
            const soilAnalysis = await soilAnalysisService.getByLand(landId);
            setSoilData(soilAnalysis);

            // Fetch crop recommendations
            const cropRecs = await cropRecommendationService.getByLand(landId);
            setRecommendations(cropRecs || []);

            // Fetch chart data from backend
            await fetchChartData(landId);
        } catch (err: any) {
            console.error('Error fetching soil data:', err);
            setError(err.message || 'Failed to fetch soil data');
            // Set default values if no data found
            setSoilData(null);
            setRecommendations([]);
        } finally {
            setLoading(false);
        }
    };

    React.useEffect(() => {
        if (!currentUser) {
            navigate('/');
            return;
        }
        fetchSoilData();
    }, [currentUser, navigate, id]);

    if (!currentUser) return null;

    const handleRefresh = async () => {
        setRefreshing(true);
        await fetchSoilData();
        setRefreshing(false);
    };

    const handleListen = () => {
        setListening(true);
        setTimeout(() => setListening(false), 3000);
    };

    // Calculate percentage for progress bars
    const getPercentage = (value: number, max: number) => Math.min((value / max) * 100, 100);

    // Get current time formatted
    const getCurrentTime = () => {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 border-4 border-green-900 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading soil analysis...</p>
                </div>
            </div>
        );
    }

    if (!soilData && !loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
                <div className="bg-white rounded-3xl shadow-lg p-8 max-w-md text-center">
                    <div className="text-6xl mb-4">🌾</div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">No Soil Data Available</h2>
                    <p className="text-gray-600 mb-4">
                        {landInfo?.land_name || `Land ${id}`} doesn't have soil analysis data yet.
                    </p>
                    <p className="text-sm text-gray-500 mb-6">
                        Run the SQL script to add sample data for this land, or add soil analysis data through the admin panel.
                    </p>
                    <div className="flex gap-3 justify-center">
                        <button
                            onClick={() => navigate(-1)}
                            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-full font-bold hover:bg-gray-300 transition"
                        >
                            Go Back
                        </button>
                        <button
                            onClick={handleRefresh}
                            className="px-6 py-3 bg-green-900 text-white rounded-full font-bold hover:bg-green-800 transition"
                        >
                            Retry
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col p-6 font-sans">
            {/* Header */}
            <header className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <button onClick={() => navigate(-1)} className="flex items-center text-gray-600 hover:text-green-800 transition">
                        <ArrowLeft size={20} className="mr-2" /> {t('backToFields')}
                    </button>
                    <div className="text-2xl font-bold text-green-900 flex items-center gap-2">
                        <span className="w-8 h-8 bg-green-800 rounded-lg flex items-center justify-center text-white text-sm">🌾</span>
                        AgriCrop <span className="text-green-600">Pro</span>
                    </div>
                </div>
                <div className="flex items-center gap-6 text-gray-500">
                    <button onClick={() => alert(t('help'))} className="flex items-center gap-2 cursor-pointer hover:text-green-800 transition">
                        <HelpCircle size={20} /> <span className="font-semibold">{t('help')}</span>
                    </button>
                    <div className="flex items-center gap-2">
                        <div className="text-right">
                            <p className="font-bold text-gray-900 text-sm">{currentUser.name}</p>
                            <p className="text-xs text-capitalize text-gray-400">{currentUser.role}</p>
                        </div>
                        <div className="w-10 h-10 rounded-full overflow-hidden border border-orange-200">
                            <img src={currentUser.image} alt={currentUser.name} className="w-full h-full object-cover" />
                        </div>
                    </div>
                </div>
            </header>

            <div className="flex flex-col lg:flex-row gap-8">
                {/* Left Panel: Soil Stats */}
                <aside className="w-full lg:w-1/4 space-y-6">
                    <div className="bg-white p-6 rounded-3xl shadow-sm">
                        <h2 className="text-xl font-bold text-gray-900 mb-2">{t('soilAnalysis')}</h2>
                        <p className="text-xs text-gray-400 uppercase tracking-wide mb-6">
                            {landInfo?.land_name || `SECTOR ${id}`} • {t('today')} {getCurrentTime()}
                        </p>

                        {/* PH Levels */}
                        <div className="mb-6">
                            <div className="flex justify-between mb-2">
                                <span className="font-bold text-gray-700 flex items-center gap-2">🧪 {t('phLevels')}</span>
                                <span className="font-bold text-green-600">
                                    {soilData?.ph_level?.toFixed(1) || 'N/A'}
                                </span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2 mb-2">
                                <div
                                    className="bg-green-600 h-2 rounded-full"
                                    style={{ width: `${getPercentage(soilData?.ph_level || 0, 14)}%` }}
                                ></div>
                            </div>
                            <p className="text-xs text-gray-400">{t('optimalRange')}: 6.0 - 7.5</p>
                        </div>

                        {/* Moisture */}
                        <div className="mb-6">
                            <div className="flex justify-between mb-2">
                                <span className="font-bold text-gray-700 flex items-center gap-2">💧 {t('moisture')}</span>
                                <span className="font-bold text-blue-600">
                                    {soilData?.moisture_level ? `${soilData.moisture_level}%` : 'N/A'}
                                </span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2 mb-2">
                                <div
                                    className="bg-blue-600 h-2 rounded-full"
                                    style={{ width: `${soilData?.moisture_level || 0}%` }}
                                ></div>
                            </div>
                            <p className="text-xs text-gray-400">{t('status')}: {t('stable')}</p>
                        </div>

                        {/* NPK Levels */}
                        <div className="mb-6">
                            <div className="flex justify-between mb-4">
                                <span className="font-bold text-gray-700 flex items-center gap-2">🌱 {t('npkLevels')}</span>
                            </div>
                            <div className="space-y-3">
                                <div className="flex items-center gap-2">
                                    <span className="w-4 font-bold text-xs text-gray-500">N</span>
                                    <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                                        <div
                                            className="bg-green-700 h-1.5 rounded-full"
                                            style={{ width: `${soilData?.nitrogen || 0}%` }}
                                        ></div>
                                    </div>
                                    <span className="text-xs text-gray-500">{soilData?.nitrogen || 0}%</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="w-4 font-bold text-xs text-gray-500">P</span>
                                    <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                                        <div
                                            className="bg-green-600 h-1.5 rounded-full"
                                            style={{ width: `${soilData?.phosphorus || 0}%` }}
                                        ></div>
                                    </div>
                                    <span className="text-xs text-gray-500">{soilData?.phosphorus || 0}%</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <span className="w-4 font-bold text-xs text-gray-500">K</span>
                                    <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                                        <div
                                            className="bg-green-500 h-1.5 rounded-full"
                                            style={{ width: `${soilData?.potassium || 0}%` }}
                                        ></div>
                                    </div>
                                    <span className="text-xs text-gray-500">{soilData?.potassium || 0}%</span>
                                </div>
                            </div>
                        </div>

                        {/* Insight Box */}
                        <div className="bg-green-50 p-4 rounded-xl border border-green-100">
                            <h4 className="flex items-center gap-2 font-bold text-green-900 text-sm mb-2">ℹ️ {t('soilInsight')}</h4>
                            <p className="text-xs text-green-800 leading-relaxed">
                                {landInfo?.soil_type ? `Soil Type: ${landInfo.soil_type}. ` : ''}
                                {soilData?.organic_matter ? `Organic Matter: ${soilData.organic_matter}%. ` : ''}
                                {t('soilInsightText')}
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={handleRefresh}
                        className={`w-full py-4 bg-white border border-gray-200 rounded-full font-bold text-green-900 hover:bg-gray-50 shadow-sm transition flex justify-center items-center gap-2 ${refreshing ? 'opacity-75 cursor-wait' : ''}`}
                        disabled={refreshing}
                    >
                        {refreshing ? <div className="w-4 h-4 border-2 border-green-900 border-t-transparent rounded-full animate-spin"></div> : null}
                        {t('refreshSensors')}
                    </button>
                </aside>

                {/* Center Panel: Charts and Analysis */}
                <main className="flex-1 space-y-6">
                    {/* Chart Toggle Button */}
                    <div className="flex justify-between items-center">
                        <div>
                            <h2 className="text-3xl font-bold text-gray-900">{t('soilAnalysis')}</h2>
                            <p className="text-gray-500">Visual Data Analysis & Insights</p>
                        </div>
                        <button
                            onClick={() => setShowCharts(!showCharts)}
                            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-full font-semibold text-gray-700 hover:bg-gray-50 transition"
                        >
                            {showCharts ? <TrendingUp size={18} /> : <BarChart3 size={18} />}
                            {showCharts ? 'Hide Charts' : 'Show Charts'}
                        </button>
                    </div>

                    {/* Charts Section */}
                    {showCharts && chartData && (
                        <div className="space-y-6">
                            {/* Row 1: NPK | Comparison | Water Levels (3 columns) */}
                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                                <NPKBarChart data={chartData.npk_bar_chart} />
                                <ComparisonChart data={chartData.comparison_chart} />
                                {waterData && <WaterLevelsChart data={waterData} />}
                            </div>

                            {/* Row 2: Crop Suitability Chart (Full Width) */}
                            {cropChartData && cropChartData.crops && (
                                <CropSuitabilityChart crops={cropChartData.crops} />
                            )}

                            {/* Row 3: Sensor Availability */}
                            {sensorData && (
                                <SensorAvailabilityChart data={sensorData} />
                            )}
                        </div>
                    )}

                    {/* Separator */}
                    {showCharts && chartData && (
                        <div className="border-t border-gray-200 my-8"></div>
                    )}

                    {/* Crop Recommendations Section */}
                    <div>
                        <h2 className="text-3xl font-bold text-gray-900 mb-2">{t('topRecommendations')}</h2>
                        <p className="text-gray-500 mb-8">{t('recommendationsSubtitle')}</p>
                    </div>

                    {recommendations.length === 0 ? (
                        <div className="bg-white p-12 rounded-3xl shadow-sm text-center">
                            <div className="text-6xl mb-4">🌾</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">No Recommendations Available</h3>
                            <p className="text-gray-500">Soil analysis data is needed to generate crop recommendations.</p>
                        </div>
                    ) : (
                        <>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
                                {/* Display top 2 recommendations as cards */}
                                {recommendations.slice(0, 2).map((rec, index) => (
                                    <div key={rec.recommendation_id} className="bg-white p-4 rounded-3xl shadow-sm hover:shadow-md transition">
                                        <div className="h-40 rounded-2xl overflow-hidden mb-4 relative">
                                            <img
                                                src={rec.image_url || 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&q=80&w=1000'}
                                                alt={rec.crop_name || 'Crop'}
                                                className="w-full h-full object-cover"
                                            />
                                            {rec.is_optimal && (
                                                <span className="absolute top-3 left-3 bg-green-900 text-white text-[10px] font-bold px-2 py-1 rounded-full">
                                                    {t('optimalChoice')}
                                                </span>
                                            )}
                                            {!rec.is_optimal && (
                                                <span className="absolute top-3 left-3 bg-white text-green-900 text-[10px] font-bold px-2 py-1 rounded-full border border-green-200">
                                                    {t('highlyCompatible')}
                                                </span>
                                            )}
                                            <div className="absolute bottom-3 right-3 bg-white/90 backdrop-blur px-2 py-1 rounded-full text-xs font-bold text-green-900">
                                                Score: {rec.suitability_score || 0}%
                                            </div>
                                        </div>
                                        <div className="flex justify-between items-start mb-2">
                                            <h3 className="text-xl font-bold text-gray-900">{rec.crop_name || 'Unknown Crop'}</h3>
                                            <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center text-green-700 text-xs">✔</div>
                                        </div>
                                        <div className="flex gap-4 text-xs text-gray-500 font-medium mb-4">
                                            {rec.growth_duration_days && (
                                                <span className="flex items-center gap-1">📅 {rec.growth_duration_days} days</span>
                                            )}
                                            {rec.estimated_yield && (
                                                <span className="flex items-center gap-1">📈 {rec.estimated_yield}</span>
                                            )}
                                            {rec.crop_type && (
                                                <span className="flex items-center gap-1">🌾 {rec.crop_type}</span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Full Width Card for 3rd recommendation */}
                            {recommendations.length > 2 && (
                                <div className="bg-white p-4 rounded-3xl shadow-sm hover:shadow-md transition mt-6 flex flex-col md:flex-row gap-6">
                                    <div className="w-full md:w-1/3 h-40 md:h-auto rounded-2xl overflow-hidden relative">
                                        <img
                                            src={recommendations[2].image_url || 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&q=80&w=1000'}
                                            alt={recommendations[2].crop_name || 'Crop'}
                                            className="w-full h-full object-cover"
                                        />
                                    </div>
                                    <div className="flex-1 py-2">
                                        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 block">
                                            {t('alternative')}
                                        </span>
                                        <div className="flex justify-between items-start mb-2">
                                            <h3 className="text-2xl font-bold text-gray-900">{recommendations[2].crop_name || 'Unknown Crop'}</h3>
                                            <div className="w-6 h-6 bg-gray-100 rounded-full flex items-center justify-center text-gray-400 text-xs">✔</div>
                                        </div>
                                        <p className="text-sm text-gray-500 mb-6 leading-relaxed">
                                            {recommendations[2].description || t('cornDescription')}
                                        </p>
                                        <div className="flex gap-6">
                                            {recommendations[2].crop_type && (
                                                <div className="flex items-center gap-2">
                                                    <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-800">🍃</div>
                                                    <div>
                                                        <p className="text-xs font-bold text-gray-900">{recommendations[2].crop_type}</p>
                                                        <p className="text-[10px] text-gray-400">{t('compatible')}</p>
                                                    </div>
                                                </div>
                                            )}
                                            {recommendations[2].market_price && (
                                                <div className="flex items-center gap-2">
                                                    <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-800">💵</div>
                                                    <div>
                                                        <p className="text-xs font-bold text-gray-900">{recommendations[2].market_price}</p>
                                                        <p className="text-[10px] text-gray-400">{t('marketPrice')}</p>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </main>

                {/* Right Panel: Assistant */}
                <aside className="w-full lg:w-1/4">
                    <div className="text-center">
                        <div className="inline-flex items-center gap-2 px-3 py-1 bg-green-100 rounded-full text-green-800 text-xs font-bold mb-4">
                            <div className={`w-2 h-2 ${listening ? 'bg-red-500 animate-ping' : 'bg-green-600 animate-pulse'} rounded-full`}></div>
                            {listening ? t('listening') : t('voiceActive')}
                        </div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-2">{t('agriAssistant')}</h2>
                        <p className="text-gray-400 text-sm mb-8">{t('voicePrompt')}</p>

                        {/* Audio Visualizer Placeholder */}
                        <div className="flex justify-center items-center gap-1 h-12 mb-8">
                            {listening ? (
                                // Active animation
                                [...Array(10)].map((_, i) => (
                                    <div key={i} className="w-1 bg-green-500 rounded-full animate-bounce" style={{ height: `${Math.random() * 40 + 10}px`, animationDelay: `${i * 0.1}s` }}></div>
                                ))
                            ) : (
                                // Static placeholder
                                [...Array(10)].map((_, i) => (
                                    <div key={i} className="w-1 bg-green-800 rounded-full h-1"></div>
                                ))
                            )}
                        </div>

                        {/* Listen Button */}
                        <button
                            onClick={handleListen}
                            className={`w-32 h-32 rounded-full border-4 flex flex-col items-center justify-center text-white shadow-2xl transition mx-auto mb-12 ${listening ? 'bg-red-600 border-red-500 animate-pulse' : 'bg-green-900 border-green-800/20 hover:scale-105'}`}
                        >
                            <Mic size={32} className="mb-2" />
                            <span className="font-bold tracking-widest text-xs uppercase">{listening ? t('listening') : t('listen')}</span>
                        </button>
                    </div>

                    {/* Recent Commands */}
                    <div className="space-y-4">
                        <p className="text-xs font-bold text-gray-400 uppercase tracking-widest text-center mb-4">{t('recentCommands')}</p>
                        <button onClick={() => alert(t('command1'))} className="w-full text-left p-4 bg-gray-100 rounded-2xl text-xs text-gray-600 font-medium hover:bg-gray-200 transition">
                            {t('command1')}
                        </button>
                        <button onClick={() => alert(t('command2'))} className="w-full text-left p-4 bg-gray-100 rounded-2xl text-xs text-gray-600 font-medium hover:bg-gray-200 transition">
                            {t('command2')}
                        </button>
                    </div>
                </aside>
            </div>
        </div>
    );
};


export default SoilAnalysis;
