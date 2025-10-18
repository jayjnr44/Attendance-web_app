from rest_framework import serializers
from .models import AttendanceReport
from attendance.serializers import CourseListSerializer


class AttendanceReportSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance Report model
    """
    generated_by_name = serializers.CharField(
        source='generated_by.get_full_name', 
        read_only=True,
        allow_null=True
    )
    course_detail = CourseListSerializer(source='course', read_only=True)
    report_type_display = serializers.CharField(
        source='get_report_type_display', 
        read_only=True
    )
    
    class Meta:
        model = AttendanceReport
        fields = ['id', 'generated_by', 'generated_by_name', 'course', 
                  'course_detail', 'report_type', 'report_type_display',
                  'start_date', 'end_date', 'created_at', 'file_path']
        read_only_fields = ['id', 'created_at', 'file_path']
    
    def validate(self, attrs):
        """Ensure start_date is before end_date"""
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError({
                    "end_date": "End date must be after start date."
                })
        
        return attrs


class ReportGenerateSerializer(serializers.Serializer):
    """
    Serializer for report generation requests
    """
    course_id = serializers.IntegerField(required=False, allow_null=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    report_type = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly', 'custom'],
        default='custom'
    )
    format = serializers.ChoiceField(
        choices=['csv', 'excel', 'pdf'],
        default='csv'
    )
    
    def validate(self, attrs):
        """Validate date range"""
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date."
            })
        return attrs