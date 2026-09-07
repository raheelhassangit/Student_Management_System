# Student Management System

A web-based **Student Management System built with Django** for managing student records, courses, attendance, profiles, and academic reports.

The project provides an authenticated dashboard where users can manage students and courses, record daily attendance, view student profiles, and generate useful reports.

## Features

* User registration and authentication
* Student management

  * Add students
  * Edit student information
  * Delete students
  * View student profiles
  * Upload student images
* Course management

  * Add courses
  * View available courses
* Attendance management

  * Mark students as Present, Absent, or Leave
  * Select attendance by date
  * Prevent duplicate attendance records for the same student and date
* Dashboard

  * Total students
  * Total courses
  * Attendance rate
  * Recent student enrollments
  * Student distribution by class
* Reports

  * Student reports
  * Filter students by course and gender
  * Attendance reports for a selected date range
* Responsive user interface using Tailwind CSS
* Django messages for user feedback
* Protected views using Django authentication

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, Tailwind CSS
* **Database:** SQLite
* **Authentication:** Django Authentication System
* **Template Engine:** Django Templates
* **Image Handling:** Pillow / Django ImageField

## Project Structure

```text
Student_Management_System/
│
├── Student_Management_System/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│
├── students/
│   ├── models.py
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│
├── theme/
│   └── ...
│
├── manage.py
└── requirements.txt
```

## Database Models

The application currently uses three main models:

### Course

Stores information about academic courses, including:

* Course name
* Course code
* Duration
* Description
* Creation date

### Student

Stores student information such as:

* Username
* Name
* Father's name
* Roll number
* Class
* Date of birth
* Gender
* Course
* Phone
* Email
* Address
* Admission date
* Profile image

### Attendance

Stores daily attendance records for students.

Attendance statuses include:

* Present
* Absent
* Leave

Each student can have only one attendance record for a particular date.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/raheelhassangit/Student_Management_System.git
cd Student_Management_System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Authentication

The system uses Django's built-in authentication framework.

Users can:

* Register an account
* Log in
* Log out
* Access protected pages after authentication

Views such as student management, attendance, dashboard, and reports are protected with Django's `login_required` decorator.

## Attendance System

Attendance can be marked for a selected date. The system uses Django's `update_or_create()` functionality to create a new attendance record or update an existing record for the same student and date.

The database also enforces a unique student/date combination to prevent duplicate attendance records.

## Reports

The system provides reporting functionality including:

* Student statistics
* Gender distribution
* Course distribution
* Attendance statistics
* Attendance rate
* Date-range attendance reports

The dashboard also calculates recent enrollment statistics and overall attendance rates.

## Future Improvements

Possible future enhancements include:

* Django REST Framework API
* REST API authentication
* Role-based permissions
* PostgreSQL/MySQL support
* Advanced search and filtering
* Pagination
* Email notifications
* Export reports to PDF/Excel
* Improved automated testing
* Deployment with a production WSGI/ASGI setup

## Learning Goals

This project was built to practice and strengthen practical Django concepts including:

* Django project and app structure
* Models and relationships
* Migrations
* Django ORM
* ModelForms
* Authentication
* Login-required views
* CRUD operations
* File/image uploads
* Query filtering
* Aggregation with `Count`
* Database constraints
* Django templates
* Tailwind CSS
* Dashboard development
* Reporting and data analysis

## License

This project is intended for educational and portfolio purposes.

## Author

**Raheel Hassan**

GitHub: https://github.com/raheelhassangit
