from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
#Represents a course/class that students enroll in
class Course(models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Course name (e.g., MATHEMATIC 101)',
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        help_text='Unique course code (e.g., MTH101)',
    )
    Class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Class teacher'},
        related_name='courses taught by teacher',
        help_text='Class teacher assigned to this course',
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'student'},
        related_name='enrolled courses',
        blank=True,
        help_text='Students enrolled in this course',
    )
    description = models.TextField(blank=True, help_text='Optional course description', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,
                                    help_text='Inactive courses wont appear in attendance marking'
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f'{self.code} - {self.name}'
    
    def __get_student_count__(self):
        return self.students.count()
    
    def clean(self):
        super().clean()
        #validation fo teacher's role
        if self.Class_teacher and self.Class_teacher.role != 'Class teacher':
            raise ValidationError('Assigned Class teacher must have the role of "Class teacher".')
        
class Attendance(models.Model):
    """Records individual attendance entries"""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late','late'),
        ('excused', 'Excused'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to = {'role': 'student'},
        related_name='attendance_records',
        help_text='Students whose attendance is being recorded'
    )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        help_text='Courses for which attendance is being marked'
    )
    date = models.DateField(
        default=timezone.now,
        help_text='Date of attendance'
    )
    status= models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='present'
    )
    remarks = models.TextField(
        blank = True,
        null = True,
        help_text='Optional notes about student attendance'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        #Ensuring one attendance record per student per course per day
        unique_together = ('user', 'date', 'course')
        ordering = ['-date', 'course', 'user']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['date', 'course']),
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.course.code} - {self.date} ({self.get_status_display()})'
    
    def clean(self):
        super().clean()
        #validate that user is a student
        if self.user and self.user.role != 'student':
            raise ValidationError('Attendance can only be marked for students')
        
        #validate that marked_by is teacher or admin
        if  self.marked_by and self.marked_by.role not in ['Class teacher', 'admin']:
            raise ValidationError('Attendance can only be marked by Class teacher or admin')