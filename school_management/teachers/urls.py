from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('create/', views.teacher_create, name='teacher_create'),
    path('update/<int:pk>/', views.teacher_update, name='teacher_update'),
    path('delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),
    path('detail/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('my-profile/', views.teacher_profile, name='teacher_profile'),
    path('assign-subject/', views.teacher_assign_subject, name='teacher_assign_subject'),
    path('export/csv/', views.export_teachers_csv, name='export_teachers_csv'),
]
