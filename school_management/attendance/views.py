from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime

from users.models import User
from academics.models import Class, Subject, Enrollment, TeacherSubjectAssignment
from attendance.models import Attendance, AttendanceSummary
from .forms import AttendanceForm, BulkAttendanceForm


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def attendance_list(request):
    attendance_records = Attendance.objects.all().select_related('student', 'class_enrolled', 'subject').order_by('-date')
    class_filter = request.GET.get('class')
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')
    
    if class_filter:
        attendance_records = attendance_records.filter(class_enrolled_id=class_filter)
    if date_filter:
        attendance_records = attendance_records.filter(date=date_filter)
    if status_filter:
        attendance_records = attendance_records.filter(status=status_filter)
    
    context = {
        'attendance_records': attendance_records,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
        'date_filter': date_filter,
        'status_filter': status_filter,
        'today': timezone.now().date(),
    }
    return render(request, 'attendance/attendance_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def mark_attendance(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_enrolled')
        subject_id = request.POST.get('subject')
        date_str = request.POST.get('date')
        attendance_data = request.POST.getlist('attendance')
        
        class_obj = get_object_or_404(Class, pk=class_id)
        subject = get_object_or_404(Subject, pk=subject_id) if subject_id else None
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        enrollments = Enrollment.objects.filter(class_enrolled=class_obj, status='active')
        
        for enrollment in enrollments:
            status = 'present' if str(enrollment.student.id) in attendance_data else 'absent'
            Attendance.objects.update_or_create(
                student=enrollment.student,
                class_enrolled=class_obj,
                subject=subject,
                date=date,
                defaults={
                    'status': status,
                    'marked_by': request.user
                }
            )
        
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance_list')
    
    classes = Class.objects.all()
    if request.user.is_teacher:
        classes = Class.objects.filter(
            Q(class_teacher=request.user) |
            Q(teacher_assignments__teacher=request.user)
        ).distinct()
    
    subjects = Subject.objects.all()
    today = timezone.now().date()
    
    context = {
        'classes': classes,
        'subjects': subjects,
        'today': today,
    }
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def bulk_attendance(request):
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            class_obj = form.cleaned_data['class_enrolled']
            subject = form.cleaned_data['subject']
            date = form.cleaned_data['date']
            attendance_list = form.cleaned_data['attendance']
            
            for student_id, status in attendance_list:
                Attendance.objects.update_or_create(
                    student_id=student_id,
                    class_enrolled=class_obj,
                    subject=subject,
                    date=date,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )
            
            messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance_list')
    else:
        form = BulkAttendanceForm()
    
    return render(request, 'attendance/bulk_attendance.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def attendance_report(request):
    class_filter = request.GET.get('class')
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    today = timezone.now().date()
    if not month:
        month = today.month
    if not year:
        year = today.year
    
    attendance_records = Attendance.objects.filter(
        date__month=month,
        date__year=year
    )
    
    if class_filter:
        attendance_records = attendance_records.filter(class_enrolled_id=class_filter)
    
    summary = attendance_records.values('student__first_name', 'student__last_name', 'class_enrolled__name').annotate(
        present=Count('id', filter=Q(status='present')),
        absent=Count('id', filter=Q(status='absent')),
        late=Count('id', filter=Q(status='late')),
        total=Count('id')
    )
    
    context = {
        'attendance_records': attendance_records[:100],
        'summary': summary,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
        'month': month,
        'year': year,
    }
    return render(request, 'attendance/attendance_report.html', context)


def student_attendance_view(request):
    if request.user.is_admin_user:
        return redirect('attendance_report')
    
    student = request.user
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')[:100]
    
    present_count = attendance_records.filter(status='present').count()
    absent_count = attendance_records.filter(status='absent').count()
    total = attendance_records.count()
    percentage = round((present_count / total) * 100, 2) if total > 0 else 0
    
    context = {
        'attendance_records': attendance_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'total': total,
        'percentage': percentage,
    }
    return render(request, 'attendance/student_attendance.html', context)


def get_class_students_attendance(request, class_id):
    date = request.GET.get('date', timezone.now().date())
    subject_id = request.GET.get('subject')
    
    enrollments = Enrollment.objects.filter(class_enrolled_id=class_id, status='active').select_related('student')
    students_data = []
    
    for enrollment in enrollments:
        attendance = Attendance.objects.filter(
            student=enrollment.student,
            class_enrolled_id=class_id,
            date=date,
            subject_id=subject_id if subject_id else None
        ).first()
        
        students_data.append({
            'id': enrollment.student.id,
            'name': enrollment.student.get_full_name(),
            'roll_number': enrollment.roll_number,
            'status': attendance.status if attendance else None,
            'attendance_id': attendance.id if attendance else None
        })
    
    return JsonResponse({'students': students_data})
