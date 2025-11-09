import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

// Check if Supabase is properly configured
export const isSupabaseConfigured = !!(supabaseUrl && supabaseAnonKey && 
  !supabaseUrl.includes('placeholder') && 
  supabaseUrl.startsWith('http'));

// Create Supabase client only if credentials are provided
// Otherwise, create a mock client that will return empty results
export const supabase: SupabaseClient = isSupabaseConfigured
  ? createClient(supabaseUrl, supabaseAnonKey)
  : createClient('https://placeholder.supabase.co', 'placeholder-key');

export interface Dorm {
  id: string;
  name: string;
  image_url: string;
  quietness: number;
  social: number;
  distance_to_campus: number;
  room_type: string;
  cost_range: number;
  gender_type: string;
  has_ac: boolean;
  has_laundry: boolean;
  has_kitchen: boolean;
  has_elevator: boolean;
  is_accessible: boolean;
  community_type: string;
  year_mix: string;
  amenities: string[];
  description: string;
  tags: string[];
}

export interface QuizResponses {
  sessionId?: string;
  // Step 1: Basic Information
  yearStatus?: string; // 'first-year' or 'upperclassman'
  major?: string; // Student's major field of study
  roomType: string;
  genderType: string;
  accessible?: boolean | string; // Can be boolean or string ('yes', 'preferred', 'no')
  isHonors?: string; // 'yes' or 'no'
  breakHousing?: string; // 'yes', 'preferred', or 'no'
  // Step 2: Social & Lifestyle
  socialLevelType?: string;
  socialLevel?: number; // Keep for backward compatibility
  noiseLevelType?: string;
  noiseLevel?: number; // Keep for backward compatibility
  activitiesImportance?: string;
  eventsImportance?: number; // Keep for backward compatibility
  environmentPref?: string;
  partyOrQuiet?: number; // Keep for backward compatibility
  yearMix: string;
  sleepSchedule: string;
  tidinessLevel?: string;
  tidiness?: number; // Keep for backward compatibility
  lifestyleMatch?: string;
  roommateMatch?: boolean; // Keep for backward compatibility
  guestFrequencyType?: string;
  guestFrequency?: number; // Keep for backward compatibility
  // Step 3: Amenities & Facilities
  kitchenImportanceType?: string;
  kitchenImportance?: number; // Keep for backward compatibility
  campusProximity?: string;
  proximityImportance?: number; // Keep for backward compatibility
  activityProximity?: string;
  locationPreference?: string; // Keep for backward compatibility
  spaceType?: string;
  greenSpaces?: boolean; // Keep for backward compatibility
  commuteDistanceType?: string;
  commuteDistance?: number; // Keep for backward compatibility
  outdoorSpaceType?: string;
  outdoorSpace?: boolean; // Keep for backward compatibility
  // Step 4: Community & Interests
  communityType: string;
  sharedInterestsType?: string;
  sharedInterests?: number; // Keep for backward compatibility
  themeDorm?: boolean; // Keep for backward compatibility
  // Step 5: Special Needs
  sensitivitiesType?: string;
  sensitivities?: string[]; // Keep for backward compatibility
  // Step 6: Priority Rankings
  priorities: { [key: string]: number };
}
