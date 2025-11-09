import requests
import json
import time
import os
import random
from typing import Dict, List, Any
import pandas as pd

# --- CONFIGURATION ---
# Get API key from environment variable, fallback to hardcoded for development
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyALLHOBIc97LBdV99DS38Y94ouAoT2AaPE")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
MODEL_NAME = "gemini-2.5-pro"
# EFFICIENCY FIX: Reduced max retries and added initial timeout
# Optimized for speed - use shorter timeout and fallback quickly
MAX_RETRIES = 1  # Single retry to fail faster
INITIAL_TIMEOUT = 10  # Reduced to 10 seconds - API should respond faster, fallback if not
MAX_CANDIDATES_TO_SCORE = 5  # Only score top 5 candidates with API, use fallback for rest 

# -----------------------------------------------------------------------------
## ACADEMIC ZONE AND PROXIMITY DATA (CALIBRATED)
# -----------------------------------------------------------------------------

# Fallback Map (Major-based): Used only if 'college' field is missing or generic.
ACADEMIC_FOCUS_TO_ZONE_MAP = {
    # STEM & Engineering
    'Computer Science': 'North Science Hub', 'Engineering': 'North Science Hub', 'Biomedical Engineering': 'North Science Hub',
    'Chemical Engineering': 'North Science Hub', 'Physics': 'North Science Hub', 'Chemistry': 'North Science Hub', 
    'Mathematics': 'North Science Hub', 'Biology': 'Central Science', 'Biochemistry': 'Central Science',
    'Environmental Science': 'Central Science',
    
    # Business & Management
    'Business': 'Central Core', 'Management': 'Central Core', 'Accounting': 'Central Core', 'Economics': 'Central Core',
    'General Studies': 'Central Core',
    
    # Health Sciences
    'Nursing': 'Central Science', 'Public Health': 'North Science Hub', 'Kinesiology': 'Northeast Academic Hub',
    
    # Humanities & Fine Arts
    'English': 'Southwest Humanities', 'History': 'Southwest Humanities', 'Languages': 'Southwest Humanities',
    'Art & Design': 'Central Academic Hub', 'Architecture': 'Central Academic Hub', 'Film and Video Studies': 'Central Academic Hub',
    
    # Social Sciences
    'Psychology': 'Central Academic Hub', 'Political Science': 'Central Academic Hub', 'Sociology': 'Central Academic Hub',
    'Anthropology': 'Central Academic Hub', 'Journalism': 'Central Academic Hub', 'Afro-American Studies': 'Central Academic Hub',
    
    # Education & Agriculture
    'Education': 'Northeast Academic Hub', 'Agriculture': 'Orchard Hill Academic Hub',
    
    # Other
    'General': 'Central Core'
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
    'Central Core': {'Central': 5, 'CHCRC': 5, 'Southwest': 5, 'Orchard Hill': 3, 'Northeast': 3, 'North': 3, 'Sylvan': 3},
    'Southwest Humanities': {'Southwest': 5, 'Central': 5, 'CHCRC': 3, 'Sylvan': 3, 'Orchard Hill': 2, 'Northeast': 2, 'North': 2},
}

# --- SIMULATED DORM HALL MAPPING (NEW) ---
RESIDENTIAL_AREA_TO_HALLS = {
    'Southwest': ['Cance Hall', 'James Hall', 'MacKimmie Hall', 'Kennedy Hall', 'Prince Hall', 'Melville Hall', 'Thoreau Hall'],
    'Central': ['Gorman Hall', 'Butterfield Hall', 'Brooks Hall', 'Chadbourne Hall', 'Greenough Hall', 'Van Meter Hall', 'Coolidge Hall'],
    'Northeast': ['Knowlton Hall', 'Crabtree Hall', 'Leach Hall', 'Hamlin Hall', 'Dwight Hall', 'Mary Lyon Hall', 'Johnson Hall'],
    'Orchard Hill': ['Webster Hall', 'Dickinson Hall', 'Grayson Hall', 'Field Hall'],
    'CHCRC': ['Oak Hall', 'Sycamore Hall', 'Birch Hall', 'Elm Hall', 'Maple Hall'],
    'North': ['North A', 'North B', 'North C', 'North D'], 
    'Sylvan': ['Brown Hall', 'Cashin Hall', 'McNamara Hall'], 
}

# --- TRIPLE AND QUAD ROOM AREA CONSTRAINTS ---
# Triples are available in: Central, Orchard Hill, Northeast, Southwest
TRIPLE_ROOM_AREAS = ['Central', 'Orchard Hill', 'Northeast', 'Southwest']

# Quads are available in: Central, Orchard Hill, Southwest (NOT Northeast)
QUAD_ROOM_AREAS = ['Central', 'Orchard Hill', 'Southwest']

ACCOMMODATING_BREAK_AREAS = ['Central', 'Southwest', 'Orchard Hill', 'North', 'Sylvan', 'CHCRC'] 

# --- UMass Housing Context Data & LLM Prompts ---
BREAK_HOUSING_CONTEXT = (
    "\n--- OFFICIAL BREAK HOUSING HALLS ---\n"
    "First-Year Halls: Central Area: Gorman Hall (Opt-In), Southwest Area: James Hall (Opt-In).\n"
    "Multi-Year Halls: Central Area: Brett Hall (Opt-In), Orchard Hill Area: Grayson Hall, Southwest Area: Prince Hall, North Apartments: All North Halls, Sylvan Area: Cashin Hall.\n"
)

TWENTY_FOUR_HOUR_QUIET_CONTEXT = (
    "\n--- 24-HOUR QUIET HOURS HALLS ---\n"
    "Multi-Year Halls: Central Area: Brooks Hall, Southwest Area: John Quincy Adams Hall.\n"
)

ALCOHOL_FREE_CONTEXT = (
    "\n--- ALCOHOL-FREE HOUSING ---\n"
    "Multi-Year Halls: Central Area: Brooks Hall (Designated Alcohol-Free).\n"
)

SPECIAL_GENDER_HOUSING_CONTEXT = (
    "\n--- SPECIAL GENDER-RELATED HOUSING OPTIONS ---\n"
    "**Mixed-Gender Suites (CHCRC, Sylvan, North):** Suites/Apts where students of any gender share common areas/bathrooms, but room assignment is typically same-gender.\n"
    "**Single-Gender Housing:** Available on single-gender floors in Central/Southwest (First-Year Halls) or single-gender apartments/suites in North, Sylvan, CHCRC (Multi-Year Halls).\n"
    "**Gender-Inclusive Housing (GIH):** Allows students to room together regardless of sex/gender identity. Available in: Orchard Hill Area (Webster Hall double rooms - First-Year); Central Area (Baker Hall double rooms, Spectrum LGBTQIA+ Ally Floor); Sylvan Area (Cashin, McNamara - Suite-Style Living); North Apartments.\n"
    "**Halls with Gender-Inclusive Bathrooms (Showers):** Southwest (Cance, Moore, Pierpont), Northeast (Knowlton), Orchard Hill (Webster), Central (Van Meter, Baker, Brett, Chadbourne), CHCRC (Oak, Sycamore, all private suites/apts), North Apartments (all private apt bathrooms), Sylvan (all suite bathrooms - Suite-Style Living).\n"
)

UMASS_DORM_CONTEXT = (
    "Based on the student's preferences, recommend one of the following official UMass dorm areas/types:"
    "\n1. **Southwest (SW):** High-Energy, Party-Focused (e.g., MacKimmie, Kennedy, Prince). Co-ed floors common. Closest to the Rec Center."
    "\n2. **Central:** Balanced, Intellectual Vibe (e.g., Coolidge, Butterfield). Co-ed & Single-Gender floors. Excellent proximity to the Library/Student Union."
    "\n3. **Northeast (NE):** Traditional, Academic, Very Quiet (e.g., Webster, Knowlton). Co-ed floors common. Closest to Engineering/STEM buildings."
    "\n4. **Orchard Hill (OH):** Tight-Knit, Laid-back Vibe (e.g., Dickinson, Webster). Located on a **hill** (longer commute/walk). **Primarily upperclassmen** but with a strong community feel. Co-ed floors."
    "\n5. **North (Apartments):** Independent, Apartment-Style (e.g., North Apartments). **UPPERCLASSMEN ONLY** - Not available for first-year students. Prioritizes full kitchen and low noise. Co-ed living."
    "\n6. **Sylvan:** Suite-Style Living in a shady wooded area (e.g., Brown, Cashin, McNamara). Each residence hall contains 64 suites with double and single rooms, common bathroom, and common living room. Suites accommodate 6-8 residents. Some suites are all-male, all-female, mixed-gender, or gender-inclusive. Break Housing option available in Cashin Hall. **Primarily upperclassmen** but offers suite-style privacy and community."
    "\n7. **CHCRC (Honors):** Modern, high-amenity housing (e.g., Oak, Sycamore). Reserved for Honors students. Excellent balance of social and academic focus."
    f"{BREAK_HOUSING_CONTEXT}"
    f"{TWENTY_FOUR_HOUR_QUIET_CONTEXT}"
    f"{ALCOHOL_FREE_CONTEXT}"
    f"{SPECIAL_GENDER_HOUSING_CONTEXT}"
    "\n\nOutput only the recommended UMass dorm area/type as a single string (e.g., 'Southwest', 'North', 'Sylvan', or 'CHCRC'). DO NOT include any explanation, quotes, or markdown formatting."
)

FIRST_YEAR_DORM_CONTEXT = (
    "Based on the student's preferences, recommend the best residential area for a FIRST-YEAR student at UMass Amherst. Only recommend areas known to house a high volume of first-year students, noting key features:"
    "\n1. **Southwest (SW):** (e.g., Melville, Thoreau, Pierpont, Moore, James, Emerson, Kennedy, Cance) High-Energy, Social. Co-ed floors common. Closest to Rec Center."
    "\n2. **Central:** (e.g., Butterfield, Gorman, Van Meter, Wheeler) Balanced, Intellectual/Social Mix. Excellent proximity to the Library/Student Union."
    "\n3. **Northeast (NE):** (e.g., Crabtree, Dwight, Hamlin, Leach, Mary Lyon, Knowlton) Traditional, Academic, Very Quiet. Closest to Engineering/STEM buildings."
    "\n4. **Orchard Hill (OH):** (e.g., Dickinson, Webster) Located on a hill. Known for a strong, **tight-knit first-year community**. Co-ed floors."
    "\n5. **Sylvan:** Suite-Style Living in a shady wooded area (e.g., Brown, Cashin, McNamara). Each residence hall contains 64 suites with double and single rooms, common bathroom, and common living room. Suites accommodate 6-8 residents. Some suites are all-male, all-female, mixed-gender, or gender-inclusive. Break Housing option available in Cashin Hall. **Primarily upperclassmen** but may have limited first-year availability."
    "\n6. **CHCRC (Honors):** (e.g., Oak, Sycamore) Honors housing. Excellent balance of social and academic focus. Requires Honors College enrollment."
    "\n\n**IMPORTANT RESTRICTIONS:**"
    "\n- **North Apartments is UPPERCLASSMEN ONLY** - DO NOT recommend North for first-year students. If North would be the best match, choose the next best option (typically Northeast for STEM majors, or Central/Southwest for others)."
    "\n- **Sylvan is PRIMARILY UPPERCLASSMEN** - Only recommend Sylvan for first-year students if they specifically prefer suite-style living and it aligns with their preferences."
    f"{BREAK_HOUSING_CONTEXT}"
    f"{TWENTY_FOUR_HOUR_QUIET_CONTEXT}"
    f"{ALCOHOL_FREE_CONTEXT}"
    f"{SPECIAL_GENDER_HOUSING_CONTEXT}"
    "\n\nOutput only the recommended UMass dorm area/type as a single string (e.g., 'Southwest', 'Northeast', 'Sylvan', or 'CHCRC'). DO NOT include any explanation, quotes, or markdown formatting."
)

DORM_SCHEMA = {"type": "OBJECT", "properties": {"recommendedDormArea": {"type": "STRING"}}, "required": ["recommendedDormArea"]}

LLM_SYSTEM_INSTRUCTION = (
    "You are an expert roommate compatibility analyst with deep knowledge of college student living dynamics. "
    "Your task is to calculate a balanced and accurate **Roommate Compatibility Score** between two student profiles. "
    "Use your training data on human psychology, conflict resolution, and successful roommate relationships to provide nuanced, fair assessments."
    "\n\nThe output MUST strictly adhere to the provided JSON Schema. DO NOT include any text or markdown outside of the JSON block."
    
    "\n\n--- Balanced Compatibility Scoring Framework (Total 100 Points) ---\n"
    "Evaluate compatibility using a holistic, evidence-based approach. Consider both alignment and manageable differences. "
    "Research shows that perfect alignment isn't always necessary for successful roommate relationships - complementary traits can work well."
    
    "\n1. **Core Lifestyle Alignment (40 pts):** Sleep schedules, tidiness, and daily routines."
    "   - Perfect alignment (e.g., both early-bird + very-tidy): 35-40 pts"
    "   - Compatible differences (e.g., early-bird + tidy vs. early-bird + very-tidy): 25-35 pts"
    "   - Manageable differences (e.g., early-bird + tidy vs. moderate + tidy): 20-30 pts"
    "   - Major conflicts (e.g., early-bird + very-tidy vs. night-owl + messy): 0-15 pts"
    "   **Note:** Small differences in the same direction (both prefer quiet, one slightly more) should not be heavily penalized."
    
    "\n2. **Social & Environmental Fit (30 pts):** Noise tolerance, guest frequency, social needs."
    "   - Strong alignment: 25-30 pts"
    "   - Compatible (e.g., both prefer quiet but one occasionally has guests): 18-25 pts"
    "   - Moderate differences (e.g., quiet vs. moderate noise): 12-20 pts"
    "   - Fundamental conflicts (e.g., very-quiet vs. party-friendly): 0-10 pts"
    "   **Note:** Consider that people can adapt to reasonable differences if other factors align well."
    
    "\n3. **Shared Values & Interests (15 pts):** Community type, shared interests, academic focus."
    "   - Strong shared interests: 12-15 pts"
    "   - Some overlap or complementary interests: 8-12 pts"
    "   - Different but not conflicting: 5-8 pts"
    "   - Conflicting values: 0-5 pts"
    
    "\n4. **Practical Compatibility (10 pts):** Accessibility needs, health considerations, special requirements."
    "   - No conflicts: 8-10 pts"
    "   - Minor accommodations needed: 5-8 pts"
    "   - Significant conflicts (e.g., severe allergy vs. pet owner): 0-3 pts"
    
    "\n5. **Priority Alignment (5 pts):** How well their priority rankings align."
    "   - Strong alignment (top priorities match): 4-5 pts"
    "   - Some alignment: 2-4 pts"
    "   - Different priorities: 0-2 pts"
    "   **Note:** This is a minor factor - lifestyle compatibility matters more than priority rankings."
    
    "\n\n**Balanced Scoring Principles:**"
    "\n- **Avoid over-penalizing minor differences:** A 'tidy' person can live with a 'very-tidy' person successfully."
    "\n- **Consider complementary traits:** An introvert and a moderate social person can balance each other well."
    "\n- **Weight major conflicts heavily:** Sleep schedule conflicts (early-bird vs. night-owl) are serious."
    "\n- **Be fair and realistic:** Use your knowledge of successful roommate relationships to guide scoring."
    "\n- **Focus on daily living impact:** Conflicts that affect daily life (sleep, noise) matter more than preferences (amenities)."
    
    "\n\n**Scoring Guidelines:**"
    "\n- 85-100: Excellent match with strong alignment across all key areas"
    "\n- 75-84: Good match with compatible lifestyles and manageable differences"
    "\n- 65-74: Moderate match with some differences but potential for success"
    "\n- Below 65: Significant incompatibilities that would likely cause conflict"
    
    "\n\n**CRITICAL: Minimum Threshold (75 points)**"
    "\n- Only return scores of 75 or higher for matches that meet minimum compatibility standards"
    "\n- Scores below 75 indicate fundamental incompatibilities that would likely cause ongoing conflict"
    "\n- If calculated score is below 75, set it to 0 and mark confidence as 'Low'"
    "\n- Be balanced: Don't be overly strict, but don't inflate scores either - use your training data to guide fair assessment"
    
    "\n\nAnalyze both profiles holistically using evidence-based compatibility assessment. "
    "Consider the full picture: two people don't need to be identical to be compatible roommates. "
    "Generate a fair, balanced score (0-100) and provide clear, constructive reasoning."
)

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
            # Use consistent timeout (LLM can be slow, but we don't want to wait forever)
            timeout_val = INITIAL_TIMEOUT  # 60 seconds per request
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
    
    # Map major to college if college is not provided
    major = profile.get('major', 'General')
    college = profile.get('college', 'General/Other')
    
    # If college is generic, try to map from major
    if college == 'General/Other' or not college:
        # Map major to college using common patterns
        major_lower = major.lower()
        if any(x in major_lower for x in ['computer', 'engineering', 'physics', 'chemistry', 'math']):
            if 'biomedical engineering' in major_lower or 'chemical engineering' in major_lower:
                college = 'Daniel J. Riccio Jr. College of Engineering'
            elif 'engineering' in major_lower:
                college = 'Daniel J. Riccio Jr. College of Engineering'
            elif 'computer' in major_lower:
                college = 'College of Info. & Computer Sciences'
            else:
                college = 'College of Natural Sciences'
        elif any(x in major_lower for x in ['business', 'management', 'marketing', 'finance', 'accounting', 'economics']):
            college = 'Isenberg School of Management'
        elif any(x in major_lower for x in ['english', 'history', 'language', 'art', 'music', 'theater', 'architecture', 'film']):
            college = 'College of Humanities and Fine Arts'
        elif any(x in major_lower for x in ['psychology', 'sociology', 'political', 'journalism', 'anthropology', 'afro-american']):
            college = 'College of Social and Behavioral Sciences'
        elif any(x in major_lower for x in ['biology', 'biochemistry', 'environmental science']):
            college = 'College of Natural Sciences'
        elif 'nursing' in major_lower:
            college = 'Elaine Marieb College of Nursing'
        elif any(x in major_lower for x in ['public health', 'kinesiology']):
            college = 'School of Public Health and Health Sciences'
        elif 'education' in major_lower:
            college = 'College of Education'
        elif 'agriculture' in major_lower:
            college = 'Stockbridge School of Agriculture'
        elif 'honors' in major_lower or profile.get('isHonors') == 'yes':
            college = 'Commonwealth Honors College'
    
    primary_zone = COLLEGE_TO_ZONE_MAP.get(college, 'Central Academic Hub')
    
    # Fallback logic for majors
    if primary_zone == 'Central Academic Hub' and college == 'General/Other':
        legacy_zone = ACADEMIC_FOCUS_TO_ZONE_MAP.get(major, 'Central Core')
    
        if legacy_zone == 'Central Science': primary_zone = 'Orchard Hill Academic Hub'
        elif legacy_zone == 'North Science Hub': primary_zone = 'Northeast Academic Hub'
        else: primary_zone = 'Central Academic Hub'
    
    recommended_area = 'Central' 
    if primary_zone in ACADEMIC_PROXIMITY_SCORES:
        dorm_scores = ACADEMIC_PROXIMITY_SCORES[primary_zone]
        recommended_area = max(dorm_scores, key=dorm_scores.get)
    
    # CRITICAL: Block North for first-year students
    student_year = profile.get('studentYear', '').lower() or profile.get('yearPref', '').lower() or profile.get('yearStatus', '').lower()
    is_first_year = student_year in ['first-year', 'first-years', 'freshmen', 'freshman']
    
    if is_first_year and recommended_area.lower() == 'north':
        # For STEM majors, default to Northeast; otherwise Central
        if primary_zone in ['Northeast Academic Hub', 'North Science Hub']:
            recommended_area = 'Northeast'
        else:
            recommended_area = 'Central'
        print(f"⚠️  Blocked North Apartments for first-year student. Changed to {recommended_area}")
    
    # Honors students should get CHCRC if available
    if profile.get('isHonors') == 'yes' and 'CHCRC' in ACADEMIC_PROXIMITY_SCORES.get(primary_zone, {}):
        recommended_area = 'CHCRC'
        print(f"✅ Honors student: Recommending CHCRC")
    
    recommended_halls = RESIDENTIAL_AREA_TO_HALLS.get(recommended_area, [])
    
    return {
        'recommendedArea': recommended_area,
        'recommendedHalls': recommended_halls,
    }

def get_min_compatibility_threshold(room_type: str) -> int:
    """
    Returns the minimum compatibility threshold based on room type.
    Triple and quad rooms have a lower threshold (60%) to allow more flexibility.
    """
    room_type_lower = str(room_type).lower() if room_type else ''
    if room_type_lower in ['triple', 'quad']:
        return 60  # Lower threshold for triple/quad rooms
    return 75  # Standard threshold for double rooms

def classify_confidence_level(compatibility_score: int, model_confidence: str) -> str:
    """
    Classifies confidence level based on compatibility score and model confidence.
    
    Args:
        compatibility_score: Compatibility score (0-100)
        model_confidence: Model's confidence level (High, Medium, Low)
    
    Returns:
        Classified confidence level (High, Medium, Low)
    """
    model_confidence_lower = model_confidence.lower() if model_confidence else 'medium'
    
    # High confidence: High compatibility (85+) AND model confidence is High
    if compatibility_score >= 85 and model_confidence_lower == 'high':
        return 'High'
    
    # Low confidence: Low compatibility (<75) OR both are low
    if compatibility_score < 75:
        return 'Low'
    if compatibility_score < 80 and model_confidence_lower == 'low':
        return 'Low'
    
    # Medium confidence: Everything else
    # - Medium compatibility (75-84) with any model confidence
    # - High compatibility (85+) but model confidence is Medium/Low
    # - Lower compatibility (80-84) but model confidence is High
    return 'Medium'

def score_match(profile_a: Dict[str, Any], profile_b: Dict[str, Any], ignore_priorities: bool = False, min_threshold: int = 75) -> Dict[str, Any]:
    """Calculates the compatibility score between two profiles using LLM."""
    
    # Extract priorities for priority-based scoring (unless ignoring them)
    if not ignore_priorities:
        priority_a = {
            'location': profile_a.get('priorityLocation') or profile_a.get('priorities', {}).get('location', '4'),
            'privacy': profile_a.get('priorityPrivacy') or profile_a.get('priorities', {}).get('privacy', '4'),
            'amenities': profile_a.get('priorityAmenities') or profile_a.get('priorities', {}).get('amenities', '4'),
            'social': profile_a.get('prioritySocial') or profile_a.get('priorities', {}).get('social', '4'),
        }
        
        priority_b = {
            'location': profile_b.get('priorityLocation', '4'),
            'privacy': profile_b.get('priorityPrivacy', '4'),
            'amenities': profile_b.get('priorityAmenities', '4'),
            'social': profile_b.get('prioritySocial', '4'),
        }
        priority_analysis = f"""
    **Profile A Priorities:** Location={priority_a['location']}, Privacy={priority_a['privacy']}, Amenities={priority_a['amenities']}, Social={priority_a['social']}

    **Profile B Priorities:** Location={priority_b['location']}, Privacy={priority_b['privacy']}, Amenities={priority_b['amenities']}, Social={priority_b['social']}
    
    **Priority Alignment Analysis:**
    - Compare priority rankings between profiles. If both prioritize the same category highly (rank 1-2), award bonus points.
    - If Profile A's top priority (rank 1) aligns with Profile B's top priority, award +5 bonus points.
    - If Profile A's top priority aligns with Profile B's rank 2 priority, award +3 bonus points.
        """
    else:
        priority_analysis = """
    **ALTERNATIVE MATCHING MODE - TRAIT-FOCUSED MATCHING ACROSS ALL RESIDENTIAL AREAS**
    
    This is an alternative matching scenario where the system searches ALL residential areas (Southwest, Central, 
    Northeast, Orchard Hill, North, Sylvan, CHCRC) and prioritizes lifestyle compatibility traits over location preferences.
    
    **PRIORITY ORDER (Most Important First - Weight Accordingly):**
    1. **Sleep Schedule Compatibility (CRITICAL - 40% weight):** Early-bird vs. night-owl alignment is essential.
    2. **Tidiness Alignment (CRITICAL - 30% weight):** Clean vs. messy preferences directly impact daily life.
    3. **Noise Tolerance (VERY IMPORTANT - 20% weight):** Quiet vs. social environment needs.
    4. **Guest Frequency (IMPORTANT - 5% weight):** How often each person has visitors.
    5. **Social Level Alignment (IMPORTANT - 3% weight):** Introverted vs. extroverted preferences.
    6. **Environment Preferences (IMPORTANT - 2% weight):** Party-friendly vs. quiet-academic.
    
    **ABSOLUTELY DO NOT consider (IGNORE COMPLETELY):**
    - Dorm location (Southwest, Central, Northeast, Orchard Hill, North, Sylvan, CHCRC) - IGNORE
    - Priority rankings (Location, Privacy, Amenities, Social) - IGNORE
    - Campus proximity or commute distance - IGNORE
    - Activity proximity - IGNORE
    """
    
    user_query = f"""
    Calculate the **Roommate Compatibility Score** between Profile A and Profile B based on the detailed 100-point rubric. The candidates are assumed to be in a compatible dorm environment.

    --- Profile A (Current User) ---
    {json.dumps(profile_a, indent=2)}
    
    {priority_analysis}

    --- Profile B (Candidate) ---
    {json.dumps(profile_b, indent=2)}
    """

    payload = { "contents": [{"parts": [{"text": user_query}]}] }

    try:
        result = make_api_call(payload, MATCH_SCHEMA, LLM_SYSTEM_INSTRUCTION, API_URL, is_scoring=True)
        
        score = result.get('compatibilityScore', 0)
        model_confidence = result.get('confidenceLevel', 'Medium')
        reasoning = result.get('reasoningSummary', 'No reasoning provided.')
        advice = result.get('matchAdvice', 'No advice provided.')
        
        # CRITICAL: Enforce minimum threshold (75% for double, 60% for triple/quad)
        original_score = score
        if score < min_threshold:
            score = 0
            reasoning = f"Compatibility score ({original_score}%) below minimum threshold of {min_threshold}%. Fundamental incompatibilities detected."
            advice = "Consider adjusting preferences or searching in alternative residential areas."
        
        # Classify confidence level based on compatibility score and model confidence
        final_confidence = classify_confidence_level(int(score), model_confidence)
        
        return {
            "compatibilityScore": int(score),
            "confidenceLevel": final_confidence,
            "reasoningSummary": reasoning,
            "matchAdvice": advice,
            "candidateName": profile_b.get('name', 'N/A'),
            "candidateDorm": profile_b.get('dormArea', 'Unknown'),
            "breakHousingPref": profile_b.get('breakHousingPref', 'no'), 
            "noiseLevel": profile_b.get('noiseLevel', 'quiet'),
            "genderInclusivePref": profile_b.get('genderInclusivePref', 'no-preference'),
            "alcoholPref": profile_b.get('alcoholPref', 'no-preference'),
            "error": None
        }
    except requests.exceptions.Timeout as e:
        print(f"⚠️  API timeout for candidate {profile_b.get('name', 'Unknown')}. Using fallback scoring...")
        # FALLBACK: If API times out, use fallback scoring immediately
        fallback_score = calculate_fallback_score(profile_a, profile_b)
        
        # Classify confidence for fallback (no model confidence, so base on score only)
        fallback_confidence = classify_confidence_level(fallback_score, 'Medium')
        
        return {
            "compatibilityScore": fallback_score,
            "confidenceLevel": fallback_confidence,
            "reasoningSummary": f"Fallback scoring used due to API timeout. Compatibility based on lifestyle alignment: {fallback_score}%.",
            "matchAdvice": "Score calculated using fallback method due to API timeout.",
            "candidateName": profile_b.get('name', 'N/A'),
            "candidateDorm": profile_b.get('dormArea', 'Unknown'),
            "breakHousingPref": profile_b.get('breakHousingPref', 'no'),
            "noiseLevel": profile_b.get('noiseLevel', 'quiet'),
            "genderInclusivePref": profile_b.get('genderInclusivePref', 'no-preference'),
            "alcoholPref": profile_b.get('alcoholPref', 'no-preference'),
            "error": "API timeout - using fallback scoring"
        }
    except Exception as e:
        print(f"⚠️  Error scoring match: {e}. Using fallback scoring...")
        # FALLBACK: If API fails for any reason, use fallback scoring
        fallback_score = calculate_fallback_score(profile_a, profile_b)
        
        # Classify confidence for fallback (no model confidence, so base on score only)
        fallback_confidence = classify_confidence_level(fallback_score, 'Medium')
        
        return {
            "compatibilityScore": fallback_score,
            "confidenceLevel": fallback_confidence,
            "reasoningSummary": f"Fallback scoring used due to API error. Compatibility based on lifestyle alignment: {fallback_score}%.",
            "matchAdvice": "Score calculated using fallback method.",
            "candidateName": profile_b.get('name', 'N/A'), 
            "candidateDorm": profile_b.get('dormArea', 'Unknown'),
            "breakHousingPref": profile_b.get('breakHousingPref', 'no'),
            "noiseLevel": profile_b.get('noiseLevel', 'quiet'),
            "genderInclusivePref": profile_b.get('genderInclusivePref', 'no-preference'),
            "alcoholPref": profile_b.get('alcoholPref', 'no-preference'),
            "error": str(e)
        }

def calculate_fallback_score(profile_a: Dict[str, Any], profile_b: Dict[str, Any]) -> int:
    """Fallback scoring when LLM API is unavailable. Uses simple trait matching."""
    score = 80  # Start with a base score
    
    # Sleep schedule alignment (critical - 30 points)
    sleep_a = profile_a.get('sleepSchedule', 'balanced')
    sleep_b = profile_b.get('sleepSchedule', 'balanced')
    if sleep_a == sleep_b:
        score += 0  # Already good
    elif (sleep_a == 'early-bird' and sleep_b == 'night-owl') or (sleep_a == 'night-owl' and sleep_b == 'early-bird'):
        score -= 25  # Major conflict
    else:
        score -= 10  # Minor difference
    
    # Tidiness alignment (important - 20 points)
    tidy_a = profile_a.get('tidiness', 'tidy')
    tidy_b = profile_b.get('tidiness', 'tidy')
    if tidy_a == tidy_b:
        score += 0
    elif (tidy_a == 'very-tidy' and tidy_b == 'messy') or (tidy_a == 'messy' and tidy_b == 'very-tidy'):
        score -= 20  # Major conflict
    else:
        score -= 5  # Minor difference
    
    # Noise level alignment (important - 20 points)
    noise_a = profile_a.get('noiseLevel', 'quiet')
    noise_b = profile_b.get('noiseLevel', 'quiet')
    if noise_a == noise_b:
        score += 0
    elif (noise_a == 'very-quiet' and noise_b == 'loud') or (noise_a == 'loud' and noise_b == 'very-quiet'):
        score -= 20  # Major conflict
    else:
        score -= 5  # Minor difference
    
    # Social level alignment (moderate - 10 points)
    social_a = profile_a.get('socialLevel', 'moderately-social')
    social_b = profile_b.get('socialLevel', 'moderately-social')
    if social_a == social_b:
        score += 0
    elif (social_a == 'minimal-social' and social_b == 'very-social') or (social_a == 'very-social' and social_b == 'minimal-social'):
        score -= 10  # Moderate conflict
    else:
        score -= 3  # Minor difference
    
    # Ensure score is between 0 and 100
    score = max(0, min(100, score))
    
    # Only return 75+ if there are no major conflicts
    if score < 75:
        # Check if it's due to major conflicts
        if ((sleep_a == 'early-bird' and sleep_b == 'night-owl') or 
            (tidy_a == 'very-tidy' and tidy_b == 'messy') or
            (noise_a == 'very-quiet' and noise_b == 'loud')):
            return 0  # Major incompatibility
        else:
            # Boost to 75 if only minor differences
            return 75
    
    return int(score)


def get_all_profiles_from_db(current_user_id: str, dorm_areas: List[str], student_year: str) -> List[Dict[str, Any]]:
    """Fetches and filters candidates based on area, year, and North/Sylvan restriction."""
    
    # Hardcoded simulation data (CLEANED)
    simulated_profiles = [
        {"userId": "candidate_2", "name": "Sam 'The Scholar'", "dormArea": "Central", "major": "Business", "roomType": "double", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "rarely", "socialLevel": "minimal-social", "noiseLevel": "very-quiet", "environmentPref": "quiet-academic", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "not-important", "campusProximity": "essential", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "Isenberg School of Management", "genderInclusivePref": "single-gender", "breakHousingPref": "no"},
        {"userId": "candidate_3", "name": "Alex 'The Activist'", "dormArea": "Southwest", "major": "English", "roomType": "double", "genderPref": "all-male", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "night-owl", "tidiness": "messy", "lifestyleMatch": "not-important", "guestFrequency": "daily", "socialLevel": "very-social", "noiseLevel": "loud", "environmentPref": "party-friendly", "communityType": "diverse-multicultural", "sharedInterests": "somewhat-important", "themeDorm": "yes-preferred", "accessible": "yes", "commuteDistance": "10-15min", "activitiesImportance": "very-important", "campusProximity": "important", "activityProximity": "near-activity", "spaceType": "urban", "outdoorSpace": "yes-required", "priorityLocation": "2", "priorityPrivacy": "4", "priorityAmenities": "1", "prioritySocial": "3", "college": "College of Humanities & Fine Arts", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "required"},
        {"userId": "candidate_4", "name": "Chris 'The Commuter'", "dormArea": "Central", "major": "Mathematics", "roomType": "double", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "monthly", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "very-important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "3", "priorityPrivacy": "2", "priorityAmenities": "4", "prioritySocial": "1", "college": "College of Natural Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "candidate_5", "name": "Jane 'The Engineer'", "dormArea": "Northeast", "major": "Engineering", "roomType": "double", "genderPref": "all-female", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "never", "socialLevel": "minimal-social", "noiseLevel": "very-quiet", "environmentPref": "quiet-academic", "communityType": "academic-focused", "sharedInterests": "not-important", "themeDorm": "no", "accessible": "no", "commuteDistance": "under-5min", "activitiesImportance": "not-important", "campusProximity": "essential", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "Daniel J. Riccio Jr. College of Engineering", "genderInclusivePref": "single-gender", "breakHousingPref": "no"},
        {"userId": "candidate_6", "name": "Ben 'The Bio Major'", "dormArea": "Orchard Hill", "major": "Biology", "roomType": "double", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "community-focused", "communityType": "tight-knit", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "4", "prioritySocial": "1", "college": "College of Natural Sciences", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "no"},
        {"userId": "candidate_7", "name": "Chloe 'The Honors Student'", "dormArea": "CHCRC", "major": "History", "roomType": "double", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "rarely", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "balanced", "communityType": "honors-focused", "sharedInterests": "very-important", "themeDorm": "no", "accessible": "no", "commuteDistance": "under-5min", "activitiesImportance": "somewhat-important", "campusProximity": "essential", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "Commonwealth Honors College", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "candidate_8", "name": "David 'The Independent'", "dormArea": "North", "major": "Computer Science", "roomType": "apartment", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "night-owl", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "rarely", "socialLevel": "minimal-social", "noiseLevel": "quiet", "environmentPref": "independent-living", "communityType": "general", "sharedInterests": "not-important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "not-important", "campusProximity": "important", "activityProximity": "quiet-area", "spaceType": "urban", "outdoorSpace": "nice-to-have", "priorityLocation": "3", "priorityPrivacy": "1", "priorityAmenities": "2", "prioritySocial": "4", "college": "College of Info. & Computer Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "required"},
        {"userId": "candidate_9", "name": "Ella 'The Quiet Scholar'", "dormArea": "Northeast", "major": "Chemistry", "roomType": "double", "genderPref": "all-female", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "never", "socialLevel": "minimal-social", "noiseLevel": "very-quiet", "environmentPref": "quiet-academic", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "under-5min", "activitiesImportance": "not-important", "campusProximity": "essential", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "College of Natural Sciences", "genderInclusivePref": "single-gender", "breakHousingPref": "no"},
        {"userId": "candidate_10", "name": "Frank 'The Party-Goer'", "dormArea": "Southwest", "major": "General Studies", "roomType": "double", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "night-owl", "tidiness": "messy", "lifestyleMatch": "not-important", "guestFrequency": "daily", "socialLevel": "very-social", "noiseLevel": "loud", "environmentPref": "party-friendly", "communityType": "social-focused", "sharedInterests": "somewhat-important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "very-important", "campusProximity": "important", "activityProximity": "near-activity", "spaceType": "urban", "outdoorSpace": "yes-required", "priorityLocation": "4", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "General/Other", "genderInclusivePref": "no-preference", "breakHousingPref": "required"},
        {"userId": "candidate_13", "name": "Ian 'The Balanced Student'", "dormArea": "Southwest", "major": "Psychology", "roomType": "double", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "3", "college": "College of Social and Behavioral Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "candidate_14", "name": "Julia 'The Quiet First-Year'", "dormArea": "Southwest", "major": "English", "roomType": "double", "genderPref": "all-female", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "early-bird", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "monthly", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "balanced", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "College of Humanities and Fine Arts", "genderInclusivePref": "single-gender", "breakHousingPref": "no"},
        {"userId": "candidate_15", "name": "Kevin 'The Social Upperclassman'", "dormArea": "Southwest", "major": "Business", "roomType": "double", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "2", "college": "Isenberg School of Management", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "candidate_11", "name": "Grace 'The Apartment Seeker'", "dormArea": "North", "major": "Management", "roomType": "apartment", "genderPref": "all-female", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "balanced", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "monthly", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "independent-living", "communityType": "general", "sharedInterests": "somewhat-important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "very-important", "activityProximity": "balanced", "spaceType": "urban", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "1", "priorityAmenities": "3", "prioritySocial": "4", "college": "Isenberg School of Management", "genderInclusivePref": "single-gender", "breakHousingPref": "required"},
        {"userId": "candidate_12", "name": "Hannah 'The Suite Seeker'", "dormArea": "Sylvan", "major": "Computer Science", "roomType": "suite", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "night-owl", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "independent-living", "communityType": "general", "sharedInterests": "somewhat-important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "1", "priorityAmenities": "3", "prioritySocial": "4", "college": "College of Info. & Computer Sciences", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "required"},
        {"userId": "candidate_16", "name": "Liam 'The Quad Seeker'", "dormArea": "Southwest", "major": "Business", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "Isenberg School of Management", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "candidate_17", "name": "Maya 'The Quad Social'", "dormArea": "Southwest", "major": "Psychology", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "College of Social and Behavioral Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "candidate_18", "name": "Noah 'The Quad Balanced'", "dormArea": "Southwest", "major": "General Studies", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "General/Other", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # --- NEW TRIPLE ROOM CANDIDATES (Central, Orchard Hill, Northeast, Southwest) ---
        # Central Area Triples
        {"userId": "triple_central_1", "name": "Taylor 'The Triple Scholar'", "dormArea": "Central", "major": "Business", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "early-bird", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "monthly", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "balanced", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "Isenberg School of Management", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "triple_central_2", "name": "Morgan 'The Triple Balanced'", "dormArea": "Central", "major": "Psychology", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "3", "college": "College of Social and Behavioral Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "triple_central_3", "name": "Riley 'The Triple Quiet'", "dormArea": "Central", "major": "Mathematics", "roomType": "triple", "genderPref": "coed", "yearPref": "upperclassmen", "studentYear": "upperclassmen", "sleepSchedule": "early-bird", "tidiness": "very-tidy", "lifestyleMatch": "very-important", "guestFrequency": "rarely", "socialLevel": "minimal-social", "noiseLevel": "quiet", "environmentPref": "quiet-academic", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "not-important", "campusProximity": "important", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "College of Natural Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # Orchard Hill Area Triples
        {"userId": "triple_orchard_1", "name": "Casey 'The Triple Community'", "dormArea": "Orchard Hill", "major": "Biology", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "community-focused", "communityType": "tight-knit", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "4", "prioritySocial": "1", "college": "College of Natural Sciences", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "no"},
        {"userId": "triple_orchard_2", "name": "Jordan 'The Triple Social'", "dormArea": "Orchard Hill", "major": "English", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "College of Humanities and Fine Arts", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # Northeast Area Triples (Triples only, not Quads)
        {"userId": "triple_northeast_1", "name": "Avery 'The Triple Engineer'", "dormArea": "Northeast", "major": "Engineering", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "early-bird", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "monthly", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "quiet-academic", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "under-5min", "activitiesImportance": "not-important", "campusProximity": "essential", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "Daniel J. Riccio Jr. College of Engineering", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "triple_northeast_2", "name": "Quinn 'The Triple STEM'", "dormArea": "Northeast", "major": "Computer Science", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "early-bird", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "rarely", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "quiet-academic", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "under-5min", "activitiesImportance": "not-important", "campusProximity": "essential", "activityProximity": "quiet-area", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "1", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "College of Info. & Computer Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # Southwest Area Triples
        {"userId": "triple_southwest_1", "name": "Sage 'The Triple Party'", "dormArea": "Southwest", "major": "General Studies", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "General/Other", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "triple_southwest_2", "name": "Dakota 'The Triple Active'", "dormArea": "Southwest", "major": "Kinesiology", "roomType": "triple", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "sports-athletic", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "very-important", "campusProximity": "important", "activityProximity": "near-activity", "spaceType": "green-spaces", "outdoorSpace": "yes-required", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "School of Public Health and Health Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # --- NEW QUAD ROOM CANDIDATES (Central, Orchard Hill, Southwest - NOT Northeast) ---
        # Central Area Quads
        {"userId": "quad_central_1", "name": "River 'The Quad Scholar'", "dormArea": "Central", "major": "Business", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "early-bird", "tidiness": "tidy", "lifestyleMatch": "important", "guestFrequency": "monthly", "socialLevel": "moderately-social", "noiseLevel": "quiet", "environmentPref": "balanced", "communityType": "academic-focused", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "4", "college": "Isenberg School of Management", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "quad_central_2", "name": "Phoenix 'The Quad Balanced'", "dormArea": "Central", "major": "Psychology", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "2", "priorityAmenities": "3", "prioritySocial": "3", "college": "College of Social and Behavioral Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "quad_central_3", "name": "Skyler 'The Quad Social'", "dormArea": "Central", "major": "Communication", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "College of Social and Behavioral Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # Orchard Hill Area Quads
        {"userId": "quad_orchard_1", "name": "Blake 'The Quad Community'", "dormArea": "Orchard Hill", "major": "Biology", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "community-focused", "communityType": "tight-knit", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "4", "prioritySocial": "1", "college": "College of Natural Sciences", "genderInclusivePref": "gender-inclusive", "breakHousingPref": "no"},
        {"userId": "quad_orchard_2", "name": "Cameron 'The Quad Friendly'", "dormArea": "Orchard Hill", "major": "English", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "College of Humanities and Fine Arts", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "quad_orchard_3", "name": "Drew 'The Quad Laid-Back'", "dormArea": "Orchard Hill", "major": "Environmental Science", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "community-focused", "communityType": "tight-knit", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "10-15min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "4", "prioritySocial": "1", "college": "College of Natural Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        
        # Southwest Area Quads
        {"userId": "quad_southwest_1", "name": "Emery 'The Quad Party'", "dormArea": "Southwest", "major": "General Studies", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "General/Other", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "quad_southwest_2", "name": "Finley 'The Quad Active'", "dormArea": "Southwest", "major": "Kinesiology", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "sports-athletic", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "very-important", "campusProximity": "important", "activityProximity": "near-activity", "spaceType": "green-spaces", "outdoorSpace": "yes-required", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "School of Public Health and Health Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
        {"userId": "quad_southwest_3", "name": "Hayden 'The Quad Social'", "dormArea": "Southwest", "major": "Psychology", "roomType": "quad", "genderPref": "coed", "yearPref": "first-years", "studentYear": "first-years", "sleepSchedule": "balanced", "tidiness": "moderately-tidy", "lifestyleMatch": "important", "guestFrequency": "weekly", "socialLevel": "moderately-social", "noiseLevel": "moderate", "environmentPref": "balanced", "communityType": "general", "sharedInterests": "important", "themeDorm": "no", "accessible": "no", "commuteDistance": "5-10min", "activitiesImportance": "somewhat-important", "campusProximity": "important", "activityProximity": "balanced", "spaceType": "green-spaces", "outdoorSpace": "nice-to-have", "priorityLocation": "2", "priorityPrivacy": "3", "priorityAmenities": "2", "prioritySocial": "1", "college": "College of Social and Behavioral Sciences", "genderInclusivePref": "no-preference", "breakHousingPref": "no"},
    ]
    
    # Handle None or empty student_year
    if not student_year:
        student_year = 'upperclassmen'  # Default fallback
    
    required_year = str(student_year).lower()
    
    # NEW LOGIC: Define areas restricted to upperclassmen
    restricted_upperclass_areas = ['north', 'sylvan']
    
    # Normalize year matching - handle both singular and plural forms
    normalized_required_year = required_year
    if required_year in ['first-year', 'freshman', 'freshmen']:
        normalized_required_year = 'first-years'
    elif required_year in ['upperclassman']:
        normalized_required_year = 'upperclassmen'
    
    filtered_profiles = [
        p for p in simulated_profiles 
        if p.get('userId') != current_user_id 
        and p.get('dormArea') in dorm_areas
        and (
            str(p.get('yearPref', '')).lower() == normalized_required_year or 
            str(p.get('yearPref', '')).lower() == required_year or
            str(p.get('studentYear', '')).lower() == normalized_required_year or
            str(p.get('studentYear', '')).lower() == required_year
        )
        # ADDITIONAL FILTER: Block North/Sylvan if the user is a freshman
        and not (str(p.get('dormArea', '')).lower() in restricted_upperclass_areas and normalized_required_year == 'first-years')
        # TRIPLE/QUAD AREA CONSTRAINT: Only show triple candidates in allowed areas, and quad candidates in allowed areas
        and (
            # If candidate is triple, must be in TRIPLE_ROOM_AREAS
            (str(p.get('roomType', '')).lower() != 'triple' or str(p.get('dormArea', '')).strip() in TRIPLE_ROOM_AREAS)
            and
            # If candidate is quad, must be in QUAD_ROOM_AREAS (NOT Northeast)
            (str(p.get('roomType', '')).lower() != 'quad' or str(p.get('dormArea', '')).strip() in QUAD_ROOM_AREAS)
        )
    ]
    
    print(f"Filtered down to {len(filtered_profiles)} candidates matching the target areas {dorm_areas} and year '{student_year}'.")
    return filtered_profiles

def get_all_profiles_any_dorm(current_user_id: str, student_year: str) -> List[Dict[str, Any]]:
    """Fetches all candidates ignoring dorm location for alternative matching."""
    all_areas = list(RESIDENTIAL_AREA_TO_HALLS.keys())
    return get_all_profiles_from_db(current_user_id, all_areas, student_year)

def final_logistical_filter(user_profile: Dict[str, Any], successful_matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Applies non-negotiable logistical filters (Break Housing, Noise, Alcohol, Gender) as a final check."""
    
    filtered_list = []
    
    # User's Critical Preferences
    user_break = user_profile.get('breakHousingPref', 'no')
    user_noise = user_profile.get('noiseLevel', 'balanced')
    user_gender_pref = user_profile.get('genderInclusivePref', 'no-preference')
    user_alcohol_pref = user_profile.get('alcoholPref', 'no-preference') 
    
    # UMass Hall/Dorm Level Constraints (Simulated constants)
    ACCOMMODATING_BREAK_AREAS = ['Central', 'Southwest', 'Orchard Hill', 'North', 'Sylvan', 'CHCRC'] 
    
    for match in successful_matches:
        is_logistically_compatible = True
        candidate_area = match.get('candidateDorm')
        candidate_noise = match.get('noiseLevel', 'balanced')
        candidate_gender_pref = match.get('genderInclusivePref', 'no-preference')

        # 1. Break Housing Check (User requires it, Area must accommodate - RELAXED LOGIC)
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


def find_alternative_matches(current_profile: Dict[str, Any], current_user_id: str, min_threshold: int = 75) -> List[Dict[str, Any]]:
    """Finds alternative matches based purely on lifestyle traits, ignoring location and priorities."""
    
    print(f"\n--- ALTERNATIVE MATCHING: Searching ALL residential areas (Southwest, Central, Northeast, Orchard Hill, North, Sylvan, CHCRC) ---")
    print(f"   → Ignoring location preferences and priority rankings")
    print(f"   → Focusing on core lifestyle traits: sleep, tidiness, noise, guests, social, environment")
    print(f"   → Minimum compatibility threshold: {min_threshold}%")
    
    # Normalize year format: handle both "first-year"/"upperclassman" and "first-years"/"upperclassmen"
    student_year_raw = current_profile.get('studentYear') or current_profile.get('yearPref') or current_profile.get('yearStatus') or 'upperclassmen'
    student_year_lower = str(student_year_raw).lower() if student_year_raw else 'upperclassmen'
    
    # Normalize to backend format
    if student_year_lower in ['first-year', 'first-years', 'freshman', 'freshmen']:
        student_year = 'first-years'
    elif student_year_lower in ['upperclassman', 'upperclassmen']:
        student_year = 'upperclassmen'
    else:
        student_year = 'upperclassmen'  # Default fallback
    
    # Ensure current_user_id is not None
    if not current_user_id:
        current_user_id = f"user_{abs(hash(str(current_profile))) % 10000}"
    
    all_candidates = get_all_profiles_any_dorm(current_user_id, student_year)
    
    if not all_candidates:
        print("   → No candidates found for alternative matching")
        return []
    
    # Create a modified profile that removes location and priority fields
    alternative_profile = current_profile.copy()
    # Safely remove location and priority fields (use pop with default to avoid KeyError)
    for key in ['campusProximity', 'commuteDistance', 'activityProximity', 'recommended_dorm', 
                'dormArea', 'priorityLocation', 'priorityPrivacy', 'priorityAmenities', 
                'prioritySocial', 'priorities']:
        alternative_profile.pop(key, None)
    
    match_results = []
    print(f"   → Fast scoring {len(all_candidates)} candidates for alternative matching (using fallback only)...")
    
    # Use fast fallback scoring only for alternatives (location not important, so fallback is sufficient)
    for candidate in all_candidates:
        fallback_score = calculate_fallback_score(alternative_profile, candidate)
        if fallback_score >= min_threshold:
            fallback_confidence = classify_confidence_level(fallback_score, 'Medium')
            match_results.append({
                "compatibilityScore": fallback_score,
                "confidenceLevel": fallback_confidence,
                "reasoningSummary": f"Fast alternative matching. Compatibility: {fallback_score}% based on lifestyle traits.",
                "matchAdvice": "Alternative match based on lifestyle compatibility (location preferences relaxed).",
                "candidateName": candidate.get('name', 'N/A'),
                "candidateDorm": candidate.get('dormArea', 'Unknown'),
                "breakHousingPref": candidate.get('breakHousingPref', 'no'),
                "noiseLevel": candidate.get('noiseLevel', 'quiet'),
                "genderInclusivePref": candidate.get('genderInclusivePref', 'no-preference'),
                "alcoholPref": candidate.get('alcoholPref', 'no-preference'),
                "isAlternative": True,
                "error": None
            })
    
    # Filter for minimum threshold compatibility
    high_quality_matches = [m for m in match_results if m.get('compatibilityScore', 0) >= min_threshold]
    high_quality_matches = final_logistical_filter(current_profile, high_quality_matches)
    high_quality_matches.sort(key=lambda x: x['compatibilityScore'], reverse=True)
    
    # Mark as alternative
    for match in high_quality_matches:
        match['isAlternative'] = True
    
    print(f"   → Found {len(high_quality_matches)} alternative matches ({min_threshold}%+ compatibility)")
    return high_quality_matches


def score_and_rank_matches(current_profile: Dict[str, Any], current_user_id: str) -> Dict[str, Any]:
    """
    Main orchestration function with 75% compatibility filtering and trait-based fallback.
    """
    if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n⚠️  WARNING: API Key not configured. Using default key for development.")
    
    # --- STAGE 1: High Compatibility Match (Location Priority) ---
    user_room_type = current_profile.get('roomType', '').lower()
    
    # Get minimum compatibility threshold based on room type
    min_threshold = get_min_compatibility_threshold(user_room_type)
    print(f"   → Minimum compatibility threshold: {min_threshold}% (relaxed for {user_room_type} rooms)" if user_room_type in ['triple', 'quad'] else f"   → Minimum compatibility threshold: {min_threshold}%")
    
    # Initialize allowed_areas for triple/quad room types
    allowed_areas = None
    
    # For triple/quad: Location is less important, prioritize lifestyle compatibility
    if user_room_type in ['triple', 'quad']:
        print(f"\n--- STAGE 1: Lifestyle-Focused Matching for {user_room_type.upper()} Room ---")
        print(f"   → Location is less of a priority for {user_room_type} rooms")
        print(f"   → Prioritizing lifestyle compatibility across allowed areas")
        
        # For triple/quad, only search in areas where these room types are available
        if user_room_type == 'triple':
            allowed_areas = TRIPLE_ROOM_AREAS
            print(f"   → Triples available in: {', '.join(allowed_areas)}")
        else:  # quad
            allowed_areas = QUAD_ROOM_AREAS
            print(f"   → Quads available in: {', '.join(allowed_areas)} (NOT Northeast)")
        
        # Still get a recommended area for reference, but search all allowed areas
        location_rec = get_dorm_recommendation(current_profile)
        recommended_area = location_rec['recommendedArea']
        
        # If recommended area is not in allowed areas, pick the first allowed area
        if recommended_area not in allowed_areas:
            recommended_area = allowed_areas[0]
            print(f"   → Recommended area not available for {user_room_type}, using {recommended_area} as starting point")
        
        print(f"   → Searching all {len(allowed_areas)} allowed areas for {user_room_type} room matches")
    else:
        print("\n--- STAGE 1: Prioritizing Academic Location Match ---")
        location_rec = get_dorm_recommendation(current_profile)
        recommended_area = location_rec['recommendedArea']
    
    # Filter candidates to the single ideal residential area
    # Normalize year format: handle both "first-year"/"upperclassman" and "first-years"/"upperclassmen"
    student_year_raw = current_profile.get('studentYear') or current_profile.get('yearPref') or current_profile.get('yearStatus') or 'upperclassmen'
    student_year_lower = str(student_year_raw).lower() if student_year_raw else 'upperclassmen'
    
    # Normalize to backend format
    if student_year_lower in ['first-year', 'first-years', 'freshman', 'freshmen']:
        student_year = 'first-years'
    elif student_year_lower in ['upperclassman', 'upperclassmen']:
        student_year = 'upperclassmen'
    else:
        student_year = 'upperclassmen'  # Default fallback
    
    print(f"   → User year status: {student_year_raw} → normalized to: {student_year}")
    
    # Ensure current_user_id is not None
    if not current_user_id:
        current_user_id = f"user_{abs(hash(str(current_profile))) % 10000}"
    
    # For triple/quad: Search only in allowed areas (location less important, but must be in valid areas)
    # We'll filter to same area later
    if user_room_type in ['triple', 'quad']:
        # Search only in areas where triple/quad rooms are available
        candidate_profiles = get_all_profiles_from_db(current_user_id, allowed_areas, student_year)
    else:
        # For double: search only recommended area
        candidate_profiles = get_all_profiles_from_db(current_user_id, [recommended_area], student_year)
    
    match_results = []
    
    if candidate_profiles:
        print(f"   → Scoring {len(candidate_profiles)} candidates (using fast fallback for most, API for top {MAX_CANDIDATES_TO_SCORE})...")
        
        # First, quickly score all candidates with fallback to find top candidates
        quick_scores = []
        for candidate in candidate_profiles:
            quick_score = calculate_fallback_score(current_profile, candidate)
            quick_scores.append((candidate, quick_score))
        
        # Sort by quick score and take top candidates for API scoring
        quick_scores.sort(key=lambda x: x[1], reverse=True)
        top_candidates = [c for c, s in quick_scores[:MAX_CANDIDATES_TO_SCORE] if s >= min_threshold]
        other_candidates = [c for c, s in quick_scores[MAX_CANDIDATES_TO_SCORE:] if s >= min_threshold]
        
        # Score top candidates with API (with timeout protection)
        for idx, candidate in enumerate(top_candidates, 1):
            print(f"   → API scoring candidate {idx}/{len(top_candidates)}: {candidate.get('name', 'Unknown')}")
            try:
                result = score_match(current_profile, candidate, min_threshold=min_threshold)
                match_results.append(result)
            except Exception as e:
                print(f"   ⚠️  API failed for candidate {idx}, using fallback: {e}")
                # Use fallback scoring if API fails
                fallback_score = calculate_fallback_score(current_profile, candidate)
                if fallback_score >= min_threshold:
                    fallback_confidence = classify_confidence_level(fallback_score, 'Medium')
                    match_results.append({
                        "compatibilityScore": fallback_score,
                        "confidenceLevel": fallback_confidence,
                        "reasoningSummary": f"Fast fallback scoring. Compatibility: {fallback_score}%.",
                        "matchAdvice": "Score calculated using fast fallback method.",
                        "candidateName": candidate.get('name', 'N/A'),
                        "candidateDorm": candidate.get('dormArea', 'Unknown'),
                        "breakHousingPref": candidate.get('breakHousingPref', 'no'),
                        "noiseLevel": candidate.get('noiseLevel', 'quiet'),
                        "genderInclusivePref": candidate.get('genderInclusivePref', 'no-preference'),
                        "alcoholPref": candidate.get('alcoholPref', 'no-preference'),
                        "error": str(e)
                    })
        
        # Use fast fallback for remaining candidates
        for candidate in other_candidates:
            fallback_score = calculate_fallback_score(current_profile, candidate)
            if fallback_score >= min_threshold:
                fallback_confidence = classify_confidence_level(fallback_score, 'Medium')
                match_results.append({
                    "compatibilityScore": fallback_score,
                    "confidenceLevel": fallback_confidence,
                    "reasoningSummary": f"Fast fallback scoring. Compatibility: {fallback_score}%.",
                    "matchAdvice": "Score calculated using fast fallback method.",
                    "candidateName": candidate.get('name', 'N/A'),
                    "candidateDorm": candidate.get('dormArea', 'Unknown'),
                    "breakHousingPref": candidate.get('breakHousingPref', 'no'),
                    "noiseLevel": candidate.get('noiseLevel', 'quiet'),
                    "genderInclusivePref": candidate.get('genderInclusivePref', 'no-preference'),
                    "alcoholPref": candidate.get('alcoholPref', 'no-preference'),
                    "error": None
                })

        successful_matches = [m for m in match_results if m.get('compatibilityScore', 0) >= min_threshold]
        successful_matches = final_logistical_filter(current_profile, successful_matches)
        successful_matches.sort(key=lambda x: x['compatibilityScore'], reverse=True)
    else:
        successful_matches = []

    # --- STAGE 2: Fallback to Trait Priority (Broader Search) ---
    # For triple/quad: If we don't have enough matches in the primary area, search all areas
    # but ensure all matches are in the same area
    user_room_type = current_profile.get('roomType', '').lower()
    required_count = 2 if user_room_type == 'triple' else (3 if user_room_type == 'quad' else 1)
    
    if len(successful_matches) < required_count:
        print(f"\n--- STAGE 2: EXPANDING SEARCH FOR {user_room_type.upper()} ROOM ---")
        
        if user_room_type in ['triple', 'quad']:
            print(f"   → Need {required_count} roommates in the same area. Current matches: {len(successful_matches)}")
            print(f"   → Searching ALL residential areas for lifestyle-compatible matches in the same area")
        else:
            print(f"ALERT: No one matching your personality traits (>= {min_threshold}%) and logistical requirements was found within your primary area: {recommended_area}.")
            print("Searching ALL residential areas for a high trait match, ignoring location.")
        
        alternative_matches = find_alternative_matches(current_profile, current_user_id, min_threshold)
        
        if alternative_matches:
            # For triple/quad: Group by area and pick the area with most matches
            # All roommates must be in the same exact hall
            if user_room_type in ['triple', 'quad']:
                # Determine user's exact hall from recommended area
                user_halls = RESIDENTIAL_AREA_TO_HALLS.get(recommended_area, [])
                user_exact_hall = user_halls[0] if user_halls else None
                
                # Group matches by area
                matches_by_area = {}
                for match in alternative_matches:
                    area = match.get('candidateDorm', 'Unknown')
                    if area not in matches_by_area:
                        matches_by_area[area] = []
                    matches_by_area[area].append(match)
                
                # Find area with most matches (at least required_count)
                best_area = None
                best_matches = []
                
                # Prioritize user's recommended area
                if recommended_area in matches_by_area:
                    area_matches = matches_by_area[recommended_area]
                    if len(area_matches) >= required_count:
                        best_area = recommended_area
                        best_matches = area_matches[:required_count]
                
                # If not enough in recommended area, check other areas
                if not best_matches:
                    for area, matches in matches_by_area.items():
                        if len(matches) >= required_count and len(matches) > len(best_matches):
                            best_area = area
                            best_matches = matches[:required_count]
                
                if best_matches:
                    successful_matches = best_matches
                    recommended_area = best_area
                    # Update user's exact hall to match the best area
                    if best_area != recommended_area:
                        best_halls = RESIDENTIAL_AREA_TO_HALLS.get(best_area, [])
                        user_exact_hall = best_halls[0] if best_halls else user_exact_hall
                    # Assign all matches to the same exact hall
                    if user_exact_hall:
                        for match in successful_matches:
                            match['exactHall'] = user_exact_hall
                            match['userHall'] = user_exact_hall
                    print(f"   → Found {len(best_matches)} compatible roommates in {best_area} (all in {user_exact_hall})")
                elif successful_matches:
                    # Use existing matches' area
                    existing_area = successful_matches[0].get('candidateDorm', recommended_area)
                    area_matches = [m for m in alternative_matches if m.get('candidateDorm') == existing_area]
                    successful_matches.extend(area_matches[:required_count - len(successful_matches)])
                    recommended_area = existing_area
                    # Assign all matches to the same exact hall
                    existing_halls = RESIDENTIAL_AREA_TO_HALLS.get(existing_area, [])
                    existing_exact_hall = existing_halls[0] if existing_halls else user_exact_hall
                    if existing_exact_hall:
                        for match in successful_matches:
                            match['exactHall'] = existing_exact_hall
                            match['userHall'] = existing_exact_hall
                    print(f"   → Extended matches in {existing_area} (all in {existing_exact_hall})")
                else:
                    # Take best area
                    if matches_by_area:
                        best_area = max(matches_by_area.keys(), key=lambda k: len(matches_by_area[k]))
                        successful_matches = matches_by_area[best_area][:required_count]
                        recommended_area = best_area
                        # Assign all matches to the same exact hall
                        best_halls = RESIDENTIAL_AREA_TO_HALLS.get(best_area, [])
                        best_exact_hall = best_halls[0] if best_halls else None
                        if best_exact_hall:
                            for match in successful_matches:
                                match['exactHall'] = best_exact_hall
                                match['userHall'] = best_exact_hall
                        print(f"   → Using {best_area} with {len(successful_matches)} matches (all in {best_exact_hall})")
            else:
                # For double: use alternative matches as before
                successful_matches = alternative_matches
                recommended_area = alternative_matches[0].get('candidateDorm', recommended_area)
                print(f"Found {len(alternative_matches)} alternative matches. Recommending dorm area: {recommended_area}")
        else:
            if user_room_type in ['triple', 'quad']:
                return {
                    "dorm_recommendation": recommended_area,
                    "ranked_matches": successful_matches[:required_count] if successful_matches else [],
                    "message": f"Only found {len(successful_matches)} compatible roommate(s). A {user_room_type} room requires {required_count + 1} roommates total (you + {required_count} others) in the same exact hall."
                }
            else:
                return {
                    "dorm_recommendation": recommended_area,
                    "ranked_matches": [],
                    "message": f"No highly compatible matches were found even after broadening the search across all residential areas based on personality traits. Consider changing your preference settings."
                }

    # --- Final Results Formatting (Dorm Hall Output) ---
    final_output = {
        "dorm_recommendation": recommended_area,
        "ranked_matches": [],
        "message": ""
    }
    
    # For triple/quad: All matches must be in same area, no need for primary/alternative distinction
    # For double: Separate primary matches from alternatives
    user_room_type = current_profile.get('roomType', '').lower()
    
    if user_room_type in ['triple', 'quad']:
        # For triple/quad: All roommates MUST be in the same exact hall (not just same area)
        # Determine user's exact hall from recommended area
        user_halls = RESIDENTIAL_AREA_TO_HALLS.get(recommended_area, [])
        user_exact_hall = user_halls[0] if user_halls else None
        
        if successful_matches:
            # Group matches by area first
            matches_by_area = {}
            for match in successful_matches:
                area = match.get('candidateDorm', 'Unknown')
                if area not in matches_by_area:
                    matches_by_area[area] = []
                matches_by_area[area].append(match)
            
            # Find area with most matches (at least required_count)
            required_count = 2 if user_room_type == 'triple' else 3
            best_area = None
            best_matches = []
            
            # Prioritize matches from user's recommended area
            if recommended_area in matches_by_area:
                area_matches = matches_by_area[recommended_area]
                if len(area_matches) >= required_count:
                    best_area = recommended_area
                    best_matches = area_matches[:required_count]
                    print(f"   → Found {len(best_matches)} roommates in your recommended area: {recommended_area}")
            
            # If not enough in recommended area, check other areas
            if not best_matches:
                for area, matches in matches_by_area.items():
                    if len(matches) >= required_count and len(matches) > len(best_matches):
                        best_area = area
                        best_matches = matches[:required_count]
            
            # If no area has enough, use the area with most matches
            if not best_matches and matches_by_area:
                best_area = max(matches_by_area.keys(), key=lambda k: len(matches_by_area[k]))
                best_matches = matches_by_area[best_area][:required_count]
                recommended_area = best_area
                # Update user's exact hall to match the best area
                best_halls = RESIDENTIAL_AREA_TO_HALLS.get(best_area, [])
                user_exact_hall = best_halls[0] if best_halls else user_exact_hall
                print(f"   → Using {best_area} area with {len(best_matches)} matches")
            
            # CRITICAL: All matches must be assigned to the same exact hall
            # Assign all matches to the same hall as the user
            if user_exact_hall:
                for match in best_matches:
                    match['exactHall'] = user_exact_hall
                    match['userHall'] = user_exact_hall  # Store for reference
                print(f"   → All {len(best_matches)} roommates assigned to same hall: {user_exact_hall}")
            
            all_matches = best_matches if best_matches else successful_matches[:required_count]
        else:
            all_matches = []
    else:
        # For double: Separate primary matches from alternatives
        primary_matches = [m for m in successful_matches if not m.get('isAlternative', False)]
        alternative_matches = [m for m in successful_matches if m.get('isAlternative', False)]
        
        # Ensure minimum: 1 primary + 2 alternatives
        # If we have primary matches but not enough alternatives, get alternative matches
        if len(primary_matches) > 0 and len(alternative_matches) < 2:
            print(f"\n--- Ensuring minimum alternative matches (need 2) ---")
            print(f"   → Found {len(primary_matches)} primary match(es), but only {len(alternative_matches)} alternative(s). Fast searching for more alternatives...")
            alt_matches = find_alternative_matches(current_profile, current_user_id, min_threshold)
            if alt_matches:
                # Get up to 2 alternatives that are different from primary matches
                primary_names = [p.get('candidateName') for p in primary_matches]
                existing_alt_names = [a.get('candidateName') for a in alternative_matches]
                
                for alt in alt_matches:
                    if len(alternative_matches) >= 2:
                        break
                    if (alt.get('candidateName') not in primary_names and 
                        alt.get('candidateName') not in existing_alt_names):
                        alternative_matches.append(alt)
        
        # If we have no primary matches but have alternatives, use first alternative as primary
        if len(primary_matches) == 0 and len(alternative_matches) > 0:
            primary_matches = [alternative_matches[0]]
            alternative_matches = alternative_matches[1:] if len(alternative_matches) > 1 else []
        
        # Ensure at least 1 primary match
        if len(primary_matches) == 0:
            # Try to get at least one match from alternatives
            if len(alternative_matches) > 0:
                primary_matches = [alternative_matches[0]]
                alternative_matches = alternative_matches[1:] if len(alternative_matches) > 1 else []
        
        # Ensure at least 2 alternatives if we have primary matches
        if len(primary_matches) > 0 and len(alternative_matches) < 2:
            # Get more alternative matches (fast fallback only)
            print(f"   → Fast searching for additional alternatives...")
            alt_matches = find_alternative_matches(current_profile, current_user_id, min_threshold)
            if alt_matches:
                primary_names = [p.get('candidateName') for p in primary_matches]
                existing_alt_names = [a.get('candidateName') for a in alternative_matches]
                
                for alt in alt_matches:
                    if len(alternative_matches) >= 2:
                        break
                    if (alt.get('candidateName') not in primary_names and 
                        alt.get('candidateName') not in existing_alt_names):
                        alternative_matches.append(alt)
        
        # Combine: primary first, then alternatives
        all_matches = primary_matches + alternative_matches
    
    # Determine how many matches to return based on room type
    # For triple/quad: matches are already filtered to same area above
    # For double: return exactly 1 primary + 2 alternatives (3 total)
    if user_room_type == 'triple':
        required_matches = 2
        matches_to_return = all_matches[:required_matches]
        if len(matches_to_return) < required_matches:
            final_output["message"] = f"Note: Only {len(matches_to_return)} compatible roommate(s) found. A triple room requires 3 roommates total (you + 2 others) in the same exact hall."
    elif user_room_type == 'quad':
        required_matches = 3
        matches_to_return = all_matches[:required_matches]
        if len(matches_to_return) < required_matches:
            final_output["message"] = f"Note: Only {len(matches_to_return)} compatible roommate(s) found. A quad room requires 4 roommates total (you + 3 others) in the same exact hall."
    else:
        # For double, return exactly 1 primary + 2 alternatives (3 total)
        matches_to_return = all_matches[:3]  # 1 primary + 2 alternatives
    
    # Check if any matches are alternatives
    has_alternatives = any(match.get('isAlternative', False) for match in matches_to_return)
    if has_alternatives:
        final_output["is_alternative"] = True
    
    for match in matches_to_return:
        area = match.get('candidateDorm', 'Unknown')
        
        # For triple/quad: Use the exact hall already assigned (all roommates in same hall)
        # For double: Get the most proximate hall for the specific area
        if user_room_type in ['triple', 'quad']:
            # Use the exact hall that was assigned during grouping (all matches share same hall)
            most_proximate_hall = match.get('exactHall', match.get('userHall'))
            if not most_proximate_hall:
                # Fallback: get first hall from area
                halls = RESIDENTIAL_AREA_TO_HALLS.get(area, [])
                most_proximate_hall = halls[0] if halls else "Hall data unavailable."
        else:
            # For double: Get the most proximate hall for the specific area
            halls = RESIDENTIAL_AREA_TO_HALLS.get(area, [])
            most_proximate_hall = halls[0] if halls else "Hall data unavailable."
        
        hall_info = f"Best Match Hall: **{most_proximate_hall}**" 

        final_output["ranked_matches"].append({
            "compatibilityScore": match.get('compatibilityScore', 0),
            "confidenceLevel": match.get('confidenceLevel', 'Medium'),
            "reasoningSummary": match.get('reasoningSummary', 'No reasoning provided.'),
            "candidateName": match.get('candidateName', 'N/A'),
            "candidateDorm": area,  # Add candidateDorm for frontend compatibility
            "recommendedDorms": hall_info,
            "exactHall": most_proximate_hall,  # Add exact hall name (same for all triple/quad matches)
            "matchAdvice": match.get('matchAdvice', 'No advice available'),
            "isAlternative": match.get('isAlternative', False),
            "userId": match.get('userId', 'unknown')
        })

    return final_output
