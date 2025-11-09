import requests
import json
import time
import random
from typing import Dict, List, Any

# --- CONFIGURATION ---
API_KEY = "AIzaSyALLHOBIc97LBdV99DS38Y94ouAoT2AaPE"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
MODEL_NAME = "gemini-2.5-pro"
# EFFICIENCY FIX: Reduced max retries (from 10 to 5) and added initial timeout
MAX_RETRIES = 5
INITIAL_TIMEOUT = 10 

# -----------------------------------------------------------------------------
## ACADEMIC ZONE AND PROXIMITY DATA (CALIBRATED)
# -----------------------------------------------------------------------------

# Fallback Map (Major-based): Used only if 'college' field is missing or generic.
ACADEMIC_FOCUS_TO_ZONE_MAP = {
    'Computer Science': 'North Science Hub', 'Engineering': 'North Science Hub', 'Physics': 'North Science Hub',      
    'Chemistry': 'North Science Hub', 'Mathematics': 'North Science Hub', 'Biology': 'Central Science',        
    'Business': 'Central Core', 'Management': 'Central Core', 'General Studies': 'Central Core',
    'English': 'Southwest Humanities', 'History': 'Southwest Humanities', 'Languages': 'Southwest Humanities',
    'General': 'Central Core', 'Afro-American Studies': 'Central Academic Hub', 'Anthropology': 'Central Academic Hub',          
    'Film and Video Studies': 'Central Academic Hub', 'Kinesiology': 'Northeast Academic Hub', 'Agriculture': 'Orchard Hill Academic Hub'      
}

# PRIMARY ACADEMIC PROXIMITY MAP (College-based, highly specific)
COLLEGE_TO_ZONE_MAP = {
    'Isenberg School of Management': 'Southwest Academic Hub', 'College of Natural Sciences': 'Orchard Hill Academic Hub', 
    'College of Info. & Computer Sciences': 'Northeast Academic Hub', 'Daniel J. Riccio Jr. College of Engineering': 'Northeast Academic Hub', 
    'College of Humanities and Fine Arts': 'Central Academic Hub', 'College of Social and Behavioral Sciences': 'Central Academic Hub', 
    'Elaine Marieb College of Nursing': 'Orchard Hill Academic Hub', 'School of Public Health and Health Sciences': 'Northeast Academic Hub',
    'College of Education': 'Northeast Academic Hub', 'Commonwealth Honors College': 'CHCRC Academic Hub',
    'General/Other': 'Central Academic Hub', 'Stockbridge School of Agriculture': 'Orchard Hill Academic Hub', 'School of Public Policy': 'Central Academic Hub'
}

# Maps Academic Zones to the optimal Dormitory Areas and their calculated proximity score (5=Best)
ACADEMIC_PROXIMITY_SCORES = {
    'Central Academic Hub': {'Central': 5, 'CHCRC': 4, 'Southwest': 4, 'Northeast': 3, 'Orchard Hill': 2, 'North': 3, 'Sylvan': 2},
    'Southwest Academic Hub': {'Southwest': 5, 'Central': 4, 'CHCRC': 3, 'Orchard Hill': 2, 'Northeast': 2, 'North': 2, 'Sylvan': 2},
    'Northeast Academic Hub': {'Northeast': 5, 'North': 4, 'Sylvan': 3, 'Orchard Hill': 3, 'Central': 2, 'CHCRC': 2, 'Southwest': 1},
    'Orchard Hill Academic Hub': {'Orchard Hill': 5, 'Central': 4, 'CHCRC': 3, 'Northeast': 3, 'Southwest': 2, 'North': 2, 'Sylvan': 3},
    'CHCRC Academic Hub': {'CHCRC': 5, 'Central': 5, 'Southwest': 4, 'Orchard Hill': 3, 'Northeast': 2, 'North': 2, 'Sylvan': 2},
    
    'Central Science': {'Central': 5, 'CHCRC': 5, 'Orchard Hill': 4, 'Northeast': 3, 'Southwest': 3, 'North': 2, 'Sylvan': 3},
    'North Science Hub': {'Northeast': 5, 'North': 4, 'Orchard Hill': 3, 'Central': 2, 'CHCRC': 2, 'Southwest': 1, 'Sylvan': 3},
}

# --- RESIDENTIAL AREA TO HALLS (For specific hall output) ---
RESIDENTIAL_AREA_TO_HALLS = {
    'Southwest': ['Cance Hall', 'James Hall', 'MacKimmie Hall', 'Kennedy Hall', 'Prince Hall', 'Melville Hall', 'Thoreau Hall'],
    'Central': ['Gorman Hall', 'Butterfield Hall', 'Brooks Hall', 'Chadbourne Hall', 'Greenough Hall', 'Van Meter Hall', 'Coolidge Hall'],
    'Northeast': ['Knowlton Hall', 'Crabtree Hall', 'Leach Hall', 'Hamlin Hall', 'Dwight Hall', 'Mary Lyon Hall', 'Johnson Hall'],
    'Orchard Hill': ['Webster Hall', 'Dickinson Hall', 'Grayson Hall', 'Field Hall'],
    'CHCRC': ['Oak Hall', 'Sycamore Hall', 'Birch Hall', 'Elm Hall', 'Maple Hall'],
    'North': ['North A', 'North B', 'North C', 'North D'], 
    'Sylvan': ['Brown Hall', 'Cashin Hall', 'McNamara Hall'], 
}

ACCOMMODATING_BREAK_AREAS = ['Central', 'Southwest', 'Orchard Hill', 'North', 'Sylvan', 'CHCRC'] 

# --- UMass Housing Context Data & LLM Prompts (Placeholder/Truncated for efficiency) ---
BREAK_HOUSING_CONTEXT = "..."
TWENTY_FOUR_HOUR_QUIET_CONTEXT = "..."
ALCOHOL_FREE_CONTEXT = "..."
SPECIAL_GENDER_HOUSING_CONTEXT = "..."
UMASS_DORM_CONTEXT = "..."
FIRST_YEAR_DORM_CONTEXT = "..."
DORM_SCHEMA = {"type": "OBJECT", "properties": {"recommendedDormArea": {"type": "STRING"}}, "required": ["recommendedDormArea"]}
LLM_SYSTEM_INSTRUCTION = "..."
MATCH_SCHEMA = {"type": "OBJECT", "properties": {"compatibilityScore": {"type": "INTEGER"}, "confidenceLevel": {"type": "STRING"}, "reasoningSummary": {"type": "STRING"}, "matchAdvice": {"type": "STRING"}}, "required": ["compatibilityScore", "confidenceLevel", "reasoningSummary", "matchAdvice"]}


# --- Core Functions ---

def make_api_call(payload: Dict[str, Any], schema: Dict[str, Any], system_instruction: str, url: str, is_scoring: bool = False) -> Dict[str, Any]:
    """Handles the robust API call with reduced retries and jittered exponential backoff."""
    headers = { 'Content-Type': 'application/json' }
    
    payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
    payload["generationConfig"] = {
        "responseMimeType": "application/json",
        "responseSchema": schema,
        "temperature": 0.0 if is_scoring else 0.2 
    }

    for i in range(MAX_RETRIES):
        try:
            timeout_val = INITIAL_TIMEOUT + (2 ** i) # Progressive timeout
            response = requests.post(
                f"{url}?key={API_KEY}", 
                headers=headers, 
                data=json.dumps(payload),
                timeout=timeout_val
            )
            response.raise_for_status()

            result = response.json()
            json_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')

            if json_text:
                return json.loads(json_text)
            else:
                raise ValueError("API returned no valid JSON content.")

        except requests.exceptions.RequestException as e:
            print(f"[API Call] Network/API Error on attempt {i+1}/{MAX_RETRIES}: {e}")
            if i < MAX_RETRIES - 1:
                # EFFICIENCY FIX: Jittered exponential backoff
                wait_time = (2 ** i) + random.uniform(0, 1.0)
                time.sleep(wait_time)
            else:
                raise ConnectionError(f"Persistent network/API error after {MAX_RETRIES} attempts.") from e
        
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[API Call] JSON Parsing Error on attempt {i+1}/{MAX_RETRIES}: {e}")
            if i < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                raise ValueError("Persistent JSON parsing error from AI output.") from e
        
        except Exception as e:
            print(f"[API Call] Unhandled Error on attempt {i+1}/{MAX_RETRIES}: {e}")
            raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e

def get_dorm_recommendation(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Determines the best residential area based on academic proximity."""
    
    college = profile.get('college', 'General/Other')
    primary_zone = COLLEGE_TO_ZONE_MAP.get(college, 'Central Academic Hub')
    
    # Fallback logic for majors
    if primary_zone == 'Central Academic Hub' and college == 'General/Other':
        major = profile.get('major', 'General')
        legacy_zone = ACADEMIC_FOCUS_TO_ZONE_MAP.get(major, 'Central Core')
        
        if legacy_zone == 'Central Science': primary_zone = 'Orchard Hill Academic Hub'
        elif legacy_zone == 'North Science Hub': primary_zone = 'Northeast Academic Hub'
        else: primary_zone = 'Central Academic Hub'
    
    recommended_area = 'Central' 
    if primary_zone in ACADEMIC_PROXIMITY_SCORES:
        dorm_scores = ACADEMIC_PROXIMITY_SCORES[primary_zone]
        recommended_area = max(dorm_scores, key=dorm_scores.get)
        
    recommended_halls = RESIDENTIAL_AREA_TO_HALLS.get(recommended_area, [])
    
    return {
        'recommendedArea': recommended_area,
        'recommendedHalls': recommended_halls,
    }

def score_match(profile_a: Dict[str, Any], profile_b: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates LLM compatibility scoring."""
    
    score = 88 # Default high score for simulation

    # Lower score if conflicting sleep habits
    if profile_a.get('sleepSchedule') == 'night-owl' and profile_b.get('sleepSchedule') == 'early-bird':
        score = 65
    elif profile_a.get('sleepSchedule') == 'early-bird' and profile_b.get('sleepSchedule') == 'night-owl':
        score = 65
    
    # Lower score if major conflict on social/noise
    elif profile_a.get('noiseLevel') == 'very-quiet' and profile_b.get('noiseLevel') == 'loud':
        score = 60
    
    elif profile_a.get('dormArea') == 'Central' and profile_b.get('dormArea') == 'Southwest':
        score = 78

    return {
        "compatibilityScore": score, 
        "confidenceLevel": "High",
        "reasoningSummary": f"Simulated score of {score}% based on alignment.",
        "matchAdvice": "Simulated advice.",
        "candidateName": profile_b.get('name', 'N/A'), 
        "candidateDorm": profile_b.get('dormArea', 'N/A'),
        "breakHousingPref": profile_b.get('breakHousingPref', 'no'), 
        "noiseLevel": profile_b.get('noiseLevel', 'quiet'),
        "genderInclusivePref": profile_b.get('genderInclusivePref', 'no-preference'),
        "alcoholPref": 'required' if profile_b.get('dormArea') == 'Central' and profile_b.get('name') == 'Sam' else 'no-preference', 
        "error": None
    }


def get_all_profiles_from_db(current_user_id: str, dorm_areas: List[str], student_year: str) -> List[Dict[str, Any]]:
    """Fetches and filters candidates based on area, year, and North/Sylvan restriction."""
    
    # Hardcoded simulation data (CLEANED)
    simulated_profiles = [
        # UPPERCLASSMEN
        {"userId": "candidate_2", "name": "Sam 'The Scholar'", "dormArea": "Central", "Hall": "Gorman Hall", "major": "Business", "yearPref": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "noiseLevel": "very-quiet", "college": "Isenberg School of Management", "genderInclusivePref": "single-gender", "breakHousingPref": "no", "alcoholPref": "no-preference"},
        {"userId": "candidate_3", "name": "Alex 'The Activist'", "dormArea": "Southwest", "Hall": "Cance Hall", "major": "English", "yearPref": "upperclassmen", "sleepSchedule": "night-owl", "tidiness": "messy", "noiseLevel": "loud", "college": "College of Humanities & Fine Arts", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "required", "alcoholPref": "no-preference"},
        {"userId": "candidate_4", "name": "Chris 'The Commuter'", "dormArea": "Central", "Hall": "Butterfield Hall", "major": "Mathematics", "yearPref": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "tidy", "noiseLevel": "quiet", "college": "College of Natural Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no", "alcoholPref": "no-preference"},
        {"userId": "candidate_7", "name": "Chloe 'The Honors Student'", "dormArea": "CHCRC", "Hall": "Oak Hall", "major": "History", "yearPref": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "noiseLevel": "quiet", "college": "Commonwealth Honors College", "genderInclusivePref": "no-preference", "breakHousingPref": "no", "alcoholPref": "no-preference"},
        {"userId": "candidate_8", "name": "David 'The Independent'", "dormArea": "North", "Hall": "North A", "major": "Computer Science", "yearPref": "upperclassmen", "sleepSchedule": "night-owl", "tidiness": "tidy", "noiseLevel": "quiet", "college": "College of Info. & Computer Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "required", "alcoholPref": "no-preference"},
        {"userId": "candidate_9", "name": "Ella 'The Quiet Scholar'", "dormArea": "Northeast", "Hall": "Knowlton Hall", "major": "Chemistry", "yearPref": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "noiseLevel": "very-quiet", "college": "College of Natural Sciences", "genderInclusivePref": "single-gender", "breakHousingPref": "no", "alcoholPref": "no-preference"},
        {"userId": "candidate_11", "name": "Grace 'The Apartment Seeker'", "dormArea": "North", "Hall": "North B", "major": "Management", "yearPref": "upperclassmen", "sleepSchedule": "balanced", "tidiness": "tidy", "noiseLevel": "quiet", "college": "Isenberg School of Management", "genderInclusivePref": "single-gender", "breakHousingPref": "required", "alcoholPref": "no-preference"},
        {"userId": "candidate_12", "name": "Hannah 'The Suite Seeker'", "dormArea": "Sylvan", "Hall": "Brown Hall", "major": "Computer Science", "yearPref": "upperclassmen", "sleepSchedule": "night-owl", "tidiness": "moderately-tidy", "noiseLevel": "moderate", "college": "College of Info. & Computer Sciences", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "required", "alcoholPref": "no-preference"},
        # FIRST-YEARS
        {"userId": "candidate_5", "name": "Jane 'The Engineer'", "dormArea": "Northeast", "Hall": "Crabtree Hall", "major": "Engineering", "yearPref": "first-years", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "noiseLevel": "very-quiet", "college": "Daniel J. Riccio Jr. College of Engineering", "genderInclusivePref": "single-gender", "breakHousingPref": "no", "alcoholPref": "no-preference"},
        {"userId": "candidate_6", "name": "Ben 'The Bio Major'", "dormArea": "Orchard Hill", "Hall": "Webster Hall", "major": "Biology", "yearPref": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "noiseLevel": "moderate", "college": "College of Natural Sciences", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "no", "alcoholPref": "no-preference"},
        {"userId": "candidate_10", "name": "Frank 'The Party-Goer'", "dormArea": "Southwest", "Hall": "Cance Hall", "major": "General Studies", "yearPref": "first-years", "sleepSchedule": "night-owl", "tidiness": "messy", "noiseLevel": "loud", "college": "General/Other", "genderInclusivePref": "no-preference", "breakHousingPref": "required", "alcoholPref": "no-preference"},
    ]
    
    required_year = student_year.lower()
    
    # Define areas restricted to upperclassmen (North/Sylvan)
    restricted_upperclass_areas = ['north', 'sylvan']
    
    filtered_profiles = [
        p for p in simulated_profiles 
        if p['userId'] != current_user_id 
        and p['dormArea'] in dorm_areas
        and p['yearPref'].lower() == required_year
        # BLOCK: If freshman AND the area is North/Sylvan
        and not (p['dormArea'].lower() in restricted_upperclass_areas and required_year == 'first-years')
    ]
    
    print(f"Filtered down to {len(filtered_profiles)} candidates matching the target areas {dorm_areas} and year '{student_year}'.")
    return filtered_profiles

def final_logistical_filter(user_profile: Dict[str, Any], successful_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Applies non-negotiable logistical filters (Break Housing, Noise, Alcohol, Gender) as a final check."""
    
    filtered_list = []
    
    # User's Critical Preferences
    user_break = user_profile.get('breakHousingPref', 'no')
    user_noise = user_profile.get('noiseLevel', 'balanced')
    user_gender_pref = user_profile.get('genderInclusivePref', 'no-preference')
    user_alcohol_pref = user_profile.get('alcoholPref', 'no-preference') 
    
    ACCOMMODATING_BREAK_AREAS = ['Central', 'Southwest', 'Orchard Hill', 'North', 'Sylvan', 'CHCRC'] 
    
    for match in successful_matches:
        is_logistically_compatible = True
        candidate_area = match.get('candidateDorm')
        candidate_noise = match.get('noiseLevel', 'balanced')
        candidate_gender_pref = match.get('genderInclusivePref', 'no-preference')

        # 1. Break Housing Check (User requires it, Area must accommodate)
        if user_break == 'required' and candidate_area not in ACCOMMODATING_BREAK_AREAS:
            is_logistically_compatible = False
        
        # 2. Noise Level Check (Very Quiet vs Loud Conflict)
        if (user_noise == 'very-quiet' and candidate_noise == 'loud') or \
           (user_noise == 'loud' and candidate_noise == 'very-quiet'):
            is_logistically_compatible = False
            
        # 3. Alcohol-Free Check (If user requires AF, cannot be matched to loud/party areas)
        if user_alcohol_pref == 'required':
            if candidate_area == 'Southwest':
                 is_logistically_compatible = False
            if candidate_noise == 'loud':
                 is_logistically_compatible = False
                 
        # 4. Gender Check (Conflict if user needs Single-Gender but candidate explicitly prefers GIH)
        if user_gender_pref == 'single-gender':
            if candidate_gender_pref == 'gender-inclusive':
                is_logistically_compatible = False

        if is_logistically_compatible:
            filtered_list.append(match)
            
    return filtered_list


def score_and_rank_matches(current_profile: Dict[str, Any], current_user_id: str) -> Dict[str, Any]:
    """
    Main orchestration function with 75% compatibility filtering and trait-based fallback.
    """
    if API_KEY == "AIzaSyALLHOBIc97LBdV99DS38Y94ouAoT2AaPE":
        # NOTE: In a live environment, this check would fail or require a valid key
        pass 

    # --- STAGE 1: High Compatibility Match (Location Priority) ---
    print("\n--- STAGE 1: Prioritizing Academic Location Match ---")
    
    location_rec = get_dorm_recommendation(current_profile)
    recommended_area = location_rec['recommendedArea']
    
    # Filter candidates to the single ideal residential area
    candidate_profiles = get_all_profiles_from_db(current_user_id, [recommended_area], current_profile.get('studentYear'))

    match_results = []
    
    if candidate_profiles:
        for candidate in candidate_profiles:
            result = score_match(current_profile, candidate)
            match_results.append(result)

        successful_matches = [m for m in match_results if m.get('compatibilityScore', 0) >= 75]
        successful_matches = final_logistical_filter(current_profile, successful_matches)
        successful_matches.sort(key=lambda x: x['compatibilityScore'], reverse=True)
    else:
        successful_matches = []

    # --- STAGE 2: Fallback to Trait Priority (Broader Search) ---
    if not successful_matches:
        print(f"\n--- STAGE 2: FALLBACK TRIGGERED ---")
        
        print(f"ALERT: No one matching your personality traits (>= 75%) and logistical requirements was found within your primary area: {recommended_area}. User needs to change settings or accept a broader search.")
        print("SIMULATION: Searching ALL residential areas for a high trait match, ignoring location.")
        
        fallback_profile = current_profile.copy()
        fallback_profile['priorityLocation'] = '5' 
        fallback_profile['priorityPrivacy'] = '1'  
        fallback_profile['prioritySocial'] = '1'   

        all_areas = list(RESIDENTIAL_AREA_TO_HALLS.keys())
        all_candidate_profiles = get_all_profiles_from_db(current_user_id, all_areas, current_profile.get('studentYear'))
        
        fallback_match_results = []
        if all_candidate_profiles:
            for candidate in all_candidate_profiles:
                 result = score_match(fallback_profile, candidate)
                 fallback_match_results.append(result)

            successful_matches = [m for m in fallback_match_results if m.get('compatibilityScore', 0) >= 75]
            successful_matches = final_logistical_filter(current_profile, successful_matches)
            successful_matches.sort(key=lambda x: x['compatibilityScore'], reverse=True)

        if not successful_matches:
             return {
                "dorm_recommendation": recommended_area,
                "ranked_matches": [],
                "message": f"No highly compatible matches were found even after broadening the search across all residential areas based on personality traits. Consider changing your preference settings."
            }

        recommended_area = successful_matches[0]['candidateDorm']
        print(f"Found {len(successful_matches)} trait matches. Recommending dorm area: {recommended_area}")

    # --- Final Results Formatting (Dorm Hall Output) ---
    final_output = {
        "dorm_recommendation": recommended_area,
        "ranked_matches": [],
        "message": ""
    }
    
    for match in successful_matches:
        # We try to use the specific Hall name defined in the candidate profile,
        # or fall back to the most proximate hall if not available.
        specific_hall = match.get('Hall', RESIDENTIAL_AREA_TO_HALLS.get(match['candidateDorm'], ["Hall data unavailable."])[0])
        
        hall_info = f"Best Match Hall: {specific_hall}" 

        final_output["ranked_matches"].append({
            "compatibilityScore": match['compatibilityScore'],
            "candidateName": match['candidateName'],
            "recommendedDorms": hall_info,
            "matchAdvice": match['matchAdvice']
        })

    return final_output


# --- EXAMPLE EXECUTION (TEST SUITE) ---
if __name__ == "__main__":
    
    # NOTE: The Hall field is now explicitly included in the test profile definitions
    # to demonstrate the simulated location for the user being tested.
    test_profiles = [
        # Test Case 1: Freshman Engineer (Freshman, Engineering -> Northeast)
        {
            "userId": "test_case_1", "name": "Freshman Engineer (Case 1)", "major": "Engineering", 
            "dormArea": "Northeast", "Hall": "Crabtree Hall",
            "roomType": "double", "genderPref": "coed", "accessible": "no", "studentYear": "first-years", "commuteDistance": "under-5min",
            "sleepSchedule": "early-bird", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "rarely", 
            "socialLevel": "minimal-social", "noiseLevel": "very-quiet", "environmentPref": "quiet-academic", 
            "communityType": "academic-focused", "sharedInterests": "very-important", 
            "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4",
            "college": "Daniel J. Riccio Jr. College of Engineering", "genderInclusivePref": "single-gender", "breakHousingPref": "no",
            "alcoholPref": "no-preference",
        },
        
        # Test Case 2: Upperclassman Fallback (Upperclassman, Honors -> CHCRC)
        {
            "userId": "test_case_2", "name": "Upperclassman Fallback (Case 2)", "major": "History", 
            "dormArea": "CHCRC", "Hall": "Oak Hall",
            "roomType": "single", "genderPref": "all-female", "accessible": "no", "studentYear": "upperclassmen", "commuteDistance": "5-10min",
            "sleepSchedule": "night-owl", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "rarely", 
            "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "balanced", 
            "communityType": "honors-focused", "sharedInterests": "important", 
            "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4",
            "college": "Commonwealth Honors College", "genderInclusivePref": "no-preference", "breakHousingPref": "no",
            "alcoholPref": "no-preference",
        },
        
        # Test Case 3: Freshman Block & CICS Check (Freshman CICS -> Northeast)
        {
            "userId": "test_case_3", "name": "Freshman Block & CICS Check (Case 3)", "major": "Computer Science", 
            "dormArea": "Northeast", "Hall": "Knowlton Hall",
            "roomType": "double", "genderPref": "coed", "accessible": "no", "studentYear": "first-years", "commuteDistance": "5-10min",
            "sleepSchedule": "balanced", "tidiness": "tidy", "noiseLevel": "quiet", "college": "College of Info. & Computer Sciences", 
            "genderInclusivePref": "no-preference", "breakHousingPref": "no", 
            "alcoholPref": "no-preference",
        },
        
        # Test Case 4: Logistical FAIL ALL (Upperclassman, Alcohol Free Required)
        {
            "userId": "test_case_4", "name": "Upperclassman Logistical Fail (Case 4)", "major": "General Studies", 
            "dormArea": "Central", "Hall": "Brooks Hall",
            "roomType": "double", "genderPref": "coed", "accessible": "no", "studentYear": "upperclassmen", "commuteDistance": "10-15min",
            "sleepSchedule": "early-bird", "tidiness": "very-tidy", "noiseLevel": "very-quiet", "college": "General/Other", "genderInclusivePref": "single-gender", 
            "breakHousingPref": "no", "alcoholPref": "required",
        }
    ]

    print(f"--- Running UMass Roommate Matcher Backend TEST SUITE ---")
    
    for i, profile in enumerate(test_profiles):
        print("\n" + "="*80)
        print(f"Executing Test Case {i+1}: {profile['name']}")
        print("="*80)

        final_results = score_and_rank_matches(profile, profile['userId'])
        
        # --- Final Results Summary for Test Case ---
        print("\n--- Test Case Results Summary ---")
        
        dorm_rec = final_results.get('dorm_recommendation')
        if dorm_rec:
            print(f"Recommended Residential Area (Final Selection): {dorm_rec}")

        ranked_matches = final_results.get('ranked_matches', [])
        
        if ranked_matches:
            print(f"\n--- Ranked Match List ({len(ranked_matches)} Matches Found) ---")
            for j, match in enumerate(ranked_matches):
                score = match['compatibilityScore']
                name = match['candidateName']
                dorms = match['recommendedDorms']
                advice = match['matchAdvice']
                # CLEANED OUTPUT: Show the specific dorm name, stripped of extra formatting
                cleaned_dorm = dorms.replace('Best Match Hall: ', '').replace('**', '')
                print(f"#{j+1}: {name} ({score}%) - Dorm: {cleaned_dorm} - Advice: {advice}")
        
        elif final_results.get('message'):
            print(final_results['message'])
            
    print("\n" + "="*80)
    print("Test Suite Complete.")