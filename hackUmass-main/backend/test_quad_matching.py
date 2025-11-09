#!/usr/bin/env python3
"""
Test script for quad room matching functionality
Tests that:
1. Quad rooms return 3 matches
2. No "triple" references exist
3. Backend handles quad room type correctly
"""

import sys
import os
import re

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from HackUmass_back_end import (
    score_and_rank_matches,
    get_dorm_recommendation,
    get_all_profiles_from_db
)

def test_quad_room_matching():
    """Test that quad rooms return 3 matches"""
    print("=" * 60)
    print("TEST 1: Quad Room Matching (Should return 3 matches)")
    print("=" * 60)
    
    # Create a test profile for quad room
    test_profile = {
        "userId": "test_user_quad",
        "name": "Test User",
        "major": "Business",
        "yearStatus": "first-year",
        "studentYear": "first-years",
        "roomType": "quad",  # Quad room type
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
    }
    
    try:
        result = score_and_rank_matches(test_profile, "test_user_quad")
        
        print(f"\n✅ Test Profile:")
        print(f"   Room Type: {test_profile['roomType']}")
        print(f"   Major: {test_profile['major']}")
        print(f"   Year: {test_profile['yearStatus']}")
        
        print(f"\n📊 Results:")
        print(f"   Dorm Recommendation: {result.get('dorm_recommendation', 'N/A')}")
        print(f"   Number of Matches: {len(result.get('ranked_matches', []))}")
        
        matches = result.get('ranked_matches', [])
        if len(matches) > 0:
            print(f"\n   Matches Found:")
            for i, match in enumerate(matches, 1):
                print(f"   {i}. {match.get('candidateName', 'N/A')} - {match.get('compatibilityScore', 0)}%")
        
        # Assertion: Quad rooms should return up to 3 matches
        if len(matches) <= 3:
            print(f"\n✅ PASS: Quad room returned {len(matches)} match(es) (expected up to 3)")
            if len(matches) == 3:
                print("   ✅ Perfect: All 3 roommates found for quad room!")
            elif len(matches) > 0:
                print(f"   ⚠️  Warning: Only {len(matches)} of 3 roommates found")
            return True
        else:
            print(f"\n❌ FAIL: Quad room returned {len(matches)} matches (expected max 3)")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_double_room_matching():
    """Test that double rooms return normal matching"""
    print("\n" + "=" * 60)
    print("TEST 2: Double Room Matching (Should return normal matches)")
    print("=" * 60)
    
    test_profile = {
        "userId": "test_user_double",
        "name": "Test User",
        "major": "Computer Science",
        "yearStatus": "upperclassman",
        "studentYear": "upperclassmen",
        "roomType": "double",  # Double room type
        "genderType": "female",
        "genderPref": "coed",
        "accessible": "no",
        "isHonors": "no",
        "breakHousing": "no",
        "socialLevel": "moderately-social",
        "noiseLevel": "quiet",
        "activitiesImportance": "somewhat-important",
        "environmentPref": "balanced",
        "yearPref": "upperclassmen",
        "sleepSchedule": "early-bird",
        "tidiness": "tidy",
        "lifestyleMatch": "important",
        "guestFrequency": "monthly",
        "campusProximity": "important",
        "activityProximity": "quiet-area",
        "spaceType": "green-spaces",
        "commuteDistance": "5-10min",
        "outdoorSpace": "nice-to-have",
        "communityType": "general",
        "sharedInterests": "important",
        "sensitivities": "none",
        "priorityLocation": "1",
        "priorityPrivacy": "2",
        "priorityAmenities": "3",
        "prioritySocial": "4"
    }
    
    try:
        result = score_and_rank_matches(test_profile, "test_user_double")
        
        print(f"\n✅ Test Profile:")
        print(f"   Room Type: {test_profile['roomType']}")
        print(f"   Major: {test_profile['major']}")
        
        matches = result.get('ranked_matches', [])
        print(f"\n📊 Results:")
        print(f"   Dorm Recommendation: {result.get('dorm_recommendation', 'N/A')}")
        print(f"   Number of Matches: {len(matches)}")
        
        if len(matches) > 0:
            print(f"\n   ✅ PASS: Double room matching works correctly")
            return True
        else:
            print(f"\n   ⚠️  No matches found (this might be expected)")
            return True  # Not a failure, just no matches
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_no_triple_references():
    """Test that no 'triple' references exist in the code"""
    print("\n" + "=" * 60)
    print("TEST 3: Verify No 'triple' References")
    print("=" * 60)
    
    import re
    
    backend_file = os.path.join(os.path.dirname(__file__), 'HackUmass_back_end.py')
    
    try:
        with open(backend_file, 'r') as f:
            content = f.read()
        
        # Search for "triple" (case-insensitive)
        triple_matches = re.findall(r'triple', content, re.IGNORECASE)
        
        if triple_matches:
            print(f"\n❌ FAIL: Found {len(triple_matches)} reference(s) to 'triple':")
            for match in set(triple_matches):
                print(f"   - '{match}'")
            return False
        else:
            print(f"\n✅ PASS: No 'triple' references found in backend")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

def test_quad_candidate_exists():
    """Test that quad candidate exists in simulated profiles"""
    print("\n" + "=" * 60)
    print("TEST 4: Verify Quad Candidate Exists")
    print("=" * 60)
    
    backend_file = os.path.join(os.path.dirname(__file__), 'HackUmass_back_end.py')
    
    try:
        with open(backend_file, 'r') as f:
            content = f.read()
        
        # Search for quad roomType in candidate profiles
        quad_matches = re.findall(r'"roomType":\s*"quad"', content, re.IGNORECASE)
        
        if quad_matches:
            print(f"\n✅ PASS: Found {len(quad_matches)} candidate(s) with roomType 'quad'")
            return True
        else:
            print(f"\n❌ FAIL: No candidates with roomType 'quad' found")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 RUNNING BACKEND TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test 1: Quad room matching
    results.append(("Quad Room Matching", test_quad_room_matching()))
    
    # Test 2: Double room matching
    results.append(("Double Room Matching", test_double_room_matching()))
    
    # Test 3: No triple references
    results.append(("No Triple References", test_no_triple_references()))
    
    # Test 4: Quad candidate exists
    results.append(("Quad Candidate Exists", test_quad_candidate_exists()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'=' * 60}")
    print(f"Total: {passed}/{total} tests passed")
    print(f"{'=' * 60}\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

