# ============================================================
# Phase IV: Software Testing
# Kindergarten Child Management System
# Test File — All 3 Components
# ============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kindergarten_system import (
    login, ATTENDANCE_DB,
    record_checkin, record_checkout, mark_absent, CHILDREN_DB,
    create_child_profile, update_child_profile, get_child_profile, PROFILES_DB
)

# ============================================================
# COMPONENT 1: Login / Authentication Tests
# ============================================================

def test_TC01_valid_login_parent():
    """TC01 - Valid login with correct parent credentials"""
    result = login("parent01", "parent123")
    assert result["status"] == "success", f"Expected success, got: {result}"
    assert result["message"] == "Login successful"
    assert result["role"] == "parent"

def test_TC02_valid_login_teacher():
    """TC02 - Valid login with correct teacher credentials"""
    result = login("teacher01", "teacher123")
    assert result["status"] == "success"
    assert result["role"] == "teacher"

def test_TC03_valid_login_admin():
    """TC03 - Valid login with correct admin credentials"""
    result = login("admin01", "admin123")
    assert result["status"] == "success"
    assert result["role"] == "admin"

def test_TC04_wrong_password():
    """TC04 - Login with correct username but wrong password"""
    result = login("parent01", "wrongpassword")
    assert result["status"] == "error"
    assert result["message"] == "Invalid username or password"

def test_TC05_unknown_username():
    """TC05 - Login with username that does not exist"""
    result = login("unknownuser", "parent123")
    assert result["status"] == "error"
    assert result["message"] == "Invalid username or password"

def test_TC06_empty_username():
    """TC06 - Login with empty username"""
    result = login("", "parent123")
    assert result["status"] == "error"
    assert result["message"] == "Username and password are required"

def test_TC07_empty_password():
    """TC07 - Login with empty password"""
    result = login("parent01", "")
    assert result["status"] == "error"
    assert result["message"] == "Username and password are required"

def test_TC08_both_fields_empty():
    """TC08 - Login with both fields empty"""
    result = login("", "")
    assert result["status"] == "error"
    assert result["message"] == "Username and password are required"

def test_TC09_extra_spaces():
    """TC09 - Boundary: username with extra spaces"""
    result = login("  parent01  ", "parent123")
    assert result["status"] == "success"

def test_TC10_inactive_account():
    """TC10 - Login attempt with deactivated account"""
    result = login("inactive01", "pass123")
    assert result["status"] == "error"
    assert result["message"] == "Account is deactivated"

def test_TC11_case_sensitive_password():
    """TC11 - Boundary: password case sensitivity"""
    result = login("parent01", "Parent123")
    assert result["status"] == "error"
    assert result["message"] == "Invalid username or password"


# ============================================================
# COMPONENT 2: Attendance Recording Tests
# ============================================================

def setup_attendance():
    """Clear attendance DB before each test group"""
    ATTENDANCE_DB.clear()

def test_TC12_valid_checkin():
    """TC12 - Valid check-in for enrolled child"""
    setup_attendance()
    result = record_checkin("C001", "teacher01")
    assert result["status"] == "success"
    assert result["message"] == "Check-in recorded successfully"

def test_TC13_checkin_unenrolled_child():
    """TC13 - Check-in attempt for unenrolled child"""
    setup_attendance()
    result = record_checkin("C003", "teacher01")
    assert result["status"] == "error"
    assert result["message"] == "Child is not enrolled"

def test_TC14_checkin_nonexistent_child():
    """TC14 - Check-in attempt for child that does not exist"""
    setup_attendance()
    result = record_checkin("C999", "teacher01")
    assert result["status"] == "error"
    assert result["message"] == "Child not found"

def test_TC15_duplicate_checkin():
    """TC15 - Duplicate check-in for same child on same day"""
    setup_attendance()
    record_checkin("C001", "teacher01")
    result = record_checkin("C001", "teacher01")
    assert result["status"] == "error"
    assert result["message"] == "Child already checked in today"

def test_TC16_valid_checkout():
    """TC16 - Valid check-out after check-in"""
    setup_attendance()
    record_checkin("C001", "teacher01")
    result = record_checkout("C001")
    assert result["status"] == "success"
    assert result["message"] == "Check-out recorded successfully"

def test_TC17_checkout_without_checkin():
    """TC17 - Check-out attempt without prior check-in"""
    setup_attendance()
    result = record_checkout("C002")
    assert result["status"] == "error"
    assert result["message"] == "No check-in record found for today"

def test_TC18_duplicate_checkout():
    """TC18 - Duplicate check-out for same child"""
    setup_attendance()
    record_checkin("C001", "teacher01")
    record_checkout("C001")
    result = record_checkout("C001")
    assert result["status"] == "error"
    assert result["message"] == "Child already checked out today"

def test_TC19_mark_absent():
    """TC19 - Mark a child as absent"""
    setup_attendance()
    result = mark_absent("C002", "teacher01")
    assert result["status"] == "success"
    assert result["message"] == "Child marked as absent"

def test_TC20_mark_absent_after_checkin():
    """TC20 - Try to mark absent when attendance already recorded"""
    setup_attendance()
    record_checkin("C001", "teacher01")
    result = mark_absent("C001", "teacher01")
    assert result["status"] == "error"
    assert result["message"] == "Attendance already recorded for today"

def test_TC21_checkin_missing_fields():
    """TC21 - Boundary: check-in with missing teacher ID"""
    setup_attendance()
    result = record_checkin("C001", "")
    assert result["status"] == "error"
    assert result["message"] == "Child ID and Teacher ID are required"


# ============================================================
# COMPONENT 3: Child Profile Management Tests
# ============================================================

def setup_profiles():
    """Clear profiles DB before each test group"""
    PROFILES_DB.clear()

def test_TC22_create_valid_profile():
    """TC22 - Create a valid child profile"""
    setup_profiles()
    result = create_child_profile("P001", "Ana", "Koci", "2020-05-15",
                                   allergy_info="Peanuts",
                                   emergency_contact="0681234567")
    assert result["status"] == "success"
    assert result["message"] == "Child profile created successfully"

def test_TC23_create_profile_missing_fields():
    """TC23 - Create profile with missing required fields"""
    setup_profiles()
    result = create_child_profile("P002", "", "Marku", "2020-03-10")
    assert result["status"] == "error"
    assert "required" in result["message"]

def test_TC24_duplicate_profile():
    """TC24 - Create duplicate profile for same child ID"""
    setup_profiles()
    create_child_profile("P001", "Ana", "Koci", "2020-05-15")
    result = create_child_profile("P001", "Ana", "Koci", "2020-05-15")
    assert result["status"] == "error"
    assert result["message"] == "Child profile already exists"

def test_TC25_invalid_date_format():
    """TC25 - Create profile with invalid date format"""
    setup_profiles()
    result = create_child_profile("P003", "Luca", "Marku", "15-05-2020")
    assert result["status"] == "error"
    assert result["message"] == "Invalid date format. Use YYYY-MM-DD"

def test_TC26_child_too_old():
    """TC26 - Boundary: child age above maximum (over 10 years)"""
    setup_profiles()
    result = create_child_profile("P004", "Old", "Child", "2010-01-01")
    assert result["status"] == "error"
    assert "age" in result["message"]

def test_TC27_child_too_young():
    """TC27 - Boundary: child age below minimum (under 1 year)"""
    setup_profiles()
    result = create_child_profile("P005", "Baby", "Child", "2025-12-01")
    assert result["status"] == "error"
    assert "age" in result["message"]

def test_TC28_get_existing_profile():
    """TC28 - Retrieve an existing child profile"""
    setup_profiles()
    create_child_profile("P001", "Ana", "Koci", "2020-05-15")
    result = get_child_profile("P001")
    assert result["status"] == "success"
    assert result["data"]["first_name"] == "Ana"
    assert result["data"]["last_name"] == "Koci"

def test_TC29_get_nonexistent_profile():
    """TC29 - Retrieve profile that does not exist"""
    setup_profiles()
    result = get_child_profile("P999")
    assert result["status"] == "error"
    assert result["message"] == "Child profile not found"

def test_TC30_update_profile():
    """TC30 - Update allergy info on existing profile"""
    setup_profiles()
    create_child_profile("P001", "Ana", "Koci", "2020-05-15")
    result = update_child_profile("P001", allergy_info="Peanuts, Milk")
    assert result["status"] == "success"
    assert PROFILES_DB["P001"]["allergy_info"] == "Peanuts, Milk"

def test_TC31_update_nonexistent_profile():
    """TC31 - Update profile that does not exist"""
    setup_profiles()
    result = update_child_profile("P999", allergy_info="Peanuts")
    assert result["status"] == "error"
    assert result["message"] == "Child profile not found"

def test_TC32_profile_with_spaces_only():
    """TC32 - Boundary: first name with only whitespace"""
    setup_profiles()
    result = create_child_profile("P006", "   ", "Koci", "2020-05-15")
    assert result["status"] == "error"


# ============================================================
# TEST RUNNER
# ============================================================

def run_all_tests():
    tests = [
        # Component 1: Login
        ("TC01", "Valid login - Parent",               test_TC01_valid_login_parent),
        ("TC02", "Valid login - Teacher",              test_TC02_valid_login_teacher),
        ("TC03", "Valid login - Admin",                test_TC03_valid_login_admin),
        ("TC04", "Wrong password",                     test_TC04_wrong_password),
        ("TC05", "Unknown username",                   test_TC05_unknown_username),
        ("TC06", "Empty username",                     test_TC06_empty_username),
        ("TC07", "Empty password",                     test_TC07_empty_password),
        ("TC08", "Both fields empty",                  test_TC08_both_fields_empty),
        ("TC09", "Extra spaces - boundary",            test_TC09_extra_spaces),
        ("TC10", "Inactive account",                   test_TC10_inactive_account),
        ("TC11", "Case sensitive password - boundary", test_TC11_case_sensitive_password),
        # Component 2: Attendance
        ("TC12", "Valid check-in",                     test_TC12_valid_checkin),
        ("TC13", "Unenrolled child check-in",          test_TC13_checkin_unenrolled_child),
        ("TC14", "Nonexistent child check-in",         test_TC14_checkin_nonexistent_child),
        ("TC15", "Duplicate check-in",                 test_TC15_duplicate_checkin),
        ("TC16", "Valid check-out",                    test_TC16_valid_checkout),
        ("TC17", "Check-out without check-in",         test_TC17_checkout_without_checkin),
        ("TC18", "Duplicate check-out",                test_TC18_duplicate_checkout),
        ("TC19", "Mark absent",                        test_TC19_mark_absent),
        ("TC20", "Mark absent after check-in",         test_TC20_mark_absent_after_checkin),
        ("TC21", "Missing teacher ID - boundary",      test_TC21_checkin_missing_fields),
        # Component 3: Child Profile
        ("TC22", "Create valid profile",               test_TC22_create_valid_profile),
        ("TC23", "Missing required fields",            test_TC23_create_profile_missing_fields),
        ("TC24", "Duplicate profile",                  test_TC24_duplicate_profile),
        ("TC25", "Invalid date format",                test_TC25_invalid_date_format),
        ("TC26", "Child too old - boundary",           test_TC26_child_too_old),
        ("TC27", "Child too young - boundary",         test_TC27_child_too_young),
        ("TC28", "Get existing profile",               test_TC28_get_existing_profile),
        ("TC29", "Get nonexistent profile",            test_TC29_get_nonexistent_profile),
        ("TC30", "Update profile",                     test_TC30_update_profile),
        ("TC31", "Update nonexistent profile",         test_TC31_update_nonexistent_profile),
        ("TC32", "Whitespace-only name - boundary",    test_TC32_profile_with_spaces_only),
    ]

    passed = 0
    failed = 0
    errors = []

    print("=" * 65)
    print("  KINDERGARTEN CHILD MANAGEMENT SYSTEM — TEST RESULTS")
    print("=" * 65)

    components = {
        "Component 1: Login / Authentication":    [t for t in tests if t[0] in [f"TC{str(i).zfill(2)}" for i in range(1,12)]],
        "Component 2: Attendance Recording":       [t for t in tests if t[0] in [f"TC{str(i).zfill(2)}" for i in range(12,22)]],
        "Component 3: Child Profile Management":   [t for t in tests if t[0] in [f"TC{str(i).zfill(2)}" for i in range(22,33)]],
    }

    for comp_name, comp_tests in components.items():
        print(f"\n  {comp_name}")
        print("  " + "-" * 62)
        for tc_id, description, func in comp_tests:
            try:
                func()
                print(f"  [PASS] {tc_id} — {description}")
                passed += 1
            except AssertionError as e:
                print(f"  [FAIL] {tc_id} — {description}")
                errors.append((tc_id, description, str(e)))
                failed += 1
            except Exception as e:
                print(f"  [ERROR] {tc_id} — {description}: {e}")
                errors.append((tc_id, description, str(e)))
                failed += 1

    total = passed + failed
    print("\n" + "=" * 65)
    print(f"  SUMMARY: {passed}/{total} tests passed | {failed} failed")
    print(f"  Coverage: {round(passed/total*100, 1)}%")
    print("=" * 65)

    if errors:
        print("\n  FAILED TESTS:")
        for tc_id, desc, msg in errors:
            print(f"  - {tc_id} ({desc}): {msg}")

    return passed, failed

if __name__ == "__main__":
    run_all_tests()
