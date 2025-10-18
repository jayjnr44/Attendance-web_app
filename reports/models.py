from django.db import models
from django.conf import settings
from attendance.models import Course

class AttendaceReport(models.Model):
    """Stores metadata for generated attendance reports """

    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('custom', 'Custom Range Report'),
    ]

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role__in': ['admin', 'teacher']},
        related_name='reports_generated',
        help_text="User who generated this report"
    )
    course= models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Leave blank for all-courses report"
    )
    report_type =models.CharField(
        max_length=10,
        choices=REPORT_TYPE_CHOICES,
        default='daily',
    )
    start_date = models.DateField(help_text="Start date for the report")
    end_date = models.DateField(help_text="End date for the report")
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(
        upload_to='attendance_reports/%Y/%m/',
        blank=True,
        null=True,
        help_text="Path to the generated report file"
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = "Attendance Report"
        verbose_name_plural = "Attendance Reports"

    def __str__(self):
        course_name =  self.course.code if self.course else 'All Courses'
        return f'{self.get_report_type_display()}: {course_name} ({self.start_date} to {self.start_date} to {self.end_date})'
    
    
    

