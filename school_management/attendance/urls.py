from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('bulk/', views.bulk_attendance, name='bulk_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('my-attendance/', views.student_attendance_view, name='student_attendance'),
    path('api/class-students/<int:class_id>/', views.get_class_students_attendance, name='get_class_students_attendance'),
]
