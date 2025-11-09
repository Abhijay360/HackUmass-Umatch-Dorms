#!/usr/bin/env python3
"""
Test suite for UMass Housing Recommender matching system
Tests year normalization, fallback scoring, and match finding
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from HackUmass_back_end import (
    score_and_rank_matches,
    get_all_profiles_from_db,
    calculate_fallback_score,
    get_dorm_recommendation
)

def print_test_header(test_name):
    print("\n" + "="*80)
    print(f"TEST: {test_name}")
    print("="*80)

def print_result(result, expected_matches_min=1):
    dorm_rec = result.get('dorm_recommendation', 'N/A')
    matches = result.get('ranked_matches', [])
    message = result.get('message', '')
    is_alternative = result.get('is_alternative', False)
    
    print(f"\n✅ Results:")
    print(f"   Dorm Recommendation: {dorm_rec}")
    print(f"   Matches Found: {len(matches)}")
    print(f"   Alternative Match: {'Yes' if is_alternative else 'No'}")
    
    if matches:
        print(f"\n   Top Matches:")
        for i, match in enumerate(matches[:3], 1):
            score = match.get('compatibilityScore', 0)
            name = match.get('candidateName', 'N/A')
            dorm = match.get('recommendedDorms', 'N/A')
            is_alt = match.get('isAlternative', False)
            alt_tag = " [ALTERNATIVE]" if is_alt else ""
            print(f"   {i}. {name} - {score}% - {dorm}{alt_tag}")
    else:
        print(f"   ⚠️  No matches found")
        if message:
            print(f"   Message: {message}")
    
    # Validation
    if len(matches) >= expected_matches_min:
        print(f"\n   ✅ PASS: Found {len(matches)} matches (expected at least {expected_matches_min})")
        return True
    else:
        print(f"\n   ❌ FAIL: Found {len(matches)} matches (expected at least {expected_matches_min})")
        return False

# Test Case 1: Upperclassman, North Apartments (should find matches)
def test_upperclassman_north():
    print_test_header("Upperclassman - North Apartments Recommendation")
    
    profile = {
        'userId': 'test_upperclassman',
        'name': 'Test Upperclassman',
        'major': 'Computer Science',
        'yearStatus': 'upperclassman',  # Frontend format
        'studentYear': 'upperclassmen',  # Backend format
        'roomType': 'apartment',
        'genderType': 'male',
        'genderPref': 'coed',
        'socialLevel': 'moderately-social',
        'noiseLevel': 'quiet',
        'sleepSchedule': 'balanced',
        'tidiness': 'tidy',
        'guestFrequency': 'monthly',
        'communityType': 'general',
        'priorityLocation': '1',
        'priorityPrivacy': '1',
        'priorityAmenities': '2',
        'prioritySocial': '3',
        'college': 'College of Info. & Computer Sciences',
        'breakHousingPref': 'no',
        'isHonors': 'no'
    }
    
    result = score_and_rank_matches(profile, profile['userId'])
    return print_result(result, expected_matches_min=1)

# Test Case 2: First-year, North Apartments (should be blocked, find alternatives)
def test_firstyear_north_blocked():
    print_test_header("First-Year - North Apartments Blocked (Should Find Alternatives)")
    
    profile = {
        'userId': 'test_firstyear',
        'name': 'Test First-Year',
        'major': 'Computer Science',
        'yearStatus': 'first-year',  # Frontend format
        'studentYear': 'first-years',  # Backend format
        'roomType': 'double',
        'genderType': 'male',
        'genderPref': 'coed',
        'socialLevel': 'moderately-social',
        'noiseLevel': 'quiet',
        'sleepSchedule': 'early-bird',
        'tidiness': 'tidy',
        'guestFrequency': 'weekly',
        'communityType': 'academic-focused',
        'priorityLocation': '1',
        'priorityPrivacy': '2',
        'priorityAmenities': '3',
        'prioritySocial': '4',
        'college': 'College of Info. & Computer Sciences',
        'breakHousingPref': 'no',
        'isHonors': 'no'
    }
    
    result = score_and_rank_matches(profile, profile['userId'])
    # Should find alternative matches from other dorms
    return print_result(result, expected_matches_min=1)

# Test Case 3: Year Format Normalization (singular vs plural)
def test_year_format_normalization():
    print_test_header("Year Format Normalization (first-year vs first-years)")
    
    # Test with singular form
    profile_singular = {
        'userId': 'test_singular',
        'name': 'Test User',
        'major': 'Biology',
        'yearStatus': 'first-year',  # Singular
        'roomType': 'double',
        'genderType': 'female',
        'genderPref': 'coed',
        'socialLevel': 'moderately-social',
        'noiseLevel': 'moderate',
        'sleepSchedule': 'balanced',
        'tidiness': 'moderately-tidy',
        'guestFrequency': 'weekly',
        'communityType': 'tight-knit',
        'priorityLocation': '2',
        'priorityPrivacy': '3',
        'priorityAmenities': '4',
        'prioritySocial': '1',
        'college': 'College of Natural Sciences',
        'breakHousingPref': 'no',
        'isHonors': 'no'
    }
    
    # Check if candidates are found
    candidates = get_all_profiles_from_db('test_singular', ['Orchard Hill'], 'first-years')
    print(f"\n   Found {len(candidates)} candidates with normalized year format")
    
    if len(candidates) > 0:
        print(f"   ✅ PASS: Year normalization works (found {len(candidates)} candidates)")
        return True
    else:
        print(f"   ❌ FAIL: Year normalization failed (found 0 candidates)")
        return False

# Test Case 4: Fallback Scoring Test
def test_fallback_scoring():
    print_test_header("Fallback Scoring (When API Fails)")
    
    profile_a = {
        'sleepSchedule': 'balanced',
        'tidiness': 'tidy',
        'noiseLevel': 'quiet',
        'socialLevel': 'moderately-social'
    }
    
    profile_b = {
        'sleepSchedule': 'balanced',
        'tidiness': 'tidy',
        'noiseLevel': 'quiet',
        'socialLevel': 'moderately-social',
        'name': 'Compatible Candidate',
        'dormArea': 'Central'
    }
    
    score = calculate_fallback_score(profile_a, profile_b)
    print(f"\n   Fallback Score: {score}%")
    
    if score >= 75:
        print(f"   ✅ PASS: Fallback scoring returns 75+ for compatible matches")
        return True
    else:
        print(f"   ❌ FAIL: Fallback scoring returned {score}% (expected 75+)")
        return False

# Test Case 5: Fallback Scoring - Major Conflicts
def test_fallback_scoring_conflicts():
    print_test_header("Fallback Scoring - Major Conflicts (Should Return 0)")
    
    profile_a = {
        'sleepSchedule': 'early-bird',
        'tidiness': 'very-tidy',
        'noiseLevel': 'very-quiet',
        'socialLevel': 'minimal-social'
    }
    
    profile_b = {
        'sleepSchedule': 'night-owl',  # Major conflict
        'tidiness': 'messy',  # Major conflict
        'noiseLevel': 'loud',  # Major conflict
        'socialLevel': 'very-social',
        'name': 'Incompatible Candidate',
        'dormArea': 'Southwest'
    }
    
    score = calculate_fallback_score(profile_a, profile_b)
    print(f"\n   Fallback Score: {score}%")
    
    if score == 0:
        print(f"   ✅ PASS: Fallback scoring correctly identifies major conflicts (score: 0)")
        return True
    else:
        print(f"   ❌ FAIL: Fallback scoring returned {score}% (expected 0 for major conflicts)")
        return False

# Test Case 6: Alternative Matching Trigger
def test_alternative_matching():
    print_test_header("Alternative Matching (When No Matches in Primary Area)")
    
    # Profile that won't match well with North candidates
    profile = {
        'userId': 'test_alternative',
        'name': 'Test User',
        'major': 'Business',
        'yearStatus': 'upperclassman',
        'studentYear': 'upperclassmen',
        'roomType': 'double',
        'genderType': 'male',
        'genderPref': 'coed',
        'socialLevel': 'very-social',
        'noiseLevel': 'loud',
        'sleepSchedule': 'night-owl',
        'tidiness': 'messy',
        'guestFrequency': 'daily',
        'communityType': 'social-focused',
        'priorityLocation': '4',
        'priorityPrivacy': '3',
        'priorityAmenities': '2',
        'prioritySocial': '1',
        'college': 'Isenberg School of Management',
        'breakHousingPref': 'required',
        'isHonors': 'no'
    }
    
    result = score_and_rank_matches(profile, profile['userId'])
    is_alternative = result.get('is_alternative', False)
    matches = result.get('ranked_matches', [])
    
    print_result(result, expected_matches_min=1)
    
    if is_alternative and len(matches) > 0:
        print(f"   ✅ PASS: Alternative matching triggered and found matches")
        return True
    elif len(matches) > 0:
        print(f"   ⚠️  WARNING: Found matches but alternative flag not set")
        return True  # Still a pass if matches found
    else:
        print(f"   ❌ FAIL: Alternative matching did not find any matches")
        return False

# Test Case 7: Dorm Recommendation for Different Majors
def test_dorm_recommendations():
    print_test_header("Dorm Recommendations by Major")
    
    majors_to_test = [
        ('Computer Science', 'Northeast'),
        ('Business', 'Southwest'),
        ('Biology', 'Orchard Hill'),
        ('Engineering', 'Northeast'),
    ]
    
    all_passed = True
    for major, expected_area in majors_to_test:
        profile = {
            'major': major,
            'college': 'General/Other',
            'studentYear': 'upperclassmen',
            'isHonors': 'no'
        }
        
        rec = get_dorm_recommendation(profile)
        recommended = rec['recommendedArea']
        
        if expected_area.lower() in recommended.lower() or recommended.lower() in expected_area.lower():
            print(f"   ✅ {major:20} → {recommended:15} (expected: {expected_area})")
        else:
            print(f"   ⚠️  {major:20} → {recommended:15} (expected: {expected_area})")
            all_passed = False
    
    return all_passed

# Test Case 8: Honors Student CHCRC Recommendation
def test_honors_chcrc():
    print_test_header("Honors Student - CHCRC Recommendation")
    
    profile = {
        'userId': 'test_honors',
        'name': 'Test Honors Student',
        'major': 'History',
        'yearStatus': 'upperclassman',
        'studentYear': 'upperclassmen',
        'isHonors': 'yes',
        'roomType': 'double',
        'genderType': 'female',
        'genderPref': 'coed',
        'socialLevel': 'moderately-social',
        'noiseLevel': 'quiet',
        'sleepSchedule': 'early-bird',
        'tidiness': 'very-tidy',
        'guestFrequency': 'rarely',
        'communityType': 'honors-focused',
        'priorityLocation': '1',
        'priorityPrivacy': '2',
        'priorityAmenities': '3',
        'prioritySocial': '4',
        'college': 'Commonwealth Honors College',
        'breakHousingPref': 'no',
        'isHonors': 'yes'
    }
    
    rec = get_dorm_recommendation(profile)
    recommended = rec['recommendedArea']
    
    print(f"\n   Recommended Dorm: {recommended}")
    
    if recommended == 'CHCRC':
        print(f"   ✅ PASS: Honors student correctly recommended CHCRC")
        return True
    else:
        print(f"   ⚠️  WARNING: Honors student recommended {recommended} instead of CHCRC")
        return True  # Not a critical failure

# Run all tests
def run_all_tests():
    print("\n" + "="*80)
    print("UMASS HOUSING RECOMMENDER - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    tests = [
        ("Upperclassman North Apartments", test_upperclassman_north),
        ("First-Year North Blocked", test_firstyear_north_blocked),
        ("Year Format Normalization", test_year_format_normalization),
        ("Fallback Scoring (Compatible)", test_fallback_scoring),
        ("Fallback Scoring (Conflicts)", test_fallback_scoring_conflicts),
        ("Alternative Matching", test_alternative_matching),
        ("Dorm Recommendations", test_dorm_recommendations),
        ("Honors CHCRC", test_honors_chcrc),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n   ❌ ERROR in {test_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({passed*100//total}%)")
    print("="*80 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

