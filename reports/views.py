from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.db.models import Count, Q
from datetime import datetime
import csv
from .models import AttendanceReport
from .serializers import AttendanceReportSerializer, ReportGenerateSerializer
from attendance.models import Attendance, Course


class AttendanceReportListView(generics.ListAPIView):
    """
    List all generated reports
    GET /api/reports/
    """
    serializer_class = AttendanceReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = AttendanceReport.objects.select_related('generated_by', 'course')
        
        # Teachers only see reports they generated
        if user.role == 'teacher':
            queryset = queryset.filter(generated_by=user)
        
        # Students cannot view reports
        elif user.role == 'student':
            queryset = queryset.none()
        
        return queryset.order_by('-created_at')


class AttendanceReportDetailView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a report
    GET/DELETE /api/reports/<id>/
    """
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = AttendanceReport.objects.all()
        
        if user.role == 'teacher':
            queryset = queryset.filter(generated_by=user)
        elif user.role == 'student':
            queryset = queryset.none()
        
        return queryset


class GenerateReportView(APIView):
    """
    Generate attendance report and download as CSV
    POST /api/reports/generate/
    
    Request body:
    {
        "course_id": 1 (optional - leave blank for all courses),
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "report_type": "monthly",
        "format": "csv"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Only admins and teachers can generate reports
        if request.user.role == 'student':
            return Response({
                'error': 'Students cannot generate reports'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReportGenerateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract validated data
        course_id = serializer.validated_data.get('course_id')
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        report_type = serializer.validated_data['report_type']
        report_format = serializer.validated_data['format']
        
        # Build query
        queryset = Attendance.objects.select_related('user', 'course', 'marked_by')
        queryset = queryset.filter(date__range=[start_date, end_date])
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        # Teachers can only generate reports for their courses
        if request.user.role == 'teacher':
            queryset = queryset.filter(course__teacher=request.user)
        
        queryset = queryset.order_by('date', 'course', 'user')
        
        # Generate CSV response
        if report_format == 'csv':
            return self._generate_csv(queryset, start_date, end_date)
        
        return Response({
            'error': 'Only CSV format is currently supported'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def _generate_csv(self, queryset, start_date, end_date):
        """Generate CSV file from attendance queryset"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendance_report_{start_date}_{end_date}.csv"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow([
            'Date',
            'Course Code',
            'Course Name',
            'Student Username',
            'Student Name',
            'Status',
            'Remarks',
            'Marked By'
        ])
        
        # Write data rows
        for attendance in queryset:
            writer.writerow([
                attendance.date.strftime('%Y-%m-%d'),
                attendance.course.code,
                attendance.course.name,
                attendance.user.username,
                attendance.user.get_full_name() or attendance.user.username,
                attendance.get_status_display(),
                attendance.remarks or '',
                attendance.marked_by.get_full_name() if attendance.marked_by else 'N/A'
            ])
        
        # Write summary
        writer.writerow([])
        writer.writerow(['SUMMARY'])
        writer.writerow(['Total Records', queryset.count()])
        writer.writerow(['Present', queryset.filter(status='present').count()])
        writer.writerow(['Absent', queryset.filter(status='absent').count()])
        writer.writerow(['Late', queryset.filter(status='late').count()])
        writer.writerow(['Excused', queryset.filter(status='excused').count()])
        
        return response


class DailySummaryView(APIView):
    """
    Get daily attendance summary
    GET /api/reports/daily-summary/?date=2025-01-15&course_id=1
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role == 'student':
            return Response({
                'error': 'Students cannot view summary reports'
            }, status=status.HTTP_403_FORBIDDEN)
        
        date_str = request.query_params.get('date')
        course_id = request.query_params.get('course_id')
        
        if not date_str:
            return Response({
                'error': 'date parameter is required (format: YYYY-MM-DD)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Build query
        queryset = Attendance.objects.filter(date=date)
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        if request.user.role == 'teacher':
            queryset = queryset.filter(course__teacher=request.user)
        
        # Calculate summary
        total = queryset.count()
        present = queryset.filter(status='present').count()
        absent = queryset.filter(status='absent').count()
        late = queryset.filter(status='late').count()
        excused = queryset.filter(status='excused').count()
        
        attendance_rate = (present / total * 100) if total > 0 else 0
        
        return Response({
            'date': date,
            'total_students': total,
            'present': present,
            'absent': absent,
            'late': late,
            'excused': excused,
            'attendance_rate': round(attendance_rate, 2)
        })


class MonthlySummaryView(APIView):
    """
    Get monthly attendance summary
    GET /api/reports/monthly-summary/?year=2025&month=1&course_id=1
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role == 'student':
            return Response({
                'error': 'Students cannot view summary reports'
            }, status=status.HTTP_403_FORBIDDEN)
        
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        course_id = request.query_params.get('course_id')
        
        if not year or not month:
            return Response({
                'error': 'year and month parameters are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response({
                'error': 'Invalid year or month'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Build query
        queryset = Attendance.objects.filter(
            date__year=year,
            date__month=month
        )
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        if request.user.role == 'teacher':
            queryset = queryset.filter(course__teacher=request.user)
        
        # Calculate summary
        total = queryset.count()
        present = queryset.filter(status='present').count()
        absent = queryset.filter(status='absent').count()
        late = queryset.filter(status='late').count()
        excused = queryset.filter(status='excused').count()
        
        attendance_rate = (present / total * 100) if total > 0 else 0
        
        # Get unique days with attendance
        unique_days = queryset.values('date').distinct().count()
        
        return Response({
            'year': year,
            'month': month,
            'total_records': total,
            'unique_days': unique_days,
            'present': present,
            'absent': absent,
            'late': late,
            'excused': excused,
            'attendance_rate': round(attendance_rate, 2)
        })