import React, { useEffect } from 'react';
import { Mic, Leaf, LayoutGrid, Droplets } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useUser } from '../context/UserContext';
import type { Sector } from '../context/UserContext';
import { supabase } from '../lib/supabase';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { t, language, setLanguage } = useLanguage();
  const { currentUser } = useUser();
  const [filter, setFilter] = React.useState<'all' | 'critical'>('all');
  const [isListening, setIsListening] = React.useState(false);
  const [sectors, setSectors] = React.useState<Sector[]>([]);
  const [loading, setLoading] = React.useState(true);

  // Fetch live data from Supabase
  const loadSectors = async () => {
    if (!currentUser) return;

    setLoading(true);
    try {
      // Extract farmer_id from currentUser.id (format: "farmer-1" -> 1)
      const farmerId = currentUser.id.startsWith('farmer-')
        ? parseInt(currentUser.id.replace('farmer-', ''))
        : null;

      if (!farmerId) {
        console.error('Invalid farmer ID');
        setSectors([]);
        setLoading(false);
        return;
      }

      // Fetch ONLY the logged-in user's lands
      const { data: lands, error: landError } = await supabase
        .from('land')
        .select(`
                    land_id,
                    land_name,
                    area_acres,
                    soil_type,
                    village,
                    farmer_id,
                    farm:farmer_id (
                        name,
                        farm_image
                    )
                `)
        .eq('farmer_id', farmerId)
        .order('land_id', { ascending: true });

      if (landError) throw landError;

      if (lands && lands.length > 0) {
        // Process each land with its sensor readings and crops
        const sectorsData: Sector[] = await Promise.all(
          lands.map(async (land, index) => {
            // Get sensors for this land
            const { data: sensors } = await supabase
              .from('sensor')
              .select('sensor_id')
              .eq('land_id', land.land_id)
              .limit(1);

            let moisture = 50 + (index * 10) % 40; // Varied defaults for demo
            let status: 'critical' | 'optimal' = 'optimal';

            if (sensors && sensors.length > 0) {
              // Get latest reading
              const { data: readings } = await supabase
                .from('sensor_readings')
                .select('moisture, temperature')
                .eq('sensor_id', sensors[0].sensor_id)
                .order('recorded_at', { ascending: false })
                .limit(1);

              if (readings && readings.length > 0) {
                moisture = Math.round(readings[0].moisture || 50);
                // Critical if moisture below 30%
                status = moisture < 30 ? 'critical' : 'optimal';
              }
            } else {
              // No sensor, set status based on index for variety
              status = index % 3 === 0 ? 'critical' : 'optimal';
              moisture = status === 'critical' ? 15 + (index * 5) % 15 : 60 + (index * 8) % 35;
            }

            // Get crops for this land/farmer
            const { data: crops } = await supabase
              .from('crop')
              .select('growth_stage')
              .eq('farmer_id', land.farmer_id)
              .limit(1);

            const cropType = crops && crops.length > 0
              ? (crops[0].growth_stage || land.soil_type || 'Mixed Crop')
              : (land.soil_type || 'General Farming');

            // Get varied images based on status and index
            const imageOptions = status === 'critical'
              ? [
                'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=1000',
                'https://images.unsplash.com/photo-1595113316349-9fa4eb24f884?auto=format&fit=crop&q=80&w=1000',
                'https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=1000'
              ]
              : [
                'https://images.unsplash.com/photo-1625246333195-bf5f852be9b8?auto=format&fit=crop&q=80&w=1000',
                'https://images.unsplash.com/photo-1615811361524-6830df586c9a?auto=format&fit=crop&q=80&w=1000',
                'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?auto=format&fit=crop&q=80&w=1000',
                'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&q=80&w=1000'
              ];

            // Map to Sector format with full details
            return {
              id: `L-${land.land_id}`,
              nameKey: land.land_name || `${land.village || 'Field'} - Plot ${land.land_id}`,
              status,
              moisture,
              image: imageOptions[index % imageOptions.length],
              cropType: cropType
            };
          })
        );

        setSectors(sectorsData);
      } else {
        // No data yet - show empty
        setSectors([]);
      }
    } catch (error) {
      console.error('Error loading sectors:', error);
      setSectors([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSectors();
    // Auto-refresh every 30 minutes to match backend refresh cycle
    const interval = setInterval(loadSectors, 1800000); // 30 minutes
    return () => clearInterval(interval);
  }, [currentUser]);

  useEffect(() => {
    if (!currentUser) {
      navigate('/');
    }
  }, [currentUser, navigate]);

  if (!currentUser) return null;

  // Loop through languages for the switcher button
  const nextLang = () => {
    const langs: ('en' | 'hi' | 'ta' | 'ne')[] = ['en', 'hi', 'ta', 'ne'];
    const idx = langs.indexOf(language);
    setLanguage(langs[(idx + 1) % langs.length]);
  };

  const toggleListening = () => {
    setIsListening(!isListening);
    if (!isListening) {
      // Simulate listening duration
      setTimeout(() => setIsListening(false), 3000);
    }
  };

  const filteredSectors = filter === 'all'
    ? sectors
    : sectors.filter(s => s.status === 'critical');

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-sans">
      {/* Navbar */}
      <nav className="flex justify-between items-center mb-12">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-green-800 rounded-lg flex items-center justify-center text-white">
            <LayoutGrid size={24} />
          </div>
          <span className="text-xl font-bold text-green-900">AgriMonitor <span className="text-gray-400 font-light">Pro</span></span>
        </div>
        <div className="flex items-center gap-4">
          <div className="px-4 py-2 bg-gray-100 rounded-full flex items-center gap-2">
            <div className={`w-3 h-3 ${isListening ? 'bg-red-500 animate-ping' : 'bg-green-500 animate-pulse'} rounded-full`}></div>
            <span className="text-sm font-semibold text-gray-600">
              {isListening ? t('listening') : t('assistantStandby')}
            </span>
          </div>
          <button onClick={nextLang} className="w-10 h-10 bg-white rounded-full border border-gray-200 flex items-center justify-center text-xl hover:bg-gray-50 transition" title="Switch Language">
            {language === 'en' ? '🇺🇸' : language === 'hi' ? '🇮🇳' : language === 'ta' ? '🕉️' : '🇳🇵'}
          </button>
          <div className="flex items-center gap-3 ml-2 bg-white pl-2 pr-4 py-1 rounded-full border border-gray-200 shadow-sm">
            <div className="w-8 h-8 bg-orange-200 rounded-full overflow-hidden border border-orange-300">
              <img src={currentUser.image} className="w-full h-full object-cover" alt={currentUser.name} />
            </div>
            <div className="text-left hidden md:block">
              <p className="text-xs font-bold text-gray-800 leading-tight">{currentUser.name}</p>
              <p className="text-[10px] text-gray-500 leading-tight">{currentUser.role}</p>
            </div>
          </div>
        </div>
      </nav>

      <header className="mb-8 flex justify-between items-end flex-wrap gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-2">{t('dashboard')}</h1>
          <p className="text-gray-500">{t('realtime')}</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition ${filter === 'all' ? 'bg-green-800 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'}`}
          >
            {t('allSectors')}
          </button>
          <button
            onClick={() => setFilter('critical')}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition ${filter === 'critical' ? 'bg-red-600 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'}`}
          >
            {t('criticalOnly')}
          </button>
        </div>
      </header>

      {/* Grid */}
      {loading ? (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-800"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {filteredSectors.length === 0 ? (
            <div className="col-span-full text-center py-20 text-gray-400">
              <p>No sectors found for this user.</p>
            </div>
          ) : filteredSectors.map((sector) => (
            <div
              key={sector.id}
              className="group relative h-64 rounded-3xl overflow-hidden cursor-pointer shadow-lg hover:shadow-xl transition-all"
              onClick={() => navigate(`/analysis/${sector.id}`)}
            >
              {/* Background Image */}
              <div className="absolute inset-0 bg-gray-900">
                <img src={sector.image} alt={sector.nameKey} className="w-full h-full object-cover opacity-80 group-hover:opacity-60 transition-opacity" />
              </div>

              {/* Status Badge Top Left */}
              <div className={`absolute top-4 left-4 w-10 h-10 rounded-full flex items-center justify-center ${sector.status === 'critical' ? 'bg-red-500' : 'bg-green-500'} text-white shadow-md`}>
                <Droplets size={20} fill="white" />
              </div>

              {/* Status Attention Top Right */}
              {sector.status === 'critical' && (
                <div className="absolute top-4 right-4 bg-white px-3 py-1 rounded-full text-[10px] font-bold text-red-600 shadow-sm">{t('attention')}</div>
              )}

              {/* Content Bottom */}
              <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent">
                <div className="flex justify-between items-end mb-3">
                  <div>
                    <h3 className="text-2xl font-bold text-white">{sector.nameKey}</h3>
                    <p className="text-gray-300 text-sm">{sector.cropType}</p>
                  </div>
                  <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
                    <Leaf size={20} className="text-green-600" />
                  </div>
                </div>

                {/* Footer Bar */}
                <div className={`flex justify-between items-center px-4 py-2 rounded-xl backdrop-blur-md ${sector.status === 'critical' ? 'bg-red-500/90 text-white' : 'bg-green-500/90 text-white'}`}>
                  <span className="font-bold text-xs uppercase">{sector.status === 'critical' ? t('needsWater') : t('optimal')}</span>
                  <span className="font-bold">{sector.moisture}% Moisture</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Voice Command Button */}
      <div className="flex justify-center mb-12">
        <button
          onClick={toggleListening}
          className={`px-8 py-4 rounded-full shadow-2xl flex items-center gap-3 transition-transform hover:scale-105 ${isListening ? 'bg-red-600 animate-pulse' : 'bg-green-800 hover:bg-green-700'} text-white`}
        >
          <Mic size={24} />
          <span className="font-bold text-lg">{isListening ? t('listening') + '...' : t('voiceCommand')}</span>
        </button>
      </div>
    </div>
  );
};


export default Dashboard;
