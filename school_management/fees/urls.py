from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('categories/', views.fee_category_list, name='fee_category_list'),
    path('categories/create/', views.fee_category_create, name='fee_category_create'),
    path('categories/update/<int:pk>/', views.fee_category_update, name='fee_category_update'),
    
    path('structures/', views.fee_structure_list, name='fee_structure_list'),
    path('structures/create/', views.fee_structure_create, name='fee_structure_create'),
    path('structures/update/<int:pk>/', views.fee_structure_update, name='fee_structure_update'),
    
    path('collect/', views.collect_fee, name='collect_fee'),
    path('payments/', views.fee_payment_list, name='fee_payment_list'),
    path('payments/update/<int:pk>/', views.update_payment_status, name='update_payment_status'),
    path('payments/invoice/<int:pk>/', views.generate_fee_invoice, name='generate_fee_invoice'),
    
    path('report/', views.fee_report, name='fee_report'),
    path('my-fees/', views.student_fees, name='student_fees'),
]
