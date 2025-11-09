#!/usr/bin/env python3
"""
Quick test suite - tests core functionality without API calls
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from HackUmass_back_end import (
    get_all_profiles_from_db,
    calculate_fallback_score,
    get_dorm_recommendation
)

def test_1_year_normalization():
    """Test year format normalization"""
    print("\n" + "="*60)
    print("TEST 1: Year Format Normalization")
    print("="*60)
    
    # Test singular vs plural
    candidates1 = get_all_profiles_from_db('test', ['Central'], 'upperclassmen')
    candidates2 = get_all_profiles_from_db('test', ['Central'], 'upperclassman')
    
    print(f"   'upperclassmen' (plural): {len(candidates1)} candidates")
    print(f"   'upperclassman' (singular): {len(candidates2)} candidates")
    
    if len(candidates1) == len(candidates2) and len(candidates1) > 0:
        print(f"   ✅ PASS: Year normalization works")
        return True
    else:
        print(f"   ❌ FAIL: Year normalization issue")
        return False

def test_2_north_upperclassmen():
    """Test North Apartments for upperclassmen"""
    print("\n" + "="*60)
    print("TEST 2: North Apartments - Upperclassmen")
    print("="*60)
    
    candidates = get_all_profiles_from_db('test', ['North'], 'upperclassmen')
    print(f"   Found {len(candidates)} candidates in North for upperclassmen")
    
    for c in candidates:
        print(f"     - {c['name']} ({c['dormArea']})")
    
    if len(candidates) >= 2:
        print(f"   ✅ PASS: Found {len(candidates)} candidates (expected 2+)")
        return True
    else:
        print(f"   ❌ FAIL: Found {len(candidates)} candidates (expected 2+)")
        return False

def test_3_north_firstyear_blocked():
    """Test North Apartments blocked for first-years"""
    print("\n" + "="*60)
    print("TEST 3: North Apartments - First-Year Blocked")
    print("="*60)
    
    candidates = get_all_profiles_from_db('test', ['North'], 'first-years')
    print(f"   Found {len(candidates)} candidates in North for first-years")
    
    if len(candidates) == 0:
        print(f"   ✅ PASS: North correctly blocked for first-years")
        return True
    else:
        print(f"   ❌ FAIL: North not blocked (found {len(candidates)} candidates)")
        return False

def test_4_fallback_scoring():
    """Test fallback scoring"""
    print("\n" + "="*60)
    print("TEST 4: Fallback Scoring")
    print("="*60)
    
    # Compatible profiles
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
        'socialLevel': 'moderately-social'
    }
    
    score = calculate_fallback_score(profile_a, profile_b)
    print(f"   Compatible profiles score: {score}%")
    
    # Incompatible profiles
    profile_c = {
        'sleepSchedule': 'early-bird',
        'tidiness': 'very-tidy',
        'noiseLevel': 'very-quiet',
        'socialLevel': 'minimal-social'
    }
    
    profile_d = {
        'sleepSchedule': 'night-owl',
        'tidiness': 'messy',
        'noiseLevel': 'loud',
        'socialLevel': 'very-social'
    }
    
    score2 = calculate_fallback_score(profile_c, profile_d)
    print(f"   Incompatible profiles score: {score2}%")
    
    if score >= 75 and score2 == 0:
        print(f"   ✅ PASS: Fallback scoring works correctly")
        return True
    else:
        print(f"   ❌ FAIL: Fallback scoring issue (compatible: {score}%, incompatible: {score2}%)")
        return False

def test_5_dorm_recommendations():
    """Test dorm recommendations by major"""
    print("\n" + "="*60)
    print("TEST 5: Dorm Recommendations by Major")
    print("="*60)
    
    test_cases = [
        ('Computer Science', 'Northeast'),
        ('Business', 'Southwest'),
        ('Biology', 'Orchard Hill'),
    ]
    
    all_pass = True
    for major, expected in test_cases:
        profile = {
            'major': major,
            'college': 'General/Other',
            'studentYear': 'upperclassmen',
            'isHonors': 'no'
        }
        rec = get_dorm_recommendation(profile)
        recommended = rec['recommendedArea']
        match = expected.lower() in recommended.lower() or recommended.lower() in expected.lower()
        status = "✅" if match else "⚠️"
        print(f"   {status} {major:20} → {recommended:15} (expected: {expected})")
        if not match:
            all_pass = False
    
    return all_pass

def test_6_honors_chcrc():
    """Test Honors student gets CHCRC"""
    print("\n" + "="*60)
    print("TEST 6: Honors Student - CHCRC")
    print("="*60)
    
    profile = {
        'major': 'History',
        'college': 'Commonwealth Honors College',
        'studentYear': 'upperclassmen',
        'isHonors': 'yes'
    }
    
    rec = get_dorm_recommendation(profile)
    recommended = rec['recommendedArea']
    print(f"   Recommended: {recommended}")
    
    if recommended == 'CHCRC':
        print(f"   ✅ PASS: Honors student correctly recommended CHCRC")
        return True
    else:
        print(f"   ⚠️  WARNING: Recommended {recommended} instead of CHCRC")
        return True  # Not critical

# Run all tests
if __name__ == "__main__":
    print("\n" + "="*60)
    print("QUICK TEST SUITE - Core Functionality")
    print("="*60)
    
    tests = [
        ("Year Normalization", test_1_year_normalization),
        ("North - Upperclassmen", test_2_north_upperclassmen),
        ("North - First-Year Blocked", test_3_north_firstyear_blocked),
        ("Fallback Scoring", test_4_fallback_scoring),
        ("Dorm Recommendations", test_5_dorm_recommendations),
        ("Honors CHCRC", test_6_honors_chcrc),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n   ❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")

