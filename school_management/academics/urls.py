from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('classes/', views.class_list, name='class_list'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/update/<int:pk>/', views.class_update, name='class_update'),
    path('classes/delete/<int:pk>/', views.class_delete, name='class_delete'),
    path('classes/detail/<int:pk>/', views.class_detail, name='class_detail'),
    
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/create/', views.subject_create, name='subject_create'),
    path('subjects/update/<int:pk>/', views.subject_update, name='subject_update'),
    path('subjects/delete/<int:pk>/', views.subject_delete, name='subject_delete'),
    
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enroll-student/', views.enroll_student, name='enroll_student'),
    path('enrollment/status/<int:pk>/', views.update_enrollment_status, name='update_enrollment_status'),
    
    path('api/class-students/<int:class_id>/', views.get_class_students, name='get_class_students'),
]
