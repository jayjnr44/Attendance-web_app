# 📚 Attendance Management System

A comprehensive REST API built with Django and Django REST Framework for managing student attendance, courses, and generating reports. This system provides role-based access control for administrators, teachers, and students.

![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![DRF](https://img.shields.io/badge/DRF-3.14+-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **Attendance Management System** is a robust backend API solution designed to streamline the process of tracking student attendance in educational institutions. It provides a complete suite of features for managing users, courses, attendance records, and generating comprehensive reports.

### What Problem Does It Solve?

Traditional attendance tracking methods are:
- Time-consuming and error-prone
- Difficult to analyze and generate reports
- Lack centralized access for students and parents
- Hard to maintain historical records

This system solves these problems by providing:
- ✅ Digital attendance marking (single and bulk)
- ✅ Real-time attendance statistics
- ✅ Automated report generation
- ✅ Role-based access control
- ✅ Secure JWT authentication
- ✅ RESTful API for easy integration

---

## ✨ Features

### 🔐 Authentication & Authorization
- User registration with email verification
- JWT-based authentication (access & refresh tokens)
- Role-based access control (Admin, Teacher, Student)
- Secure password management with change password functionality
- User profile management

### 👥 User Management
- Three user roles with different permissions:
  - **Admin**: Full system access, can manage all resources
  - **Teacher**: Can manage assigned courses and mark attendance
  - **Student**: Can view personal attendance records
- User listing and filtering by role
- Profile updates

### 📚 Course Management
- Create, read, update, and delete courses
- Assign teachers to courses
- Enroll students in courses
- Track course status (active/inactive)
- View student enrollment counts

### ✅ Attendance Tracking
- Single student attendance marking
- Bulk attendance marking for efficiency
- Four attendance statuses:
  - **Present**: Student attended
  - **Absent**: Student did not attend
  - **Late**: Student arrived late
  - **Excused**: Student has valid excuse
- Add remarks/notes to attendance records
- Update and delete attendance records
- Filter attendance by:
  - Date
  - Course
  - Student
  - Status

### 📊 Reports & Analytics
- Attendance statistics per student
- Attendance percentage calculations
- Daily attendance summaries
- Monthly attendance summaries
- CSV report generation and export
- Customizable date ranges for reports
- Course-specific or system-wide reports

---

## 🛠️ Tech Stack

### Backend
- **Django 5.2.7** - High-level Python web framework
- **Django REST Framework 3.14+** - Powerful toolkit for building Web APIs
- **djangorestframework-simplejwt** - JSON Web Token authentication

### Database
- **SQLite** (Development) - Lightweight, file-based database
- **PostgreSQL** (Production - Recommended) - Robust, scalable database

### Authentication
- **JWT (JSON Web Tokens)** - Secure, stateless authentication

### Other Tools
- **Python 3.8+** - Programming language
- **pip** - Package installer for Python
- **virtualenv** - Virtual environment management

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  (Web App / Mobile App / API Testing Tools)              │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/HTTPS + JWT
                   ▼
┌─────────────────────────────────────────────────────────┐
│                  API Gateway                             │
│         Django REST Framework Views                      │
│  ┌─────────────┬──────────────┬──────────────┐         │
│  │   Auth API  │ Attendance   │  Reports     │         │
│  │             │   API        │   API        │         │
│  └─────────────┴──────────────┴──────────────┘         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│                Business Logic Layer                      │
│              Serializers & Permissions                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│              Django ORM + Models                         │
│  ┌──────────┬─────────────┬──────────┬────────────┐    │
│  │  User    │   Course    │Attendance│   Report   │    │
│  │  Model   │   Model     │  Model   │   Model    │    │
│  └──────────┴─────────────┴──────────┴────────────┘    │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│                Database (SQLite/PostgreSQL)              │
└─────────────────────────────────────────────────────────┘
```

---

## 📥 Installation

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)
- A code editor (VS Code, PyCharm, etc.)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/attendance-management-system.git
cd attendance-management-system
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install django==5.2.7
pip install djangorestframework
pip install djangorestframework-simplejwt
```

### Step 4: Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

**Important:** Never commit `.env` to version control!

### Step 5: Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin`
- Email: `admin@example.com`
- Password: (choose a secure password)
- **Role: `admin`** (important!)

### Step 7: Load Sample Data (Optional)

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from attendance.models import Course

User = get_user_model()

# Create teacher
teacher = User.objects.create_user(
    username='teacher1',
    email='teacher@school.com',
    password='teacher123',
    role='teacher',
    first_name='John',
    last_name='Smith'
)

# Create students
for i in range(1, 6):
    User.objects.create_user(
        username=f'student{i}',
        email=f'student{i}@school.com',
        password='student123',
        role='student',
        first_name=f'Student',
        last_name=f'{i}'
    )

print("Sample users created successfully!")
exit()
```

---

## ⚙️ Configuration

### Settings Overview

Key configurations in `attendance_webapp/settings.py`:

```python
# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Timezone
TIME_ZONE = 'Africa/Accra'  # Change to your timezone
USE_TZ = True

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 🚀 Running the Application

### Development Server

```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### Access Points

- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **API Root**: `http://127.0.0.1:8000/api/`
- **API Documentation**: `http://127.0.0.1:8000/api/` (Browsable API)

### Running on Custom Port

```bash
python manage.py runserver 8080
```

### Running on Network (accessible from other devices)

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 📚 API Documentation

### Base URL

```
http://127.0.0.1:8000/api/
```

### Authentication

All endpoints (except register and login) require JWT authentication:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### API Endpoints Overview

#### 🔐 Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | ❌ |
| POST | `/api/auth/login/` | Login and get tokens | ❌ |
| POST | `/api/auth/token/refresh/` | Refresh access token | ❌ |
| GET/PUT | `/api/auth/profile/` | View/update profile | ✅ |
| POST | `/api/auth/change-password/` | Change password | ✅ |
| GET | `/api/users/` | List all users | ✅ |

#### 📚 Courses

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/courses/` | List courses | ✅ | All |
| POST | `/api/courses/` | Create course | ✅ | Admin |
| GET | `/api/courses/{id}/` | Get course details | ✅ | All |
| PUT | `/api/courses/{id}/` | Update course | ✅ | Admin |
| DELETE | `/api/courses/{id}/` | Delete course | ✅ | Admin |

#### ✅ Attendance

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/attendance/` | List attendance | ✅ | All |
| POST | `/api/attendance/` | Mark attendance | ✅ | Teacher/Admin |
| GET | `/api/attendance/{id}/` | Get attendance | ✅ | All |
| PUT | `/api/attendance/{id}/` | Update attendance | ✅ | Teacher/Admin |
| DELETE | `/api/attendance/{id}/` | Delete attendance | ✅ | Teacher/Admin |
| POST | `/api/attendance/bulk/` | Bulk mark | ✅ | Teacher/Admin |
| GET | `/api/attendance/stats/` | Get statistics | ✅ | All |

#### 📊 Reports

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/reports/` | List reports | ✅ | Teacher/Admin |
| POST | `/api/reports/generate/` | Generate CSV | ✅ | Teacher/Admin |
| GET | `/api/reports/daily-summary/` | Daily summary | ✅ | Teacher/Admin |
| GET | `/api/reports/monthly-summary/` | Monthly summary | ✅ | Teacher/Admin |

---

## 💡 Usage Examples

### 1. Register a New User

**Request:**
```bash
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "username": "teacher1",
  "email": "teacher1@school.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "teacher",
  "phone": "+233123456789"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 2,
    "username": "teacher1",
    "email": "teacher1@school.com",
    "role": "teacher"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
    "access": "eyJ0eXAiOiJKV1QiLCJh..."
  }
}
```

### 2. Login

**Request:**
```bash
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "teacher1",
  "password": "SecurePass123!"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 2,
    "username": "teacher1",
    "role": "teacher"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
    "access": "eyJ0eXAiOiJKV1QiLCJh..."
  }
}
```

### 3. Create a Course

**Request:**
```bash
POST http://127.0.0.1:8000/api/courses/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "code": "MATH101",
  "name": "Introduction to Mathematics",
  "description": "Basic math course",
  "teacher": 2,
  "students": [3, 4, 5],
  "is_active": true
}
```

### 4. Mark Attendance

**Request:**
```bash
POST http://127.0.0.1:8000/api/attendance/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "user": 3,
  "course": 1,
  "date": "2025-10-19",
  "status": "present",
  "remarks": "Excellent participation"
}
```

### 5. Bulk Mark Attendance

**Request:**
```bash
POST http://127.0.0.1:8000/api/attendance/bulk/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "course": 1,
  "date": "2025-10-19",
  "attendance_data": [
    {"user_id": 3, "status": "present", "remarks": ""},
    {"user_id": 4, "status": "absent", "remarks": "Sick"},
    {"user_id": 5, "status": "late", "remarks": "Traffic"}
  ]
}
```

### 6. Get Attendance Statistics

**Request:**
```bash
GET http://127.0.0.1:8000/api/attendance/stats/?user_id=3&course_id=1
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "total_days": 20,
  "present_count": 18,
  "absent_count": 1,
  "late_count": 1,
  "excused_count": 0,
  "attendance_percentage": 90.0
}
```

### 7. Generate CSV Report

**Request:**
```bash
POST http://127.0.0.1:8000/api/reports/generate/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "course_id": 1,
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "report_type": "monthly",
  "format": "csv"
}
```

**Response:** Downloads a CSV file with attendance data

---

## 📁 Project Structure

```
attendance-management-system/
│
├── attendance_webapp/          # Main project directory
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
│
├── users/                      # User management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py               # Admin configuration
│   ├── apps.py
│   ├── models.py              # CustomUser model
│   ├── serializers.py         # User serializers
│   ├── views.py               # Authentication views
│   ├── urls.py                # User URL patterns
│   └── tests.py
│
├── attendance/                 # Attendance management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py               # Course & Attendance admin
│   ├── apps.py
│   ├── models.py              # Course & Attendance models
│   ├── serializers.py         # Attendance serializers
│   ├── views.py               # Attendance views
│   ├── permissions.py         # Custom permissions
│   ├── urls.py                # Attendance URL patterns
│   └── tests.py
│
├── reports/                    # Reporting app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # AttendanceReport model
│   ├── serializers.py         # Report serializers
│   ├── views.py               # Report generation views
│   ├── urls.py                # Report URL patterns
│   └── tests.py
│
├── media/                      # User-uploaded files
│   └── reports/               # Generated reports
│
├── .env                        # Environment variables (not in git)
├── .gitignore                 # Git ignore file
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── db.sqlite3                 # Database (not in git)
```

---

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Run Tests for Specific App

```bash
python manage.py test users
python manage.py test attendance
python manage.py test reports
```

### Run Tests with Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Manual API Testing

Use tools like:
- **Postman** - Full-featured API testing
- **Thunder Client** - VS Code extension
- **cURL** - Command-line testing
- **DRF Browsable API** - Built-in browser interface

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Module not found" Error

**Solution:**
```bash
pip install -r requirements.txt
```

#### 2. "No such table" Error

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. "Authentication credentials were not provided"

**Solution:** Add Authorization header with Bearer token

#### 4. "You do not have permission"

**Solution:** Check user role matches required permission

#### 5. Port Already in Use

**Solution:**
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9
```

#### 6. Token Expired

**Solution:** Use refresh token endpoint to get new access token:
```bash
POST /api/auth/token/refresh/
{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Write meaningful commit messages
- Add docstrings to functions and classes
- Write tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@jayjnr44](https://github.com/jayjnr44/Attendance-web_app.git)
- Email: jayycrypt@gmail.com

---

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- JWT Authentication
- ALX Software Engineering Program

---

## 📞 Support

For support, email support@example.com or create an issue in the GitHub repository.

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] Email notifications for absences
- [ ] QR code attendance scanning
- [ ] Mobile app (Flutter/React Native)
- [ ] Advanced analytics dashboard
- [ ] Export to Excel/PDF
- [ ] Facial recognition attendance
- [ ] Parent portal access
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Calendar integration

---

**⭐ If you find this project useful, please give it a star!**

---

*Last Updated: October 19, 2025*