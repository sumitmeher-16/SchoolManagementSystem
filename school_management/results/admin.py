from django.contrib import admin
from .models import Exam, Result, StudentPerformance


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'class_enrolled', 'subject', 'date', 'total_marks']
    list_filter = ['exam_type', 'class_enrolled', 'date']
    search_fields = ['name']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'percentage', 'status']
    list_filter = ['exam__class_enrolled']
    search_fields = ['student__username']


@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_enrolled', 'term', 'percentage', 'rank']
    list_filter = ['term', 'class_enrolled']
