from django.urls import path
from .views import (
    CourseListCreateView,
    CourseDetailView,
    AttendanceListCreateView,
    AttendanceDetailView,
    BulkAttendanceView,
    AttendanceStatsView,
)

app_name = 'attendance'

urlpatterns = [
    # Courses
    path('courses/', CourseListCreateView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    
    # Attendance
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance_list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance_detail'),
    path('attendance/bulk/', BulkAttendanceView.as_view(), name='attendance_bulk'),
    path('attendance/stats/', AttendanceStatsView.as_view(), name='attendance_stats'),
]