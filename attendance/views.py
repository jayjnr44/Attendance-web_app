from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from datetime import datetime, timedelta
from rest_framework.exceptions import PermissionDenied
from .models import Course, Attendance
from .serializers import (
    CourseSerializer,
    CourseListSerializer,
    AttendanceSerializer,
    BulkAttendanceSerializer,
    AttendanceStatsSerializer
)
from .permissions import IsAdminOrTeacher, IsAdminOrTeacherOrOwner


class CourseListCreateView(generics.ListCreateAPIView):
    """
    List all courses or create new course
    GET/POST /api/courses/
    """
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseListSerializer
        return CourseSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.filter(is_active=True)
        
        # Teachers see only their courses
        if user.role == 'teacher':
            queryset = queryset.filter(teacher=user)
        
        # Students see only enrolled courses
        elif user.role == 'student':
            queryset = queryset.filter(students=user)
        
        return queryset.order_by('code')
    
    def perform_create(self, serializer):
        # Only admins can create courses
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can create courses")
        serializer.save()


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a course
    GET/PUT/DELETE /api/courses/<id>/
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        # Only admins can update courses
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can update courses")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only admins can delete courses
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can delete courses")
        instance.delete()


class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    List attendance records or mark new attendance
    GET/POST /api/attendance/
    """
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.select_related('user', 'course', 'marked_by')
        
        # Filter by role
        if user.role == 'student':
            queryset = queryset.filter(user=user)
        elif user.role == 'teacher':
            queryset = queryset.filter(course__teacher=user)
        
        # Filter by query params
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset.order_by('-date', 'course')
    
    def perform_create(self, serializer):
        # Only teachers and admins can mark attendance
        if self.request.user.role == 'student':
            raise PermissionDenied("Students cannot mark attendance")
        serializer.save(marked_by=self.request.user)


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete attendance record
    GET/PUT/DELETE /api/attendance/<id>/
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.all()
        
        if user.role == 'student':
            queryset = queryset.filter(user=user)
        elif user.role == 'teacher':
            queryset = queryset.filter(course__teacher=user)
        
        return queryset
    
    def perform_update(self, serializer):
        if self.request.user.role == 'student':
            raise PermissionDenied("Students cannot update attendance")
        serializer.save(marked_by=self.request.user)
    
    def perform_destroy(self, instance):
        if self.request.user.role not in ['admin', 'teacher']:
            raise PermissionDenied("Only teachers and admins can delete attendance")
        instance.delete()


class BulkAttendanceView(APIView):
    """
    Mark attendance for multiple students at once
    POST /api/attendance/bulk/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.role == 'student':
            return Response({
                'error': 'Students cannot mark attendance'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BulkAttendanceSerializer(data=request.data)
        
        if serializer.is_valid():
            course = serializer.validated_data['course']
            date = serializer.validated_data['date']
            attendance_data = serializer.validated_data['attendance_data']
            
            created_count = 0
            updated_count = 0
            errors = []
            
            for item in attendance_data:
                try:
                    user_id = item['user_id']
                    status_value = item['status']
                    remarks = item.get('remarks', '')
                    
                    # Check if attendance already exists
                    attendance, created = Attendance.objects.update_or_create(
                        user_id=user_id,
                        course=course,
                        date=date,
                        defaults={
                            'status': status_value,
                            'remarks': remarks,
                            'marked_by': request.user
                        }
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                
                except Exception as e:
                    errors.append({
                        'user_id': user_id,
                        'error': str(e)
                    })
            
            return Response({
                'message': 'Bulk attendance processed',
                'created': created_count,
                'updated': updated_count,
                'errors': errors
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceStatsView(APIView):
    """
    Get attendance statistics for a student
    GET /api/attendance/stats/?user_id=<id>&course_id=<id>
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user_id = request.query_params.get('user_id')
        course_id = request.query_params.get('course_id')
        
        if not user_id:
            user_id = request.user.id if request.user.role == 'student' else None
        
        if not user_id:
            return Response({
                'error': 'user_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Build query
        queryset = Attendance.objects.filter(user_id=user_id)
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        # Calculate stats
        total_days = queryset.count()
        present_count = queryset.filter(status='present').count()
        absent_count = queryset.filter(status='absent').count()
        late_count = queryset.filter(status='late').count()
        excused_count = queryset.filter(status='excused').count()
        
        attendance_percentage = (present_count / total_days * 100) if total_days > 0 else 0
        
        stats = {
            'total_days': total_days,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'excused_count': excused_count,
            'attendance_percentage': round(attendance_percentage, 2)
        }
        
        serializer = AttendanceStatsSerializer(stats)
        return Response(serializer.data)