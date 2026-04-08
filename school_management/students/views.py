from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

from users.models import User
from academics.models import Class, Enrollment
from attendance.models import Attendance
from results.models import Result
from fees.models import FeePayment
from .forms import StudentForm


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def student_list(request):
    students = User.objects.filter(role='student').order_by('-date_joined')
    class_filter = request.GET.get('class')
    search = request.GET.get('search')
    status = request.GET.get('status')
    
    if class_filter:
        enrolled_students = Enrollment.objects.filter(
            class_enrolled_id=class_filter,
            status='active'
        ).values_list('student_id', flat=True)
        students = students.filter(id__in=enrolled_students)
    
    if search:
        students = students.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if status:
        enrolled_ids = Enrollment.objects.filter(status=status).values_list('student_id', flat=True)
        students = students.filter(id__in=enrolled_ids)
    
    classes = Class.objects.all()
    
    context = {
        'students': students,
        'classes': classes,
        'class_filter': class_filter,
        'search': search,
        'status': status,
    }
    return render(request, 'students/student_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.get_full_name()} created successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def student_update(request, pk):
    student = get_object_or_404(User, pk=pk, role='student')
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.get_full_name()} updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'action': 'Update', 'student': student})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def student_delete(request, pk):
    student = get_object_or_404(User, pk=pk, role='student')
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def student_detail(request, pk):
    student = get_object_or_404(User, pk=pk, role='student')
    enrollments = Enrollment.objects.filter(student=student).select_related('class_enrolled')
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')[:30]
    results = Result.objects.filter(student=student).select_related('exam').order_by('-created_at')[:10]
    fee_payments = FeePayment.objects.filter(student=student).select_related('fee_structure').order_by('-created_at')[:10]
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'attendance_records': attendance_records,
        'results': results,
        'fee_payments': fee_payments,
    }
    return render(request, 'students/student_detail.html', context)


def student_profile(request):
    student = request.user
    enrollments = Enrollment.objects.filter(student=student, status='active').select_related('class_enrolled')
    current_class = enrollments.first().class_enrolled if enrollments.exists() else None
    
    attendance = Attendance.objects.filter(student=student).order_by('-date')[:30]
    results = Result.objects.filter(student=student).select_related('exam').order_by('-created_at')[:10]
    fees = FeePayment.objects.filter(student=student).order_by('-created_at')[:10]
    
    context = {
        'student_profile': student,
        'enrollments': enrollments,
        'current_class': current_class,
        'attendance': attendance,
        'results': results,
        'fees': fees,
    }
    return render(request, 'students/student_profile.html', context)


def export_students_csv(request):
    import csv
    from django.utils import timezone
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="students_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Phone', 'Status', 'Classes'])
    
    students = User.objects.filter(role='student')
    for student in students:
        classes = ', '.join([
            f"{e.class_enrolled.name}-{e.class_enrolled.section}" 
            for e in student.enrollments.filter(status='active')
        ])
        writer.writerow([
            student.username,
            student.first_name,
            student.last_name,
            student.email,
            student.phone,
            student.is_active,
            classes
        ])
    
    return response
