# Phase II: User Requirements and Application Specifications

---

## 1. Chosen Development Model

### Development Model: Agile

### Justification
The Agile development model was selected for the development of the Kindergarten Child Management System due to its flexibility, iterative nature, and ability to adapt to evolving project requirements. Since the application may require continuous refinement based on stakeholder feedback, Agile allows the development team to deliver the system incrementally while improving functionality in each iteration. This approach promotes effective collaboration, continuous testing, and early identification of issues, ensuring the final product aligns with user expectations and business needs.

---

## 2. User Requirements

### a. Stakeholders

#### Parents / Guardians
Parents are the primary end-users of the system who require continuous access to information regarding their child’s attendance, daily activities, health-related information, and communication with teachers.

#### Teachers
Teachers are responsible for maintaining student records, recording attendance, uploading daily activity updates, and ensuring accurate communication with parents.

#### Kindergarten Administration
Administrators oversee the entire kindergarten management process, including user account management, data monitoring, report generation, and supervision of operational workflows.

#### Children
Although children do not directly interact with the application, they are the main beneficiaries of the improved monitoring, communication, and personalized care enabled by the system.

#### Development Team
The development team is responsible for designing, implementing, testing, and maintaining the software application.

---

### b. User Stories

1. As a parent, I want to receive attendance notifications so that I know when my child arrives at or leaves the kindergarten.

2. As a parent, I want to access daily activity reports so that I can stay informed about my child’s learning and development.

3. As a parent, I want to add my child’s medical and allergy information so that I can ensure teachers are informed of any special requirements.

4. As a teacher, I want to digitally record attendance so that student presence is tracked accurately and efficiently.

5. As a teacher, I want to upload activity summaries and media so that parents can monitor their child’s daily engagement.

6. As a teacher, I want to update child profiles so that important information remains current.

7. As an administrator, I want to manage all user accounts so that access permissions remain controlled and organized.

8. As an administrator, I want to generate attendance and performance reports so that management decisions can be data-driven.

9. As a parent, I want to communicate directly with teachers through the platform so that communication is efficient and centralized.

10. As a teacher, I want to receive alerts for children with allergies or medical conditions so that I can provide safe care.

---

## 3. Functional Requirements

### a. Description

1. The system shall allow users to register new accounts.
2. The system shall allow users to log in securely using email and password.
3. The system shall provide password reset functionality.
4. The system shall support role-based authentication.
5. The system shall allow teachers to record child attendance.
6. The system shall automatically timestamp check-in and check-out events.
7. The system shall notify parents when attendance is recorded.
8. The system shall store child personal and medical information.
9. The system shall store child allergy and emergency contact details.
10. The system shall allow authorized users to edit child profiles.
11. The system shall allow teachers to upload daily activity reports.
12. The system shall allow image and file uploads related to activities.
13. The system shall provide messaging functionality between parents and teachers.
14. The system shall allow administrators to manage user accounts.
15. The system shall allow administrators to activate/deactivate accounts.
16. The system shall generate attendance reports.
17. The system shall generate child development/progress reports.
18. The system shall provide dashboards customized by user role.
19. The system shall support filtering and searching of child records.
20. The system shall maintain activity logs for system actions.
21. The system shall maintain notification history.
22. The system shall support linking multiple children to one parent account.
23. The system shall store emergency contact information.
24. The system shall send reminders for incomplete attendance entries.
25. The system shall export reports in downloadable formats.

---

### b. Acceptance Criteria

#### User Authentication
- User enters valid credentials.
- System verifies credentials successfully.
- User is redirected to role-specific dashboard.
- Invalid credentials produce an error message.

#### Attendance Recording
- Teacher selects child from attendance list.
- Teacher records attendance status.
- Timestamp is automatically generated.
- Parent receives attendance notification.

#### Child Profile Management
- Authorized user enters profile details.
- Required fields are validated.
- Data is stored successfully.
- Updated information is displayed immediately.

#### Messaging System
- User composes and sends message.
- Recipient receives notification.
- Message is stored in conversation history.
- Recipient can respond successfully.

#### Report Generation
- User selects report parameters.
- System retrieves corresponding records.
- Report is generated accurately.
- Report is downloadable/exportable.

---

## 4. Non-Functional Requirements

### a. Description

1. The system should load pages within acceptable response times.
2. The system should support at least 500 concurrent users.
3. The system should maintain high availability.
4. The system should protect user data securely.
5. The system should encrypt sensitive information.
6. The system should provide responsive user interfaces.
7. The system should be mobile-compatible.
8. The system should recover quickly from unexpected failures.
9. The system should validate all user inputs.
10. The system should prevent unauthorized access.
11. The system should maintain automated backups.
12. The system should provide intuitive navigation.
13. The system should support future scalability.
14. The system should maintain data consistency.
15. The system should be compatible across modern browsers.
16. The system should automatically log errors.
17. The system should support accessibility standards.
18. The system should use readable typography and layout.
19. The system should minimize maintenance downtime.
20. The system should maintain audit trails for major actions.

---

### b. Acceptance Criteria

#### Performance
- Pages load within 2 seconds under normal conditions.
- Search results display within 2 seconds.
- Dashboard loads within 3 seconds.

#### Security
- Passwords are hashed before storage.
- Unauthorized users cannot access restricted resources.
- Sessions expire after inactivity.

#### Reliability
- Monthly uptime remains above 99%.
- Daily backups are performed automatically.
- Recovery from system failure occurs within 10 minutes.

#### Usability
- Interface is understandable for first-time users.
- Navigation menus are clearly labeled.
- Mobile interface adapts correctly to screen size.

#### Scalability
- System supports at least 1000 child records.
- Performance remains stable under increasing load.
- New modules can be integrated without structural redesign.

---

## 5. Application Specifications

### a. Architecture

The application follows a three-tier architecture consisting of:

#### Presentation Layer (Frontend)
Responsible for displaying the user interface and handling user interactions.

#### Application Layer (Backend)
Responsible for processing business logic, validating requests, enforcing rules, and handling communication between frontend and database.

#### Data Layer (Database)
Responsible for storing, managing, and retrieving all persistent system data.

The frontend communicates with the backend through HTTP/API requests. The backend processes the requests, executes business logic, and interacts with the database for data retrieval and storage.

---

### b. Database Model

The system uses a relational database model designed according to normalization principles to ensure consistency, eliminate redundancy, and maintain referential integrity.

#### Entity: Users
Stores all system users.

**Attributes:**
- user_id (Primary Key)
- full_name
- email (Unique)
- password_hash
- phone_number
- role
- account_status
- created_at
- updated_at

---

#### Entity: Children
Stores child-related information.

**Attributes:**
- child_id (Primary Key)
- first_name
- last_name
- date_of_birth
- gender
- allergy_information
- medical_notes
- emergency_contact
- enrollment_date
- profile_photo

---

#### Entity: ParentChildRelationship
Associative entity used to establish many-to-many relationships between parents and children.

**Attributes:**
- relationship_id (Primary Key)
- parent_id (Foreign Key → Users.user_id)
- child_id (Foreign Key → Children.child_id)
- relationship_type

---

#### Entity: AttendanceRecords
Stores attendance history.

**Attributes:**
- attendance_id (Primary Key)
- child_id (Foreign Key → Children.child_id)
- recorded_by (Foreign Key → Users.user_id)
- attendance_date
- check_in_time
- check_out_time
- attendance_status

---

#### Entity: ActivityReports
Stores daily activity logs.

**Attributes:**
- activity_id (Primary Key)
- child_id (Foreign Key → Children.child_id)
- teacher_id (Foreign Key → Users.user_id)
- title
- description
- attachment_url
- created_at

---

#### Entity: Messages
Stores internal communication between users.

**Attributes:**
- message_id (Primary Key)
- sender_id (Foreign Key → Users.user_id)
- receiver_id (Foreign Key → Users.user_id)
- message_body
- sent_at
- is_read

---

#### Entity: Notifications
Stores automated system notifications.

**Attributes:**
- notification_id (Primary Key)
- recipient_id (Foreign Key → Users.user_id)
- notification_type
- notification_content
- created_at
- status

---

### Relationships
- One parent may be linked to multiple children.
- One child may have multiple guardians.
- One teacher may create multiple attendance and activity records.
- One child may have multiple attendance records.
- One child may have multiple activity reports.
- One user may send and receive multiple messages.
- One user may receive multiple notifications.

---

### Constraints
- User email addresses must be unique.
- Passwords must be stored in hashed format.
- Foreign key references must maintain referential integrity.
- Attendance records cannot exist without valid child and teacher references.
- Messages require valid sender and receiver references.
- Cascade deletion is applied to dependent child-related records where appropriate.

---

### c. Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask Framework)
- **Database:** MySQL
- **Version Control:** Git/GitHub

#### Technology Justification
Python was selected for backend development due to its readability, maintainability, and extensive ecosystem for web development. Flask provides lightweight yet scalable architecture for building RESTful APIs and backend logic efficiently. MySQL was chosen due to its reliability, relational structure, and compatibility with structured application data.

---

### d. User Interface Design

The user interface is designed to be intuitive, modern, and role-based. It includes:

- Login/Register Interface
- Parent Dashboard
- Teacher Dashboard
- Administrator Dashboard
- Child Profile Management Screen
- Attendance Management Interface
- Messaging Interface
- Notification Center
- Reporting Dashboard

The design prioritizes accessibility, responsive layout, and user-friendly navigation.

---

### e. Security Measures

- Secure authentication and authorization mechanisms.
- Password hashing before database storage.
- Role-based access control (RBAC).
- Session timeout for inactive users.
- Input validation and sanitization.
- Protection against unauthorized data access.
- Regular database backup procedures.
- Secure communication between client and server.

---
