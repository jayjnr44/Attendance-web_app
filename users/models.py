from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # extended user model with access control based on role of user

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('Class teacher', 'Class teacher'),
        ('student', 'Student'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text='Role of the user in the system',
    )
    email = models.EmailField(
        unique=True,
        help_text='Email address of the user(must be unique)',
    )
    phone = models.CharField(
    max_length=15,
    blank=True,
    null=True,
    help_text='Phone number of the user',
)
    date_joined= models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    @property
    def is_class_teacher(self):
        return self.role == 'Class teacher'
    @property
    def is_student(self):
        return self.role == 'student'