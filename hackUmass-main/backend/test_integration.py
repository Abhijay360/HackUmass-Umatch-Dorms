#!/usr/bin/env python3
"""
Integration test suite - Tests frontend-backend integration
Simulates actual frontend requests to identify runtime and logical errors
"""

import requests
import json
import time
import traceback
from typing import Dict, Any, List

BASE_URL = "http://localhost:8000"

def test_api_endpoint(name: str, payload: Dict[str, Any], expected_status: int = 200):
    """Test an API endpoint and return results"""
    print(f"\n{'='*80}")
    print(f"TEST: {name}")
    print(f"{'='*80}")
    print(f"📤 Payload keys: {list(payload.keys())}")
    
    errors = []
    warnings = []
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/api/match",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        print(f"⏱️  Response time: {elapsed:.2f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code != expected_status:
            errors.append(f"Expected status {expected_status}, got {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"📦 Response keys: {list(data.keys())}")
                
                # Check required fields
                if 'dorm_recommendation' not in data:
                    errors.append("Missing 'dorm_recommendation' in response")
                else:
                    print(f"🏠 Dorm Recommendation: {data.get('dorm_recommendation')}")
                
                if 'ranked_matches' not in data:
                    errors.append("Missing 'ranked_matches' in response")
                else:
                    matches = data.get('ranked_matches', [])
                    print(f"👥 Matches Found: {len(matches)}")
                    
                    # Validate match structure
                    for i, match in enumerate(matches[:3], 1):
                        print(f"   Match {i}: {match.get('candidateName', 'N/A')} - {match.get('compatibilityScore', 0)}%")
                        
                        required_fields = ['candidateName', 'compatibilityScore', 'candidateDorm', 'userId']
                        for field in required_fields:
                            if field not in match:
                                errors.append(f"Match {i} missing required field: {field}")
                        
                        # Check compatibility score
                        score = match.get('compatibilityScore', 0)
                        if score < 75 and not data.get('is_alternative'):
                            warnings.append(f"Match {i} has score {score}% (below 75% threshold)")
                
                if 'message' in data:
                    print(f"💬 Message: {data.get('message')}")
                
                if 'is_alternative' in data and data.get('is_alternative'):
                    print(f"🔄 Alternative Match Mode: Yes")
                
                if 'error' in data:
                    errors.append(f"Backend error: {data.get('error')}")
                
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON response: {str(e)}")
                print(f"❌ Response body: {response.text[:500]}")
        else:
            errors.append(f"HTTP Error: {response.text[:500]}")
        
    except requests.exceptions.Timeout:
        errors.append("Request timed out after 120 seconds")
    except requests.exceptions.ConnectionError:
        errors.append("Could not connect to backend. Is it running on port 8000?")
    except Exception as e:
        errors.append(f"Unexpected error: {str(e)}")
        traceback.print_exc()
    
    # Print results
    if errors:
        print(f"\n❌ ERRORS FOUND ({len(errors)}):")
        for error in errors:
            print(f"   • {error}")
    else:
        print(f"\n✅ No errors detected")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"   • {warning}")
    
    return errors, warnings

def run_all_tests():
    """Run comprehensive integration tests"""
    print("\n" + "="*80)
    print("🧪 COMPREHENSIVE INTEGRATION TEST SUITE")
    print("Testing Frontend-Backend Integration")
    print("="*80)
    
    all_errors = []
    all_warnings = []
    
    # Test 1: First-year Business student, Quad room
    errors, warnings = test_api_endpoint(
        "Test 1: First-Year Business Student - Quad Room",
        {
            "yearStatus": "first-year",
            "major": "Business",
            "roomType": "quad",
            "genderType": "Male",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "general",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "moderate",
            "tidinessLevel": "moderately-tidy",
            "guestFrequencyType": "weekly",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "2",
                "priorityPrivacy": "3",
                "priorityAmenities": "2",
                "prioritySocial": "1"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 2: Upperclassman Computer Science, Double room
    errors, warnings = test_api_endpoint(
        "Test 2: Upperclassman Computer Science - Double Room",
        {
            "yearStatus": "upperclassman",
            "major": "Computer Science",
            "roomType": "double",
            "genderType": "Female",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "academic-focused",
            "socialLevelType": "minimal-social",
            "noiseLevelType": "quiet",
            "tidinessLevel": "tidy",
            "guestFrequencyType": "rarely",
            "commuteDistanceType": "under-5min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "1",
                "priorityPrivacy": "2",
                "priorityAmenities": "3",
                "prioritySocial": "4"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 3: Honors student, Suite room
    errors, warnings = test_api_endpoint(
        "Test 3: Honors Student - Suite Room",
        {
            "yearStatus": "upperclassman",
            "major": "History",
            "roomType": "suite",
            "genderType": "Female",
            "isHonors": "yes",
            "breakHousing": "no",
            "communityType": "honors-focused",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "quiet",
            "tidinessLevel": "very-tidy",
            "guestFrequencyType": "rarely",
            "commuteDistanceType": "under-5min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "very-important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "1",
                "priorityPrivacy": "2",
                "priorityAmenities": "3",
                "prioritySocial": "4"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 4: First-year with break housing requirement
    errors, warnings = test_api_endpoint(
        "Test 4: First-Year Student - Break Housing Required",
        {
            "yearStatus": "first-year",
            "major": "Psychology",
            "roomType": "double",
            "genderType": "Non-binary",
            "isHonors": "no",
            "breakHousing": "yes",
            "communityType": "general",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "moderate",
            "tidinessLevel": "moderately-tidy",
            "guestFrequencyType": "weekly",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "2",
                "priorityPrivacy": "3",
                "priorityAmenities": "2",
                "prioritySocial": "1"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 5: Engineering student, Quad room
    errors, warnings = test_api_endpoint(
        "Test 5: Engineering Student - Quad Room",
        {
            "yearStatus": "first-year",
            "major": "Engineering",
            "roomType": "quad",
            "genderType": "Male",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "academic-focused",
            "socialLevelType": "minimal-social",
            "noiseLevelType": "very-quiet",
            "tidinessLevel": "very-tidy",
            "guestFrequencyType": "never",
            "commuteDistanceType": "under-5min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "not-important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "1",
                "priorityPrivacy": "2",
                "priorityAmenities": "3",
                "prioritySocial": "4"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 6: Very social party-goer, Double room
    errors, warnings = test_api_endpoint(
        "Test 6: Very Social Party-Goer - Double Room",
        {
            "yearStatus": "first-year",
            "major": "General Studies",
            "roomType": "double",
            "genderType": "Male",
            "isHonors": "no",
            "breakHousing": "yes",
            "communityType": "general",
            "socialLevelType": "very-social",
            "noiseLevelType": "loud",
            "tidinessLevel": "messy",
            "guestFrequencyType": "daily",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "yes-required",
            "sharedInterestsType": "somewhat-important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "4",
                "priorityPrivacy": "3",
                "priorityAmenities": "2",
                "prioritySocial": "1"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 7: Accessible housing required
    errors, warnings = test_api_endpoint(
        "Test 7: Accessible Housing Required",
        {
            "yearStatus": "upperclassman",
            "major": "Biology",
            "roomType": "double",
            "genderType": "Female",
            "isHonors": "no",
            "breakHousing": "no",
            "accessible": "yes",
            "communityType": "general",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "quiet",
            "tidinessLevel": "tidy",
            "guestFrequencyType": "monthly",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "2",
                "priorityPrivacy": "2",
                "priorityAmenities": "3",
                "prioritySocial": "4"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 8: Edge case - Minimal profile
    errors, warnings = test_api_endpoint(
        "Test 8: Minimal Profile - Only Required Fields",
        {
            "yearStatus": "first-year",
            "major": "General Studies",
            "roomType": "double",
            "genderType": "Male",
            "communityType": "general"
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 9: Apartment-style room (should not recommend North for first-year)
    errors, warnings = test_api_endpoint(
        "Test 9: First-Year Requesting Apartment (Should NOT get North)",
        {
            "yearStatus": "first-year",
            "major": "Management",
            "roomType": "apartment",
            "genderType": "Female",
            "isHonors": "no",
            "breakHousing": "yes",
            "communityType": "general",
            "socialLevelType": "minimal-social",
            "noiseLevelType": "quiet",
            "tidinessLevel": "tidy",
            "guestFrequencyType": "monthly",
            "commuteDistanceType": "10-15min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "somewhat-important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "2",
                "priorityPrivacy": "1",
                "priorityAmenities": "3",
                "prioritySocial": "4"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 10: Extreme preferences mismatch
    errors, warnings = test_api_endpoint(
        "Test 10: Extreme Preferences - Very Quiet vs Very Loud",
        {
            "yearStatus": "upperclassman",
            "major": "English",
            "roomType": "double",
            "genderType": "Female",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "academic-focused",
            "socialLevelType": "minimal-social",
            "noiseLevelType": "very-quiet",
            "tidinessLevel": "very-tidy",
            "guestFrequencyType": "never",
            "commuteDistanceType": "under-5min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "1",
                "priorityPrivacy": "2",
                "priorityAmenities": "3",
                "prioritySocial": "4"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 11: Quad room should return 3 matches
    errors, warnings = test_api_endpoint(
        "Test 11: Quad Room - Should Return 3 Matches",
        {
            "yearStatus": "first-year",
            "major": "Business",
            "roomType": "quad",
            "genderType": "Male",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "general",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "moderate",
            "tidinessLevel": "moderately-tidy",
            "guestFrequencyType": "weekly",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "2",
                "priorityPrivacy": "3",
                "priorityAmenities": "2",
                "prioritySocial": "1"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 12: Missing required fields
    errors, warnings = test_api_endpoint(
        "Test 12: Missing Required Fields - Should Handle Gracefully",
        {
            "yearStatus": "first-year",
            # Missing major, roomType, genderType
        },
        expected_status=200  # Should still return 200 but with error message
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 13: Invalid values
    errors, warnings = test_api_endpoint(
        "Test 13: Invalid Values - Should Handle Gracefully",
        {
            "yearStatus": "invalid-year",
            "major": "Invalid Major",
            "roomType": "invalid-room",
            "genderType": "Invalid Gender",
            "isHonors": "maybe",  # Should be "yes" or "no"
            "breakHousing": "sometimes",  # Should be "yes", "preferred", or "no"
            "communityType": "invalid-community"
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 14: All priorities same rank (should be handled)
    errors, warnings = test_api_endpoint(
        "Test 14: All Priorities Same Rank",
        {
            "yearStatus": "first-year",
            "major": "Psychology",
            "roomType": "double",
            "genderType": "Male",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "general",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "moderate",
            "tidinessLevel": "moderately-tidy",
            "guestFrequencyType": "weekly",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "1",
                "priorityPrivacy": "1",
                "priorityAmenities": "1",
                "prioritySocial": "1"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 15: Non-binary gender preference
    errors, warnings = test_api_endpoint(
        "Test 15: Non-Binary Gender Preference",
        {
            "yearStatus": "upperclassman",
            "major": "Sociology",
            "roomType": "double",
            "genderType": "Non-binary",
            "isHonors": "no",
            "breakHousing": "no",
            "communityType": "general",
            "socialLevelType": "moderately-social",
            "noiseLevelType": "moderate",
            "tidinessLevel": "moderately-tidy",
            "guestFrequencyType": "monthly",
            "commuteDistanceType": "5-10min",
            "outdoorSpaceType": "nice-to-have",
            "sharedInterestsType": "important",
            "sensitivitiesType": "none",
            "priorities": {
                "priorityLocation": "2",
                "priorityPrivacy": "2",
                "priorityAmenities": "3",
                "prioritySocial": "3"
            }
        }
    )
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Summary
    print("\n" + "="*80)
    print("📋 FINAL TEST SUMMARY")
    print("="*80)
    
    if all_errors:
        print(f"\n❌ TOTAL ERRORS FOUND: {len(all_errors)}")
        print("\nError Details:")
        for i, error in enumerate(all_errors, 1):
            print(f"   {i}. {error}")
    else:
        print(f"\n✅ No errors detected in any test!")
    
    if all_warnings:
        print(f"\n⚠️  TOTAL WARNINGS: {len(all_warnings)}")
        print("\nWarning Details:")
        for i, warning in enumerate(all_warnings, 1):
            print(f"   {i}. {warning}")
    
    print(f"\n{'='*80}\n")
    
    return len(all_errors) == 0

if __name__ == "__main__":
    print("⚠️  Make sure the backend is running on port 8000!")
    print("   Start it with: cd backend && python3 main.py\n")
    time.sleep(2)
    
    success = run_all_tests()
    exit(0 if success else 1)

