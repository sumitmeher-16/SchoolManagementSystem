from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('update/<int:pk>/', views.user_update, name='user_update'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('detail/<int:pk>/', views.user_detail, name='user_detail'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('check-username/', views.check_username, name='check_username'),
]
