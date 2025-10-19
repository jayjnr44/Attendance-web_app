#registering a teacher user
"""POST http://127.0.0.1:8000/api/auth/register/"""
{
  "username": "teacher1",
  "email": "teacher1@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "teacher",
  "phone": "+233123456789"
}

{
  "message": "User registered successfully",
  "user": {
    "id": 2,
    "username": "teacher1",
    "email": "teacher1@example.com",
    "role": "teacher",
    #...
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1...",
    "access": "eyJ0eXAiOiJKV1..."
  }
}

#Login request
"""http://127.0.0.1:8000/api/auth/login/"""
{
  "username": "teacher1",
  "password": "SecurePass123!"
}


#3️⃣ Create a Course (Admin Only)
POST http://127.0.0.1:8000/api/courses/

Headers:
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Content-Type: application/json
Body (JSON):
json{
  "code": "MATH101",
  "name": "Introduction to Mathematics",
  "description": "Basic mathematics course",
  "teacher": 2,
  "is_active": true
}


4️⃣ Enroll Students in Course
PUT http://127.0.0.1:8000/api/courses/1/
Headers:
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Body (JSON):
json{
  "code": "MATH101",
  "name": "Introduction to Mathematics",
  "teacher": 2,
  "students": [3, 4, 5]
}

5️⃣ Mark Attendance
POST http://127.0.0.1:8000/api/attendance/
Headers:
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Body (JSON):
json{
  "user": 3,
  "course": 1,
  "date": "2025-10-18",
  "status": "present",
  "remarks": "On time"
}

6️⃣ Bulk Mark Attendance
POST http://127.0.0.1:8000/api/attendance/bulk/
Body (JSON):
json{
  "course": 1,
  "date": "2025-10-18",
  "attendance_data": [
    {"user_id": 3, "status": "present", "remarks": ""},
    {"user_id": 4, "status": "absent", "remarks": "Sick"},
    {"user_id": 5, "status": "late", "remarks": "Traffic"}
  ]
}

7️⃣ Get Attendance Statistics
GET http://127.0.0.1:8000/api/attendance/stats/?user_id=3&course_id=1
Headers:
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE

8️⃣ Generate CSV Report
POST http://127.0.0.1:8000/api/reports/generate/
Headers:
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
Body (JSON):
json{
  "course_id": 1,
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "report_type": "monthly",
  "format": "csv"
}
Response: Downloads a CSV file!