import { createClient } from '@supabase/supabase-js';

// Use Vite environment variables. Set these in `.env` as VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://enjjjqprgihcsmubvxyh.supabase.co';
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_pfFLEoIWFQmHYhjrqIGfrg_LQ5TMG7F';

export const supabase = createClient(supabaseUrl, supabaseKey);
