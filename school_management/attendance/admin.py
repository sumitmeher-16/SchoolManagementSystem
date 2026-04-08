from django.contrib import admin
from .models import Attendance, AttendanceSummary


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_enrolled', 'date', 'status', 'marked_by']
    list_filter = ['status', 'date', 'class_enrolled']
    search_fields = ['student__username', 'student__first_name']


@admin.register(AttendanceSummary)
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_enrolled', 'month', 'year', 'attendance_percentage']
    list_filter = ['month', 'year']
