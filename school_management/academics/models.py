from django.db import models
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Class(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_classes',
        limit_choices_to={'role': 'teacher'}
    )
    subjects = models.ManyToManyField(Subject, related_name='classes', blank=True)
    academic_year = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name', 'section']
        unique_together = ['name', 'section', 'academic_year']
    
    def __str__(self):
        return f"{self.name}-{self.section} ({self.academic_year})"
    
    @property
    def student_count(self):
        return self.enrollments.filter(status='active').count()


class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('transferred', 'Transferred'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
    )
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'student'}
    )
    class_enrolled = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    roll_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    enrollment_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ['student', 'class_enrolled']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_enrolled.name}-{self.class_enrolled.section}"


class TeacherSubjectAssignment(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subject_assignments',
        limit_choices_to={'role': 'teacher'}
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='teacher_assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher', 'subject', 'class_assigned']
    
    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.subject.name} ({self.class_assigned.name})"
