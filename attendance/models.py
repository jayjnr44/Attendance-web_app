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