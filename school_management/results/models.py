from django.db import models
from django.conf import settings
from academics.models import Class, Subject


class Exam(models.Model):
    EXAM_TYPES = (
        ('weekly', 'Weekly Test'),
        ('monthly', 'Monthly Test'),
        ('term', 'Term Exam'),
        ('final', 'Final Exam'),
    )
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    class_enrolled = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='exams'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='exams'
    )
    date = models.DateField()
    total_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=33)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_exams'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} - {self.class_enrolled.name} - {self.subject.name}"


class Result(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results',
        limit_choices_to={'role': 'student'}
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['-created_at']
    
    @property
    def percentage(self):
        return round((self.marks_obtained / self.exam.total_marks) * 100, 2)
    
    @property
    def status(self):
        return 'Pass' if self.marks_obtained >= self.exam.passing_marks else 'Fail'
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam.name}: {self.marks_obtained}"


class StudentPerformance(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='performances',
        limit_choices_to={'role': 'student'}
    )
    class_enrolled = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='student_performances'
    )
    term = models.CharField(max_length=20)
    total_marks = models.IntegerField(default=0)
    obtained_marks = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-total_marks']
        unique_together = ['student', 'class_enrolled', 'term']
    
    @property
    def percentage(self):
        if self.total_marks == 0:
            return 0
        return round((self.obtained_marks / self.total_marks) * 100, 2)
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.term}"
