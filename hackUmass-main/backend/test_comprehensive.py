#!/usr/bin/env python3
"""
Comprehensive test suite for backend matching system
Tests multiple scenarios with different parameters to identify runtime errors
"""

import sys
import os
import traceback
import time

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from HackUmass_back_end import (
    score_and_rank_matches,
    get_dorm_recommendation,
    get_all_profiles_from_db,
    score_match
)

def test_scenario(name, profile, expected_dorm=None, min_matches=0):
    """Test a single scenario and return results"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    
    try:
        start_time = time.time()
        result = score_and_rank_matches(profile, profile.get('userId', 'test_user'))
        elapsed = time.time() - start_time
        
        print(f"⏱️  Execution time: {elapsed:.2f} seconds")
        print(f"📊 Dorm Recommendation: {result.get('dorm_recommendation', 'N/A')}")
        print(f"📊 Matches Found: {len(result.get('ranked_matches', []))}")
        
        if result.get('ranked_matches'):
            print(f"\n   Top Matches:")
            for i, match in enumerate(result.get('ranked_matches', [])[:3], 1):
                print(f"   {i}. {match.get('candidateName', 'N/A')} - {match.get('compatibilityScore', 0)}%")
        
        if result.get('message'):
            print(f"   ℹ️  Message: {result.get('message')}")
        
        if result.get('error'):
            print(f"   ❌ Error: {result.get('error')}")
            return False
        
        # Validation
        matches = result.get('ranked_matches', [])
        if len(matches) < min_matches:
            print(f"   ⚠️  Warning: Expected at least {min_matches} matches, got {len(matches)}")
        
        if expected_dorm and result.get('dorm_recommendation') != expected_dorm:
            print(f"   ⚠️  Warning: Expected dorm '{expected_dorm}', got '{result.get('dorm_recommendation')}'")
        
        print(f"   ✅ PASS")
        return True
        
    except Exception as e:
        print(f"   ❌ RUNTIME ERROR: {str(e)}")
        print(f"   📋 Traceback:")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run comprehensive test suite"""
    print("\n" + "="*70)
    print("🧪 COMPREHENSIVE BACKEND TEST SUITE")
    print("="*70)
    
    results = []
    
    # Test 1: First-year Business student, Quad room
    results.append(("First-Year Business Quad", test_scenario(
        "First-Year Business Student - Quad Room",
        {
            "userId": "test_1",
            "name": "Test User 1",
            "major": "Business",
            "yearStatus": "first-year",
            "studentYear": "first-years",
            "roomType": "quad",
            "genderType": "male",
            "genderPref": "coed",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "no",
            "socialLevel": "moderately-social",
            "noiseLevel": "moderate",
            "activitiesImportance": "somewhat-important",
            "environmentPref": "balanced",
            "yearPref": "first-years",
            "sleepSchedule": "balanced",
            "tidiness": "moderately-tidy",
            "lifestyleMatch": "important",
            "guestFrequency": "weekly",
            "campusProximity": "important",
            "activityProximity": "balanced",
            "spaceType": "green-spaces",
            "commuteDistance": "5-10min",
            "outdoorSpace": "nice-to-have",
            "communityType": "general",
            "sharedInterests": "important",
            "sensitivities": "none",
            "priorityLocation": "2",
            "priorityPrivacy": "3",
            "priorityAmenities": "2",
            "prioritySocial": "1"
        },
        expected_dorm="Southwest",
        min_matches=3
    )))
    
    # Test 2: Upperclassman Computer Science, Double room
    results.append(("Upperclassman CS Double", test_scenario(
        "Upperclassman Computer Science - Double Room",
        {
            "userId": "test_2",
            "name": "Test User 2",
            "major": "Computer Science",
            "yearStatus": "upperclassman",
            "studentYear": "upperclassmen",
            "roomType": "double",
            "genderType": "female",
            "genderPref": "coed",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "no",
            "socialLevel": "minimal-social",
            "noiseLevel": "quiet",
            "activitiesImportance": "not-important",
            "environmentPref": "quiet-academic",
            "yearPref": "upperclassmen",
            "sleepSchedule": "early-bird",
            "tidiness": "tidy",
            "lifestyleMatch": "very-important",
            "guestFrequency": "rarely",
            "campusProximity": "essential",
            "activityProximity": "quiet-area",
            "spaceType": "green-spaces",
            "commuteDistance": "under-5min",
            "outdoorSpace": "nice-to-have",
            "communityType": "academic-focused",
            "sharedInterests": "important",
            "sensitivities": "none",
            "priorityLocation": "1",
            "priorityPrivacy": "2",
            "priorityAmenities": "3",
            "prioritySocial": "4"
        },
        expected_dorm="Northeast",
        min_matches=1
    )))
    
    # Test 3: Honors student, Suite room
    results.append(("Honors Student Suite", test_scenario(
        "Honors Student - Suite Room",
        {
            "userId": "test_3",
            "name": "Test User 3",
            "major": "History",
            "yearStatus": "upperclassman",
            "studentYear": "upperclassmen",
            "roomType": "suite",
            "genderType": "female",
            "genderPref": "coed",
            "accessible": "no",
            "isHonors": "yes",
            "breakHousing": "no",
            "socialLevel": "moderately-social",
            "noiseLevel": "quiet",
            "activitiesImportance": "somewhat-important",
            "environmentPref": "balanced",
            "yearPref": "upperclassmen",
            "sleepSchedule": "early-bird",
            "tidiness": "very-tidy",
            "lifestyleMatch": "very-important",
            "guestFrequency": "rarely",
            "campusProximity": "essential",
            "activityProximity": "quiet-area",
            "spaceType": "green-spaces",
            "commuteDistance": "under-5min",
            "outdoorSpace": "nice-to-have",
            "communityType": "honors-focused",
            "sharedInterests": "very-important",
            "sensitivities": "none",
            "priorityLocation": "1",
            "priorityPrivacy": "2",
            "priorityAmenities": "3",
            "prioritySocial": "4"
        },
        expected_dorm="CHCRC",
        min_matches=1
    )))
    
    # Test 4: First-year with break housing requirement
    results.append(("First-Year Break Housing", test_scenario(
        "First-Year Student - Break Housing Required",
        {
            "userId": "test_4",
            "name": "Test User 4",
            "major": "Psychology",
            "yearStatus": "first-year",
            "studentYear": "first-years",
            "roomType": "double",
            "genderType": "non-binary",
            "genderPref": "coed",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "yes",
            "socialLevel": "moderately-social",
            "noiseLevel": "moderate",
            "activitiesImportance": "somewhat-important",
            "environmentPref": "balanced",
            "yearPref": "first-years",
            "sleepSchedule": "balanced",
            "tidiness": "moderately-tidy",
            "lifestyleMatch": "important",
            "guestFrequency": "weekly",
            "campusProximity": "important",
            "activityProximity": "balanced",
            "spaceType": "green-spaces",
            "commuteDistance": "5-10min",
            "outdoorSpace": "nice-to-have",
            "communityType": "general",
            "sharedInterests": "important",
            "sensitivities": "none",
            "priorityLocation": "2",
            "priorityPrivacy": "3",
            "priorityAmenities": "2",
            "prioritySocial": "1"
        },
        min_matches=1
    )))
    
    # Test 5: Engineering student, Quad room
    results.append(("Engineering Quad", test_scenario(
        "Engineering Student - Quad Room",
        {
            "userId": "test_5",
            "name": "Test User 5",
            "major": "Engineering",
            "yearStatus": "first-year",
            "studentYear": "first-years",
            "roomType": "quad",
            "genderType": "male",
            "genderPref": "all-male",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "no",
            "socialLevel": "minimal-social",
            "noiseLevel": "very-quiet",
            "activitiesImportance": "not-important",
            "environmentPref": "quiet-academic",
            "yearPref": "first-years",
            "sleepSchedule": "early-bird",
            "tidiness": "very-tidy",
            "lifestyleMatch": "very-important",
            "guestFrequency": "never",
            "campusProximity": "essential",
            "activityProximity": "quiet-area",
            "spaceType": "green-spaces",
            "commuteDistance": "under-5min",
            "outdoorSpace": "nice-to-have",
            "communityType": "academic-focused",
            "sharedInterests": "not-important",
            "sensitivities": "none",
            "priorityLocation": "1",
            "priorityPrivacy": "2",
            "priorityAmenities": "3",
            "prioritySocial": "4"
        },
        expected_dorm="Northeast",
        min_matches=3
    )))
    
    # Test 6: Very social party-goer, Double room
    results.append(("Social Party-Goer", test_scenario(
        "Very Social Party-Goer - Double Room",
        {
            "userId": "test_6",
            "name": "Test User 6",
            "major": "General Studies",
            "yearStatus": "first-year",
            "studentYear": "first-years",
            "roomType": "double",
            "genderType": "male",
            "genderPref": "coed",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "required",
            "socialLevel": "very-social",
            "noiseLevel": "loud",
            "activitiesImportance": "very-important",
            "environmentPref": "party-friendly",
            "yearPref": "first-years",
            "sleepSchedule": "night-owl",
            "tidiness": "messy",
            "lifestyleMatch": "not-important",
            "guestFrequency": "daily",
            "campusProximity": "important",
            "activityProximity": "near-activity",
            "spaceType": "urban",
            "commuteDistance": "5-10min",
            "outdoorSpace": "yes-required",
            "communityType": "social-focused",
            "sharedInterests": "somewhat-important",
            "sensitivities": "none",
            "priorityLocation": "4",
            "priorityPrivacy": "3",
            "priorityAmenities": "2",
            "prioritySocial": "1"
        },
        expected_dorm="Southwest",
        min_matches=1
    )))
    
    # Test 7: Accessible housing required
    results.append(("Accessible Housing", test_scenario(
        "Accessible Housing Required",
        {
            "userId": "test_7",
            "name": "Test User 7",
            "major": "Biology",
            "yearStatus": "upperclassman",
            "studentYear": "upperclassmen",
            "roomType": "double",
            "genderType": "female",
            "genderPref": "coed",
            "accessible": "yes",
            "isHonors": "no",
            "breakHousing": "no",
            "socialLevel": "moderately-social",
            "noiseLevel": "quiet",
            "activitiesImportance": "somewhat-important",
            "environmentPref": "balanced",
            "yearPref": "upperclassmen",
            "sleepSchedule": "balanced",
            "tidiness": "tidy",
            "lifestyleMatch": "important",
            "guestFrequency": "monthly",
            "campusProximity": "very-important",
            "activityProximity": "balanced",
            "spaceType": "green-spaces",
            "commuteDistance": "5-10min",
            "outdoorSpace": "nice-to-have",
            "communityType": "general",
            "sharedInterests": "important",
            "sensitivities": "none",
            "priorityLocation": "2",
            "priorityPrivacy": "2",
            "priorityAmenities": "3",
            "prioritySocial": "4"
        },
        min_matches=0
    )))
    
    # Test 8: Edge case - Missing fields
    results.append(("Minimal Profile", test_scenario(
        "Minimal Profile - Only Required Fields",
        {
            "userId": "test_8",
            "name": "Test User 8",
            "major": "General",
            "yearStatus": "first-year",
            "roomType": "double",
            "genderType": "male",
            "communityType": "general"
        },
        min_matches=0
    )))
    
    # Test 9: Apartment-style room
    results.append(("Apartment Style", test_scenario(
        "Upperclassman - Apartment Style",
        {
            "userId": "test_9",
            "name": "Test User 9",
            "major": "Management",
            "yearStatus": "upperclassman",
            "studentYear": "upperclassmen",
            "roomType": "apartment",
            "genderType": "female",
            "genderPref": "all-female",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "required",
            "socialLevel": "minimal-social",
            "noiseLevel": "quiet",
            "activitiesImportance": "somewhat-important",
            "environmentPref": "independent-living",
            "yearPref": "upperclassmen",
            "sleepSchedule": "balanced",
            "tidiness": "tidy",
            "lifestyleMatch": "important",
            "guestFrequency": "monthly",
            "campusProximity": "very-important",
            "activityProximity": "balanced",
            "spaceType": "urban",
            "commuteDistance": "10-15min",
            "outdoorSpace": "nice-to-have",
            "communityType": "general",
            "sharedInterests": "somewhat-important",
            "sensitivities": "none",
            "priorityLocation": "2",
            "priorityPrivacy": "1",
            "priorityAmenities": "3",
            "prioritySocial": "4"
        },
        expected_dorm="North",
        min_matches=1
    )))
    
    # Test 10: Extreme preferences mismatch
    results.append(("Extreme Mismatch", test_scenario(
        "Extreme Preferences - Very Quiet vs Very Loud",
        {
            "userId": "test_10",
            "name": "Test User 10",
            "major": "English",
            "yearStatus": "upperclassman",
            "studentYear": "upperclassmen",
            "roomType": "double",
            "genderType": "female",
            "genderPref": "all-female",
            "accessible": "no",
            "isHonors": "no",
            "breakHousing": "no",
            "socialLevel": "minimal-social",
            "noiseLevel": "very-quiet",
            "activitiesImportance": "not-important",
            "environmentPref": "quiet-academic",
            "yearPref": "upperclassmen",
            "sleepSchedule": "early-bird",
            "tidiness": "very-tidy",
            "lifestyleMatch": "very-important",
            "guestFrequency": "never",
            "campusProximity": "essential",
            "activityProximity": "quiet-area",
            "spaceType": "green-spaces",
            "commuteDistance": "under-5min",
            "outdoorSpace": "nice-to-have",
            "communityType": "academic-focused",
            "sharedInterests": "important",
            "sensitivities": "none",
            "priorityLocation": "1",
            "priorityPrivacy": "2",
            "priorityAmenities": "3",
            "prioritySocial": "4"
        },
        min_matches=0
    )))
    
    # Summary
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*70}")
    print(f"Total: {passed}/{total} tests passed ({passed*100//total}%)")
    print(f"{'='*70}\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

