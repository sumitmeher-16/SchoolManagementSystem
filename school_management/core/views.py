from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from users.models import User, Notification
from academics.models import Class, Subject, Enrollment, TeacherSubjectAssignment
from attendance.models import Attendance, AttendanceSummary
from results.models import Result, Exam, StudentPerformance
from fees.models import FeePayment, FeeStructure, FeeCategory


class LoginView(TemplateView):
    template_name = 'core/login.html'
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    
    if user.is_admin_user:
        return admin_dashboard(request)
    elif user.is_teacher:
        return teacher_dashboard(request)
    else:
        return student_dashboard(request)


def admin_dashboard(request):
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    
    active_enrollments = Enrollment.objects.filter(status='active').count()
    
    pending_fees = FeePayment.objects.filter(status='pending').count()
    total_fee_collection = FeePayment.objects.filter(status='paid').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(date=today).count()
    
    recent_students = User.objects.filter(role='student').order_by('-date_joined')[:5]
    recent_teachers = User.objects.filter(role='teacher').order_by('-date_joined')[:5]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'active_enrollments': active_enrollments,
        'pending_fees': pending_fees,
        'total_fee_collection': total_fee_collection,
        'today_attendance': today_attendance,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
    }
    return render(request, 'core/dashboard.html', context)


def teacher_dashboard(request):
    teacher = request.user
    
    assigned_classes = Class.objects.filter(class_teacher=teacher)
    subject_assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher)
    
    total_students = Enrollment.objects.filter(
        class_enrolled__in=assigned_classes,
        status='active'
    ).count()
    
    today = timezone.now().date()
    today_classes = assigned_classes.filter(attendance_records__date=today).distinct()
    
    recent_results = Result.objects.filter(
        exam__created_by=teacher
    ).select_related('student', 'exam').order_by('-created_at')[:5]
    
    context = {
        'assigned_classes': assigned_classes,
        'subject_assignments': subject_assignments,
        'total_students': total_students,
        'today_classes': today_classes,
        'recent_results': recent_results,
    }
    return render(request, 'core/teacher_dashboard.html', context)


def student_dashboard(request):
    student = request.user
    
    enrollments = Enrollment.objects.filter(student=student, status='active')
    current_class = enrollments.first().class_enrolled if enrollments.exists() else None
    
    recent_attendance = Attendance.objects.filter(
        student=student
    ).order_by('-date')[:30]
    
    attendance_percentage = 0
    if recent_attendance.exists():
        total = recent_attendance.count()
        present = recent_attendance.filter(status='present').count()
        attendance_percentage = round((present / total) * 100, 2)
    
    recent_results = Result.objects.filter(
        student=student
    ).select_related('exam').order_by('-created_at')[:5]
    
    pending_fees = FeePayment.objects.filter(student=student, status='pending')
    total_pending = pending_fees.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'current_class': current_class,
        'enrollments': enrollments,
        'attendance_percentage': attendance_percentage,
        'recent_attendance': recent_attendance,
        'recent_results': recent_results,
        'pending_fees': pending_fees,
        'total_pending': total_pending,
    }
    return render(request, 'core/student_dashboard.html', context)


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)[:50]
    return render(request, 'core/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, pk):
    notification = Notification.objects.get(pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


@login_required
def profile(request):
    return render(request, 'core/profile.html')


def charts_data(request):
    if not request.user.is_admin_user:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    students_by_class = Enrollment.objects.filter(status='active').values(
        'class_enrolled__name'
    ).annotate(count=Count('id'))
    
    attendance_by_month = AttendanceSummary.objects.filter(
        year=timezone.now().year
    ).values('month').annotate(
        avg_attendance=Avg('present_days') / Avg('total_days') * 100
    )
    
    fee_collection_monthly = FeePayment.objects.filter(
        status='paid',
        payment_date__year=timezone.now().year
    ).extra(
        select={'month': "strftime('%%m', payment_date)"}
    ).values('month').annotate(total=Sum('amount'))
    
    return JsonResponse({
        'students_by_class': list(students_by_class),
        'attendance_by_month': list(attendance_by_month),
        'fee_collection_monthly': list(fee_collection_monthly),
    })
