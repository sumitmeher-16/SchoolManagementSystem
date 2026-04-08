from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('detail/<int:pk>/', views.student_detail, name='student_detail'),
    path('my-profile/', views.student_profile, name='student_profile'),
    path('export/csv/', views.export_students_csv, name='export_students_csv'),
]
