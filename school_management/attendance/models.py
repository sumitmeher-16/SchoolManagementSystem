from django.db import models
from django.conf import settings
from academics.models import Class, Subject


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        limit_choices_to={'role': 'student'}
    )
    class_enrolled = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        null=True,
        blank=True
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendances'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'class_enrolled', 'date', 'subject']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.date} - {self.status}"


class AttendanceSummary(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_summaries',
        limit_choices_to={'role': 'student'}
    )
    class_enrolled = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='attendance_summaries'
    )
    month = models.IntegerField()
    year = models.IntegerField()
    total_days = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    late_days = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['student', 'class_enrolled', 'month', 'year']
        ordering = ['-year', '-month']
    
    @property
    def attendance_percentage(self):
        if self.total_days == 0:
            return 0
        return round((self.present_days / self.total_days) * 100, 2)
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.month}/{self.year}"
