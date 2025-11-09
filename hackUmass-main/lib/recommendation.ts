import { Dorm, QuizResponses } from './supabase';

// Helper function to convert social level string to numeric (1-10 scale)
function socialLevelToNumber(socialLevel?: string): number {
  if (!socialLevel) return 5;
  const levels: { [key: string]: number } = {
    'very-social': 9,
    'moderately-social': 7,
    'somewhat-social': 5,
    'minimal-social': 2,
  };
  return levels[socialLevel] || 5;
}

// Helper function to convert noise level string to numeric (1-10 scale, where 10 = very quiet)
function noiseLevelToNumber(noiseLevel?: string): number {
  if (!noiseLevel) return 5;
  const levels: { [key: string]: number } = {
    'very-quiet': 9,
    'quiet': 7,
    'moderate': 5,
    'somewhat-loud': 3,
    'loud': 1,
  };
  return levels[noiseLevel] || 5;
}

// Helper function to convert commute distance string to numeric (minutes)
function commuteDistanceToNumber(commuteDistance?: string): number {
  if (!commuteDistance) return 10;
  const distances: { [key: string]: number } = {
    'under-5min': 3,
    '5-10min': 7,
    '10-15min': 12,
    '15-20min': 17,
    'over-20min': 25,
  };
  return distances[commuteDistance] || 10;
}

// Helper function to convert importance string to numeric (1-10 scale)
function importanceToNumber(importance?: string): number {
  if (!importance) return 5;
  const levels: { [key: string]: number } = {
    'essential': 10,
    'very-important': 8,
    'important': 6,
    'nice-to-have': 4,
    'not-important': 2,
    'yes-required': 10,
    'preferred': 6,
    'no-preference': 5,
  };
  return levels[importance] || 5;
}

// Helper function to check if accessible is required
function isAccessibleRequired(accessible?: boolean | string): boolean {
  if (typeof accessible === 'boolean') return accessible;
  if (typeof accessible === 'string') return accessible === 'yes' || accessible === 'yes-required';
  return false;
}

// Helper function to normalize gender type
function normalizeGenderType(genderType?: string): string {
  if (!genderType) return 'co-ed';
  if (genderType === 'co-ed' || genderType === 'coed') return 'co-ed';
  if (genderType === 'Male' || genderType === 'male' || genderType === 'all-male') return 'all-male';
  if (genderType === 'Female' || genderType === 'female' || genderType === 'all-female') return 'all-female';
  return 'co-ed'; // Default for Non-binary, Prefer not to say
}

export function calculateCompatibility(dorm: Dorm, responses: QuizResponses): number {
  let score = 0;
  let maxScore = 0;

  const priorities = responses.priorities || {
    location: 5,
    privacy: 5,
    amenities: 5,
    social: 5,
  };

  // Room type matching
  const roomTypeWeight = priorities.privacy || 5;
  maxScore += roomTypeWeight * 10;
  if (dorm.room_type === responses.roomType) {
    score += 10 * roomTypeWeight;
  } else if (
    (responses.roomType === 'suite' && dorm.room_type === 'apartment') ||
    (responses.roomType === 'apartment' && dorm.room_type === 'suite')
  ) {
    score += 7 * roomTypeWeight;
  } else {
    score += 3 * roomTypeWeight;
  }

  // Gender type matching (strict requirement)
  const normalizedGenderType = normalizeGenderType(responses.genderType);
  if (normalizedGenderType !== 'co-ed' && dorm.gender_type !== 'co-ed') {
    if (dorm.gender_type !== normalizedGenderType) {
      return 0; // Hard requirement - no match if gender preference doesn't match
    }
  }

  // Accessibility requirement (strict)
  const accessibleRequired = isAccessibleRequired(responses.accessible);
  if (accessibleRequired && !dorm.is_accessible) {
    return 0; // Hard requirement - no match if accessibility is required but not available
  }

  // Social level matching
  const socialWeight = priorities.social || 5;
  maxScore += socialWeight * 10;
  const socialValue = responses.socialLevel || socialLevelToNumber(responses.socialLevelType);
  const socialDiff = Math.abs(dorm.social - socialValue);
  const socialScore = Math.max(0, 10 - socialDiff);
  score += socialScore * socialWeight;

  // Noise level matching (inverted - dorm.quietness is high for quiet, noiseLevel is high for loud)
  maxScore += socialWeight * 10;
  const noiseValue = responses.noiseLevel || noiseLevelToNumber(responses.noiseLevelType);
  // Convert noise preference to quietness preference (inverse relationship)
  const quietnessPreference = 11 - noiseValue; // If user wants loud (1), they want low quietness (10)
  const noiseDiff = Math.abs(dorm.quietness - quietnessPreference);
  const noiseScore = Math.max(0, 10 - noiseDiff);
  score += noiseScore * socialWeight;

  // Location/distance matching
  const locationWeight = priorities.location || 5;
  maxScore += locationWeight * 10;
  const distanceValue = responses.commuteDistance || commuteDistanceToNumber(responses.commuteDistanceType);
  const distanceDiff = Math.abs(dorm.distance_to_campus - distanceValue);
  const distanceScore = Math.max(0, 10 - (distanceDiff / 2));
  score += distanceScore * locationWeight;

  // Amenities matching
  const amenitiesWeight = priorities.amenities || 5;
  maxScore += amenitiesWeight * 10;
  let amenitiesScore = 0;

  const kitchenImportance = responses.kitchenImportance || importanceToNumber(responses.kitchenImportanceType);
  if (kitchenImportance >= 7 && dorm.has_kitchen) amenitiesScore += 3;

  if (accessibleRequired && dorm.is_accessible) amenitiesScore += 2;

  score += amenitiesScore * amenitiesWeight;

  // Community type matching
  if (responses.communityType && responses.communityType !== 'no-preference' && responses.communityType !== 'No Preference') {
    maxScore += 40;
    if (dorm.community_type === responses.communityType) {
      score += 40;
    } else if (dorm.community_type === 'General' || dorm.community_type === 'general') {
      score += 20; // Partial match for general community
    }
  }

  const compatibilityPercentage = maxScore > 0 ? (score / maxScore) * 100 : 0;
  return Math.round(Math.min(100, Math.max(0, compatibilityPercentage)));
}

export function getTopRecommendations(dorms: Dorm[], responses: QuizResponses, limit: number = 5) {
  const scored = dorms.map(dorm => ({
    dorm,
    score: calculateCompatibility(dorm, responses),
  }));

  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}
