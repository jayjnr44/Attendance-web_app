from django.contrib import admin
from .models import Course, Attendance


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'teacher', 'get_student_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'teacher', 'created_at']
    search_fields = ['code', 'name', 'teacher__username']
    filter_horizontal = ['students']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'is_active')
        }),
        ('Assignment', {
            'fields': ('teacher', 'students')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'date', 'status', 'created_at']
    list_filter = ['status', 'date', 'course']
    search_fields = ['user__username', 'course__code', 'remarks']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('user', 'course', 'date', 'status', 'remarks')
        }),
        ('Metadata', {
            'fields': ('marked_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )