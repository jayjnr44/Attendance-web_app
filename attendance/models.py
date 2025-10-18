from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Course(models.Model):
    """
    Represents a course/class that students enroll in
    """
    name = models.CharField(
        max_length=100,
        help_text="Course name (e.g., 'Mathematics 101')"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique course code (e.g., 'MATH101')"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='courses_taught',
        help_text="Teacher assigned to this course"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'student'},
        related_name='courses_enrolled',
        blank=True,
        help_text="Students enrolled in this course"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive courses won't appear in attendance marking"
    )
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_student_count(self):
        return self.students.count()
    
    def clean(self):
        """Validate model data before saving"""
        super().clean()
        if self.teacher and self.teacher.role != 'teacher':
            raise ValidationError("Course teacher must have 'teacher' role")


class Attendance(models.Model):
    """
    Records individual attendance entries
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='attendance_records',
        help_text="Student whose attendance is being recorded"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        help_text="Course for which attendance is being marked"
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Date of attendance"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='present'
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes (e.g., reason for absence)"
    )
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_marked',
        help_text="Teacher/admin who marked this attendance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'date', 'course')
        ordering = ['-date', 'course', 'user']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['date', 'course']),
            models.Index(fields=['user', 'date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.course.code} - {self.date} ({self.get_status_display()})"
    
    def clean(self):
        """Validate model data before saving"""
        super().clean()
        if self.user and self.user.role != 'student':
            raise ValidationError("Attendance can only be marked for students")
        if self.marked_by and self.marked_by.role not in ['teacher', 'admin']:
            raise ValidationError("Attendance can only be marked by teachers or admins")