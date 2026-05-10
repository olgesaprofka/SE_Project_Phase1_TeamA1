# ============================================================
# Kindergarten Child Management System
# Core components for testing
# ============================================================

import hashlib
import re
from datetime import datetime, date


# ============================================================
# COMPONENT 1: Login / Authentication
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Simulated user database
USERS_DB = {
    "parent01": {"password": hash_password("parent123"), "role": "parent", "status": "active"},
    "teacher01": {"password": hash_password("teacher123"), "role": "teacher", "status": "active"},
    "admin01":   {"password": hash_password("admin123"),   "role": "admin",   "status": "active"},
    "inactive01":{"password": hash_password("pass123"),    "role": "parent",  "status": "inactive"},
}

def login(username, password):
    """
    Authenticates a user by username and password.
    Returns a dict with status and message.
    """
    if not username or not password:
        return {"status": "error", "message": "Username and password are required"}

    username = username.strip()
    password = password.strip()

    if not username or not password:
        return {"status": "error", "message": "Username and password are required"}

    if username not in USERS_DB:
        return {"status": "error", "message": "Invalid username or password"}

    user = USERS_DB[username]

    if user["status"] == "inactive":
        return {"status": "error", "message": "Account is deactivated"}

    if user["password"] != hash_password(password):
        return {"status": "error", "message": "Invalid username or password"}

    return {"status": "success", "message": "Login successful", "role": user["role"]}


# ============================================================
# COMPONENT 2: Attendance Recording
# ============================================================

# Simulated attendance database
ATTENDANCE_DB = {}
CHILDREN_DB = {
    "C001": {"name": "Ana Koci",    "enrolled": True},
    "C002": {"name": "Luca Marku",  "enrolled": True},
    "C003": {"name": "Sara Hoxha",  "enrolled": False},
}

def record_checkin(child_id, teacher_id, checkin_time=None):
    """
    Records a child's check-in.
    Returns a dict with status and message.
    """
    if not child_id or not teacher_id:
        return {"status": "error", "message": "Child ID and Teacher ID are required"}

    if child_id not in CHILDREN_DB:
        return {"status": "error", "message": "Child not found"}

    if not CHILDREN_DB[child_id]["enrolled"]:
        return {"status": "error", "message": "Child is not enrolled"}

    today = date.today().isoformat()
    key = f"{child_id}_{today}"

    if key in ATTENDANCE_DB and ATTENDANCE_DB[key].get("checkin_time"):
        return {"status": "error", "message": "Child already checked in today"}

    checkin_time = checkin_time or datetime.now().isoformat()
    ATTENDANCE_DB[key] = {
        "child_id": child_id,
        "teacher_id": teacher_id,
        "checkin_time": checkin_time,
        "checkout_time": None,
        "status": "present"
    }
    return {"status": "success", "message": "Check-in recorded successfully", "time": checkin_time}


def record_checkout(child_id, checkout_time=None):
    """
    Records a child's check-out.
    Returns a dict with status and message.
    """
    if not child_id:
        return {"status": "error", "message": "Child ID is required"}

    if child_id not in CHILDREN_DB:
        return {"status": "error", "message": "Child not found"}

    today = date.today().isoformat()
    key = f"{child_id}_{today}"

    if key not in ATTENDANCE_DB:
        return {"status": "error", "message": "No check-in record found for today"}

    if ATTENDANCE_DB[key].get("checkout_time"):
        return {"status": "error", "message": "Child already checked out today"}

    checkout_time = checkout_time or datetime.now().isoformat()
    ATTENDANCE_DB[key]["checkout_time"] = checkout_time
    ATTENDANCE_DB[key]["status"] = "completed"

    return {"status": "success", "message": "Check-out recorded successfully", "time": checkout_time}


def mark_absent(child_id, teacher_id):
    """
    Marks a child as absent for today.
    """
    if not child_id or not teacher_id:
        return {"status": "error", "message": "Child ID and Teacher ID are required"}

    if child_id not in CHILDREN_DB:
        return {"status": "error", "message": "Child not found"}

    today = date.today().isoformat()
    key = f"{child_id}_{today}"

    if key in ATTENDANCE_DB:
        return {"status": "error", "message": "Attendance already recorded for today"}

    ATTENDANCE_DB[key] = {
        "child_id": child_id,
        "teacher_id": teacher_id,
        "checkin_time": None,
        "checkout_time": None,
        "status": "absent"
    }
    return {"status": "success", "message": "Child marked as absent"}


# ============================================================
# COMPONENT 3: Child Profile Management
# ============================================================

PROFILES_DB = {}

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def create_child_profile(child_id, first_name, last_name, date_of_birth,
                          allergy_info="", medical_notes="", emergency_contact=""):
    """
    Creates a new child profile.
    Returns a dict with status and message.
    """
    if not child_id or not first_name or not last_name or not date_of_birth:
        return {"status": "error", "message": "Child ID, first name, last name, and date of birth are required"}

    if not first_name.strip() or not last_name.strip():
        return {"status": "error", "message": "First name and last name cannot be empty"}

    if child_id in PROFILES_DB:
        return {"status": "error", "message": "Child profile already exists"}

    if not validate_date(date_of_birth):
        return {"status": "error", "message": "Invalid date format. Use YYYY-MM-DD"}

    dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    today = date.today()
    age_years = (today - dob).days / 365.25

    if age_years < 1 or age_years > 10:
        return {"status": "error", "message": "Child age must be between 1 and 10 years"}

    PROFILES_DB[child_id] = {
        "child_id": child_id,
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "date_of_birth": date_of_birth,
        "allergy_info": allergy_info.strip(),
        "medical_notes": medical_notes.strip(),
        "emergency_contact": emergency_contact.strip(),
        "enrollment_date": today.isoformat()
    }
    return {"status": "success", "message": "Child profile created successfully"}


def update_child_profile(child_id, **kwargs):
    """
    Updates an existing child profile.
    """
    if not child_id:
        return {"status": "error", "message": "Child ID is required"}

    if child_id not in PROFILES_DB:
        return {"status": "error", "message": "Child profile not found"}

    allowed_fields = {"allergy_info", "medical_notes", "emergency_contact", "first_name", "last_name"}
    for field, value in kwargs.items():
        if field in allowed_fields:
            PROFILES_DB[child_id][field] = value.strip() if isinstance(value, str) else value

    return {"status": "success", "message": "Child profile updated successfully"}


def get_child_profile(child_id):
    """
    Retrieves a child profile by ID.
    """
    if not child_id:
        return {"status": "error", "message": "Child ID is required"}

    if child_id not in PROFILES_DB:
        return {"status": "error", "message": "Child profile not found"}

    return {"status": "success", "data": PROFILES_DB[child_id]}
