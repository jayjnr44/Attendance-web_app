from rest_framework import serializers
from .models import Course, Attendance
from users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model
    """
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    student_count = serializers.IntegerField(source='get_student_count', read_only=True)
    students_detail = UserSerializer(source='students', many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'teacher', 'teacher_name',
                  'students', 'students_detail', 'student_count', 'is_active', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_teacher(self, value):
        """Ensure teacher has the correct role"""
        if value.role != 'teacher':
            raise serializers.ValidationError("Selected user must have 'teacher' role.")
        return value
    
    def validate_code(self, value):
        """Ensure course code is unique (case-insensitive)"""
        code_upper = value.upper()
        instance = self.instance
        
        query = Course.objects.filter(code__iexact=code_upper)
        if instance:
            query = query.exclude(pk=instance.pk)
        
        if query.exists():
            raise serializers.ValidationError("A course with this code already exists.")
        return code_upper


class CourseListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing courses
    """
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    student_count = serializers.IntegerField(source='get_student_count', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'teacher', 'teacher_name', 
                  'student_count', 'is_active']


class AttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Attendance model with full details
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    marked_by_name = serializers.CharField(
        source='marked_by.get_full_name', 
        read_only=True, 
        allow_null=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'user_name', 'course', 'course_name', 'course_code',
                  'date', 'status', 'status_display', 'remarks', 'marked_by', 
                  'marked_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_user(self, value):
        """Ensure user is a student"""
        if value.role != 'student':
            raise serializers.ValidationError("Attendance can only be marked for students.")
        return value
    
    def validate(self, attrs):
        """Validate that student is enrolled in the course"""
        user = attrs.get('user')
        course = attrs.get('course')
        
        if user and course:
            if not course.students.filter(id=user.id).exists():
                raise serializers.ValidationError({
                    "user": f"{user.get_full_name()} is not enrolled in {course.code}."
                })
        
        return attrs


class BulkAttendanceSerializer(serializers.Serializer):
    """
    Serializer for marking attendance for multiple students at once
    """
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    date = serializers.DateField()
    attendance_data = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    def validate_attendance_data(self, value):
        """
        Validate attendance data structure
        Expected format: [{"user_id": 1, "status": "present", "remarks": ""}, ...]
        """
        if not value:
            raise serializers.ValidationError("Attendance data cannot be empty.")
        
        for item in value:
            if 'user_id' not in item or 'status' not in item:
                raise serializers.ValidationError(
                    "Each attendance record must have 'user_id' and 'status'."
                )
            
            # Validate status choices
            valid_statuses = ['present', 'absent', 'late', 'excused']
            if item['status'] not in valid_statuses:
                raise serializers.ValidationError(
                    f"Invalid status '{item['status']}'. Must be one of: {valid_statuses}"
                )
        
        return value


class AttendanceStatsSerializer(serializers.Serializer):
    """
    Serializer for attendance statistics
    """
    total_days = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    late_count = serializers.IntegerField()
    excused_count = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()