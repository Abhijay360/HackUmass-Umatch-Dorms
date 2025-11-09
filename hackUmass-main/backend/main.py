from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import sys
import os

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass

# Import the backend functions from the same directory
import importlib.util
backend_file = os.path.join(os.path.dirname(__file__), 'HackUmass_back_end.py')
spec = importlib.util.spec_from_file_location("hackumass_backend", backend_file)
hackumass_backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hackumass_backend)
score_and_rank_matches = hackumass_backend.score_and_rank_matches

app = FastAPI(title="UMass Housing Recommender API")

# Configure CORS to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "*",  # Allow all origins for local HTML files (development only)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class UserProfile(BaseModel):
    userId: Optional[str] = None
    name: Optional[str] = None
    major: Optional[str] = "General"
    # Step 1: Basic Information
    yearStatus: Optional[str] = None  # 'first-year' or 'upperclassman'
    roomType: str
    genderType: str
    accessible: Optional[str] = None
    isHonors: Optional[str] = None  # 'yes' or 'no'
    breakHousing: Optional[str] = None  # 'yes', 'preferred', or 'no'
    # Step 2: Social & Lifestyle
    socialLevelType: Optional[str] = None
    socialLevel: Optional[str] = None
    noiseLevelType: Optional[str] = None
    noiseLevel: Optional[str] = None
    activitiesImportance: Optional[str] = None
    environmentPref: Optional[str] = None
    yearMix: Optional[str] = None
    yearPref: Optional[str] = None
    sleepSchedule: Optional[str] = None
    tidinessLevel: Optional[str] = None
    tidiness: Optional[str] = None
    lifestyleMatch: Optional[str] = None
    guestFrequencyType: Optional[str] = None
    guestFrequency: Optional[str] = None
    # Step 3: Amenities & Facilities
    kitchenImportanceType: Optional[str] = None
    kitchenImportance: Optional[str] = None
    campusProximity: Optional[str] = None
    activityProximity: Optional[str] = None
    spaceType: Optional[str] = None
    commuteDistanceType: Optional[str] = None
    commuteDistance: Optional[str] = None
    outdoorSpaceType: Optional[str] = None
    outdoorSpace: Optional[str] = None
    # Step 4: Community & Interests
    communityType: str
    sharedInterestsType: Optional[str] = None
    # Step 5: Special Needs
    sensitivitiesType: Optional[str] = None
    # Step 6: Priority Rankings
    priorities: Optional[Dict[str, int]] = None
    priorityLocation: Optional[str] = None
    priorityPrivacy: Optional[str] = None
    priorityAmenities: Optional[str] = None
    prioritySocial: Optional[str] = None

class MatchResponse(BaseModel):
    dorm_recommendation: str
    ranked_matches: List[Dict[str, Any]]
    message: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
def root():
    return {"message": "UMass Housing Recommender API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/match", response_model=MatchResponse)
async def get_matches(profile: UserProfile):
    """
    Main endpoint to get dorm recommendations and roommate matches.
    Takes a user profile and returns ranked matches.
    """
    try:
        # Convert Pydantic model to dict and normalize field names
        profile_dict = profile.dict(exclude_none=True)
        
        # Normalize field names to match Python backend expectations
        normalized_profile = {}
        for key, value in profile_dict.items():
            # Map frontend field names to backend field names
            if key == "yearStatus":
                # Map yearStatus to studentYear (new backend field name)
                normalized_profile["yearStatus"] = value
                if value == "first-year":
                    normalized_profile["studentYear"] = "first-years"
                    normalized_profile["yearPref"] = "first-years"  # Keep for compatibility
                elif value == "upperclassman":
                    normalized_profile["studentYear"] = "upperclassmen"
                    normalized_profile["yearPref"] = "upperclassmen"  # Keep for compatibility
                else:
                    normalized_profile["studentYear"] = value
                    normalized_profile["yearPref"] = value
            elif key == "socialLevelType":
                normalized_profile["socialLevel"] = value
            elif key == "noiseLevelType":
                normalized_profile["noiseLevel"] = value
            elif key == "yearMix":
                normalized_profile["yearPref"] = value
            elif key == "tidinessLevel":
                normalized_profile["tidiness"] = value
            elif key == "guestFrequencyType":
                normalized_profile["guestFrequency"] = value
            elif key == "kitchenImportanceType":
                normalized_profile["kitchenImportance"] = value
            elif key == "commuteDistanceType":
                normalized_profile["commuteDistance"] = value
            elif key == "outdoorSpaceType":
                normalized_profile["outdoorSpace"] = value
            elif key == "sharedInterestsType":
                normalized_profile["sharedInterests"] = value
            elif key == "sensitivitiesType":
                normalized_profile["sensitivities"] = value
            elif key == "priorities":
                # Handle priorities object - also extract individual fields for compatibility
                if isinstance(value, dict):
                    normalized_profile["priorities"] = value
                    # Also set individual priority fields for backward compatibility
                    normalized_profile["priorityLocation"] = str(value.get("location", "4"))
                    normalized_profile["priorityPrivacy"] = str(value.get("privacy", "4"))
                    normalized_profile["priorityAmenities"] = str(value.get("amenities", "4"))
                    normalized_profile["prioritySocial"] = str(value.get("social", "4"))
                else:
                    normalized_profile["priorities"] = value
            elif key in ["priorityLocation", "priorityPrivacy", "priorityAmenities", "prioritySocial"]:
                # Pass through individual priority fields
                normalized_profile[key] = str(value) if value else "4"
            elif key == "genderType":
                # Map user's gender to dorm preference
                # Store user's actual gender for matching
                normalized_profile["userGender"] = value
                # Map to dorm preference: male/female can match same-gender or co-ed, non-binary/prefer-not-to-say prefer co-ed
                if value in ["male", "female"]:
                    # Default to co-ed but can match same-gender dorms
                    normalized_profile["genderPref"] = "coed"
                elif value in ["non-binary", "prefer-not-to-say"]:
                    normalized_profile["genderPref"] = "coed"
                else:
                    normalized_profile["genderPref"] = "coed"  # Default fallback
            elif key == "breakHousing":
                # Map breakHousing to breakHousingPref (new backend field name)
                normalized_profile["breakHousingPref"] = value
            elif key == "major":
                # Pass through major for dorm recommendation (used for academic zone mapping)
                normalized_profile["major"] = value
                # Also set college field if not already set (backend will map from major)
                if "college" not in normalized_profile:
                    normalized_profile["college"] = "General/Other"  # Backend will map from major
            elif key == "isHonors":
                # Pass through isHonors for dorm recommendation
                normalized_profile["isHonors"] = value
            elif key == "accessible":
                # Handle accessible field - convert string/boolean to expected format
                if isinstance(value, bool):
                    normalized_profile["accessible"] = "yes" if value else "no"
                elif isinstance(value, str):
                    if value.lower() in ["yes", "true", "1", "required"]:
                        normalized_profile["accessible"] = "yes"
                    elif value.lower() in ["preferred"]:
                        normalized_profile["accessible"] = "preferred"
                    else:
                        normalized_profile["accessible"] = "no"
                else:
                    normalized_profile["accessible"] = "no"
            elif key in ["budgetRange", "budget", "housingType", "locationType", "laundry", "bathroom", 
                         "climateControl", "medicalRequirements", "dietaryReligious", "themeDorm", "priorityPrice"]:
                # Skip removed or unused fields
                continue
            else:
                normalized_profile[key] = value
        
        # Ensure required fields have defaults
        if "userId" not in normalized_profile or not normalized_profile["userId"]:
            normalized_profile["userId"] = f"user_{abs(hash(str(normalized_profile))) % 10000}"
        
        if "name" not in normalized_profile or not normalized_profile["name"]:
            normalized_profile["name"] = "Current User"
        
        if "major" not in normalized_profile or not normalized_profile["major"]:
            normalized_profile["major"] = "General"
        
        # Call the Python backend function
        try:
            result = score_and_rank_matches(
                normalized_profile,
                normalized_profile.get("userId", f"user_{abs(hash(str(normalized_profile))) % 10000}")
            )
            
            # Ensure result has required fields
            if not isinstance(result, dict):
                raise ValueError("Backend returned invalid result format")
            
            # Ensure ranked_matches is a list
            if 'ranked_matches' not in result:
                result['ranked_matches'] = []
            elif not isinstance(result['ranked_matches'], list):
                result['ranked_matches'] = []
            
            # Ensure dorm_recommendation exists
            if 'dorm_recommendation' not in result:
                result['dorm_recommendation'] = 'Unknown'
            
            return MatchResponse(**result)
        except Exception as backend_error:
            print(f"Backend error in score_and_rank_matches: {str(backend_error)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Backend processing error: {str(backend_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in /api/match: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("\n" + "="*50)
    print("🚀 Starting UMass Housing Recommender Backend")
    print("="*50)
    print(f"📡 Server running on: http://{host}:{port}")
    print(f"📝 API Documentation: http://{host}:{port}/docs")
    print(f"🔑 Using Gemini API: {'✅ Configured' if os.getenv('GEMINI_API_KEY') or hackumass_backend.API_KEY != 'YOUR_GEMINI_API_KEY_HERE' else '⚠️  Using default key'}")
    print("="*50 + "\n")
    uvicorn.run(app, host=host, port=port)

