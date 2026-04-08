from django.contrib import admin
from .models import Subject, Class, Enrollment, TeacherSubjectAssignment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'class_teacher', 'academic_year']
    list_filter = ['name', 'section', 'academic_year']
    search_fields = ['name', 'section']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_enrolled', 'roll_number', 'status', 'enrollment_date']
    list_filter = ['status', 'class_enrolled']
    search_fields = ['student__username', 'student__first_name', 'roll_number']


@admin.register(TeacherSubjectAssignment)
class TeacherSubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'class_assigned', 'created_at']
    list_filter = ['class_assigned', 'subject']
