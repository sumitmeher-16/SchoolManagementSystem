from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='api-user')
router.register(r'students-list', views.StudentViewSet, basename='api-student')
router.register(r'teachers-list', views.TeacherViewSet, basename='api-teacher')
router.register(r'subjects', views.SubjectViewSet, basename='api-subject')
router.register(r'classes', views.ClassViewSet, basename='api-class')
router.register(r'enrollments', views.EnrollmentViewSet, basename='api-enrollment')
router.register(r'attendance', views.AttendanceViewSet, basename='api-attendance')
router.register(r'exams', views.ExamViewSet, basename='api-exam')
router.register(r'results', views.ResultViewSet, basename='api-result')
router.register(r'fees', views.FeePaymentViewSet, basename='api-fee')

urlpatterns = [
    path('', include(router.urls)),
]
