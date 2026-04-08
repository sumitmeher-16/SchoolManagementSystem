from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/update/<int:pk>/', views.exam_update, name='exam_update'),
    path('exams/delete/<int:pk>/', views.exam_delete, name='exam_delete'),
    path('exams/<int:exam_id>/add-results/', views.add_results, name='add_results'),
    path('exams/<int:exam_id>/bulk-add-results/', views.bulk_add_results, name='bulk_add_results'),
    
    path('', views.result_list, name='result_list'),
    path('my-results/', views.student_results, name='student_results'),
    path('detail/<int:student_id>/', views.result_detail, name='result_detail'),
    path('report-card/<int:student_id>/', views.generate_report_card, name='generate_report_card'),
]
