# Phase IV: Software Testing
## Kindergarten Child Management System


## 1. Introduction to Testing

Software testing is the process of evaluating a software application to identify defects, bugs, or unexpected behavior before the system is deployed. It involves executing the software under controlled conditions and comparing the actual output with the expected output.

Testing is a critical part of software development because it improves the **reliability**, **correctness**, and **maintainability** of the system. Without testing, bugs may reach end users, causing system failures, security vulnerabilities, or incorrect behavior that can have serious consequences — especially in a system that handles sensitive information about children.

In the Kindergarten Child Management System, errors in authentication, attendance recording, or profile management could directly affect the safety and well-being of children and the trust of parents and teachers.

---

## 2. Purpose of Testing

The main purposes of testing in this project are:

- **Identify defects early** — Catching bugs during development is far less costly than fixing them after deployment.
- **Verify correct behavior** — Testing confirms that each component behaves as intended under both expected and unexpected conditions.
- **Validate security** — The login system must reject unauthorized access and handle edge cases such as empty fields and inactive accounts.
- **Ensure data integrity** — Child profiles must be validated to prevent incorrect or incomplete medical information from being stored.
- **Improve confidence** — A fully tested system gives developers and stakeholders confidence that the software works correctly.

---

## 3. Focus on Testing — Selected Components

Three critical components were selected for testing based on their importance to the system's core functionality, security, and data management.

---

### Component 1: Login / Authentication

**Why it was selected:**  
The login function controls access to the entire system. If it fails, unauthorized users may gain access to sensitive child data, or legitimate users may be locked out. It is the first line of defense for system security. The function checks multiple conditions: whether the username exists, whether the password matches, whether the account is active, and whether input fields are empty. Since login directly affects security and user experience, it must be tested thoroughly.

---

### Component 2: Attendance Recording

**Why it was selected:**  
Attendance recording is the most frequently used feature of the system. Teachers use it multiple times every day. Errors in check-in or check-out logic — such as allowing duplicate entries or recording attendance for non-enrolled children — would produce inaccurate records and mislead parents. The function also handles edge cases such as checking out without checking in, and marking a child absent when attendance has already been recorded.

---

### Component 3: Child Profile Management

**Why it was selected:**  
Child profiles store critical personal and medical information including allergies, medical notes, and emergency contacts. Incorrect or incomplete data in this component could have serious consequences for a child's safety. The component must validate required fields, enforce correct date formats, and ensure age boundaries are respected. It also handles profile retrieval and updates, which are used by both teachers and administrators.

---

## 4. Preparing Test Cases

Test cases were designed to cover three categories of scenarios for each component:

- **Normal inputs** — valid data that should result in successful operations
- **Invalid inputs** — incorrect or missing data that should produce appropriate error messages
- **Boundary / Edge cases** — inputs at the limits of acceptable values (extra spaces, minimum/maximum age, duplicate entries)

---

### Component 1: Login / Authentication — Test Cases

| Test ID | Scenario | Input | Expected Result |
|---|---|---|---|
| TC01 | Valid login — Parent | Correct username and password | Login successful, role: parent |
| TC02 | Valid login — Teacher | Correct username and password | Login successful, role: teacher |
| TC03 | Valid login — Admin | Correct username and password | Login successful, role: admin |
| TC04 | Wrong password | Correct username, wrong password | Error: Invalid username or password |
| TC05 | Unknown username | Non-existent username | Error: Invalid username or password |
| TC06 | Empty username | Empty username, valid password | Error: Username and password are required |
| TC07 | Empty password | Valid username, empty password | Error: Username and password are required |
| TC08 | Both fields empty | Empty username and password | Error: Username and password are required |
| TC09 | Extra spaces — boundary | Username with leading/trailing spaces | Login successful (spaces trimmed) |
| TC10 | Inactive account | Valid credentials, deactivated account | Error: Account is deactivated |
| TC11 | Case-sensitive password — boundary | Password with wrong capitalization | Error: Invalid username or password |

---

### Component 2: Attendance Recording — Test Cases

| Test ID | Scenario | Input | Expected Result |
|---|---|---|---|
| TC12 | Valid check-in | Enrolled child, valid teacher | Check-in recorded successfully |
| TC13 | Unenrolled child | Child not enrolled | Error: Child is not enrolled |
| TC14 | Nonexistent child | Child ID not in database | Error: Child not found |
| TC15 | Duplicate check-in | Check-in twice on same day | Error: Child already checked in today |
| TC16 | Valid check-out | Check-in done, then check-out | Check-out recorded successfully |
| TC17 | Check-out without check-in | No prior check-in record | Error: No check-in record found for today |
| TC18 | Duplicate check-out | Check-out twice on same day | Error: Child already checked out today |
| TC19 | Mark absent | Valid child and teacher | Child marked as absent |
| TC20 | Mark absent after check-in | Check-in already recorded | Error: Attendance already recorded for today |
| TC21 | Missing teacher ID — boundary | Empty teacher ID | Error: Child ID and Teacher ID are required |

---

### Component 3: Child Profile Management — Test Cases

| Test ID | Scenario | Input | Expected Result |
|---|---|---|---|
| TC22 | Create valid profile | All required fields, valid date | Profile created successfully |
| TC23 | Missing required fields | Empty first name | Error: required fields message |
| TC24 | Duplicate profile | Same child ID twice | Error: Child profile already exists |
| TC25 | Invalid date format | Date as DD-MM-YYYY | Error: Invalid date format. Use YYYY-MM-DD |
| TC26 | Child too old — boundary | Date of birth in 2010 (over 10 years) | Error: Child age must be between 1 and 10 years |
| TC27 | Child too young — boundary | Date of birth in 2025-12-01 (under 1 year) | Error: Child age must be between 1 and 10 years |
| TC28 | Get existing profile | Valid child ID | Returns profile data successfully |
| TC29 | Get nonexistent profile | Unknown child ID | Error: Child profile not found |
| TC30 | Update profile | Update allergy info | Profile updated successfully |
| TC31 | Update nonexistent profile | Unknown child ID | Error: Child profile not found |
| TC32 | Whitespace-only name — boundary | First name with only spaces | Error: validation message |

---

## 5. Testing Tools

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12.3 | Programming language used for both system and test code |
| pytest | 9.0.3 | Test framework for discovering and running test functions |
| hashlib | built-in | Used for password hashing (SHA-256) in the authentication component |
| datetime | built-in | Used for date validation and timestamp generation in attendance and profiles |

**Setup steps:**
```bash
# Install pytest
pip install pytest

# Run all tests
python3 -m pytest test_kindergarten.py -v

# Or run the custom test runner
python3 test_kindergarten.py
```

---

## 6. Test Code

The system code and test code are separated into two files:
- `kindergarten_system.py` — the core system with all three components
- `test_kindergarten.py` — all 32 test functions

---

### Component 1: Login Function

```python
def login(username, password):
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
```

**Selected test methods — Login:**

```python
def test_TC01_valid_login_parent():
    result = login("parent01", "parent123")
    assert result["status"] == "success"
    assert result["message"] == "Login successful"
    assert result["role"] == "parent"

def test_TC04_wrong_password():
    result = login("parent01", "wrongpassword")
    assert result["status"] == "error"
    assert result["message"] == "Invalid username or password"

def test_TC09_extra_spaces():
    result = login("  parent01  ", "parent123")
    assert result["status"] == "success"

def test_TC10_inactive_account():
    result = login("inactive01", "pass123")
    assert result["status"] == "error"
    assert result["message"] == "Account is deactivated"
```

---

### Component 2: Attendance Recording Function

```python
def record_checkin(child_id, teacher_id, checkin_time=None):
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
```

**Selected test methods — Attendance:**

```python
def test_TC12_valid_checkin():
    ATTENDANCE_DB.clear()
    result = record_checkin("C001", "teacher01")
    assert result["status"] == "success"
    assert result["message"] == "Check-in recorded successfully"

def test_TC15_duplicate_checkin():
    ATTENDANCE_DB.clear()
    record_checkin("C001", "teacher01")
    result = record_checkin("C001", "teacher01")
    assert result["status"] == "error"
    assert result["message"] == "Child already checked in today"

def test_TC17_checkout_without_checkin():
    ATTENDANCE_DB.clear()
    result = record_checkout("C002")
    assert result["status"] == "error"
    assert result["message"] == "No check-in record found for today"
```

---

### Component 3: Child Profile Management Function

```python
def create_child_profile(child_id, first_name, last_name, date_of_birth,
                          allergy_info="", medical_notes="", emergency_contact=""):
    if not child_id or not first_name or not last_name or not date_of_birth:
        return {"status": "error", "message": "Child ID, first name, last name, and date of birth are required"}

    if not first_name.strip() or not last_name.strip():
        return {"status": "error", "message": "First name and last name cannot be empty"}

    if child_id in PROFILES_DB:
        return {"status": "error", "message": "Child profile already exists"}

    if not validate_date(date_of_birth):
        return {"status": "error", "message": "Invalid date format. Use YYYY-MM-DD"}

    dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    age_years = (date.today() - dob).days / 365.25

    if age_years < 1 or age_years > 10:
        return {"status": "error", "message": "Child age must be between 1 and 10 years"}

    PROFILES_DB[child_id] = { ... }
    return {"status": "success", "message": "Child profile created successfully"}
```

**Selected test methods — Child Profile:**

```python
def test_TC22_create_valid_profile():
    PROFILES_DB.clear()
    result = create_child_profile("P001", "Ana", "Koci", "2020-05-15",
                                   allergy_info="Peanuts",
                                   emergency_contact="0681234567")
    assert result["status"] == "success"

def test_TC26_child_too_old():
    PROFILES_DB.clear()
    result = create_child_profile("P004", "Old", "Child", "2010-01-01")
    assert result["status"] == "error"
    assert "age" in result["message"]

def test_TC30_update_profile():
    PROFILES_DB.clear()
    create_child_profile("P001", "Ana", "Koci", "2020-05-15")
    result = update_child_profile("P001", allergy_info="Peanuts, Milk")
    assert result["status"] == "success"
    assert PROFILES_DB["P001"]["allergy_info"] == "Peanuts, Milk"
```

---

## 7. Execution Results

Tests were executed using both the custom test runner and **pytest** framework.

**Command used:**
```bash
python3 -m pytest test_kindergarten.py -v
```

**Full pytest output:**
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
collecting ... collected 32 items

test_kindergarten.py::test_TC01_valid_login_parent          PASSED  [  3%]
test_kindergarten.py::test_TC02_valid_login_teacher         PASSED  [  6%]
test_kindergarten.py::test_TC03_valid_login_admin           PASSED  [  9%]
test_kindergarten.py::test_TC04_wrong_password              PASSED  [ 12%]
test_kindergarten.py::test_TC05_unknown_username            PASSED  [ 15%]
test_kindergarten.py::test_TC06_empty_username              PASSED  [ 18%]
test_kindergarten.py::test_TC07_empty_password              PASSED  [ 21%]
test_kindergarten.py::test_TC08_both_fields_empty           PASSED  [ 25%]
test_kindergarten.py::test_TC09_extra_spaces                PASSED  [ 28%]
test_kindergarten.py::test_TC10_inactive_account            PASSED  [ 31%]
test_kindergarten.py::test_TC11_case_sensitive_password     PASSED  [ 34%]
test_kindergarten.py::test_TC12_valid_checkin               PASSED  [ 37%]
test_kindergarten.py::test_TC13_checkin_unenrolled_child    PASSED  [ 40%]
test_kindergarten.py::test_TC14_checkin_nonexistent_child   PASSED  [ 43%]
test_kindergarten.py::test_TC15_duplicate_checkin           PASSED  [ 46%]
test_kindergarten.py::test_TC16_valid_checkout              PASSED  [ 50%]
test_kindergarten.py::test_TC17_checkout_without_checkin    PASSED  [ 53%]
test_kindergarten.py::test_TC18_duplicate_checkout          PASSED  [ 56%]
test_kindergarten.py::test_TC19_mark_absent                 PASSED  [ 59%]
test_kindergarten.py::test_TC20_mark_absent_after_checkin   PASSED  [ 62%]
test_kindergarten.py::test_TC21_checkin_missing_fields      PASSED  [ 65%]
test_kindergarten.py::test_TC22_create_valid_profile        PASSED  [ 68%]
test_kindergarten.py::test_TC23_create_profile_missing_fields PASSED [ 71%]
test_kindergarten.py::test_TC24_duplicate_profile           PASSED  [ 75%]
test_kindergarten.py::test_TC25_invalid_date_format         PASSED  [ 78%]
test_kindergarten.py::test_TC26_child_too_old               PASSED  [ 81%]
test_kindergarten.py::test_TC27_child_too_young             PASSED  [ 84%]
test_kindergarten.py::test_TC28_get_existing_profile        PASSED  [ 87%]
test_kindergarten.py::test_TC29_get_nonexistent_profile     PASSED  [ 90%]
test_kindergarten.py::test_TC30_update_profile              PASSED  [ 93%]
test_kindergarten.py::test_TC31_update_nonexistent_profile  PASSED  [ 96%]
test_kindergarten.py::test_TC32_profile_with_spaces_only    PASSED  [100%]

============================== 32 passed in 0.06s ==============================
```

**Summary:**

| Component | Tests | Passed | Failed |
|---|---|---|---|
| Login / Authentication | 11 | 11 | 0 |
| Attendance Recording | 10 | 10 | 0 |
| Child Profile Management | 11 | 11 | 0 |
| **TOTAL** | **32** | **32** | **0** |

---

## 8. Coverage and Reflection

### Test Coverage

All 32 test cases passed successfully with **100% pass rate**. The tests cover the following paths for each component:

**Login / Authentication:**
- All three valid user roles (parent, teacher, admin)
- Invalid credentials (wrong password, unknown username)
- Empty field validation (username only, password only, both empty)
- Boundary cases (extra spaces, case-sensitive passwords)
- Account state (inactive account rejection)

**Attendance Recording:**
- Full check-in and check-out cycle
- Error conditions (unenrolled child, nonexistent child, duplicate entries)
- Edge cases (checkout without check-in, marking absent after check-in)
- Missing input validation (empty teacher ID)

**Child Profile Management:**
- Successful profile creation with all fields
- Required field validation
- Duplicate prevention
- Date format validation
- Age boundary enforcement (minimum and maximum)
- Profile retrieval and update operations
- Whitespace-only input handling

### Reflection

The testing process revealed that testing boundary cases is just as important as testing normal cases. For example, the extra-spaces boundary test (TC09) confirmed that the login function correctly trims whitespace before validation, which is a behavior that might otherwise be overlooked.

The age boundary tests (TC26, TC27) confirmed that the child profile system correctly rejects children outside the acceptable age range — this is especially important because incorrect age data could affect how the kindergarten manages enrollments.

**What could still be improved:**
- Integration tests could be added to test how components interact with each other (e.g., a teacher logging in and then recording attendance)
- Database-level tests with a real MySQL connection would provide more realistic coverage
- Performance tests could verify system behavior under load (e.g., 500 concurrent users as specified in Phase II non-functional requirements)
- Security tests could attempt SQL injection and other attack vectors on the login function
