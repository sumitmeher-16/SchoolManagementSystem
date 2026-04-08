from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

from users.models import User
from academics.models import Class, TeacherSubjectAssignment, Subject
from attendance.models import Attendance
from results.models import Result, Exam
from .forms import TeacherForm


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def teacher_list(request):
    teachers = User.objects.filter(role='teacher').order_by('-date_joined')
    search = request.GET.get('search')
    
    if search:
        teachers = teachers.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    context = {
        'teachers': teachers,
        'search': search,
    }
    return render(request, 'teachers/teacher_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher {teacher.get_full_name()} created successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teachers/teacher_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def teacher_update(request, pk):
    teacher = get_object_or_404(User, pk=pk, role='teacher')
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Teacher {teacher.get_full_name()} updated successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/teacher_form.html', {'form': form, 'action': 'Update', 'teacher': teacher})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def teacher_delete(request, pk):
    teacher = get_object_or_404(User, pk=pk, role='teacher')
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def teacher_detail(request, pk):
    teacher = get_object_or_404(User, pk=pk, role='teacher')
    assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher).select_related('subject', 'class_assigned')
    assigned_classes = Class.objects.filter(class_teacher=teacher)
    
    context = {
        'teacher': teacher,
        'assignments': assignments,
        'assigned_classes': assigned_classes,
    }
    return render(request, 'teachers/teacher_detail.html', context)


def teacher_profile(request):
    teacher = request.user
    assignments = TeacherSubjectAssignment.objects.filter(teacher=teacher).select_related('subject', 'class_assigned')
    assigned_classes = Class.objects.filter(class_teacher=teacher)
    
    context = {
        'teacher_profile': teacher,
        'assignments': assignments,
        'assigned_classes': assigned_classes,
    }
    return render(request, 'teachers/teacher_profile.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def teacher_assign_subject(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        subject_id = request.POST.get('subject')
        class_id = request.POST.get('class_assigned')
        
        assignment, created = TeacherSubjectAssignment.objects.get_or_create(
            teacher_id=teacher_id,
            subject_id=subject_id,
            class_assigned_id=class_id
        )
        
        if created:
            messages.success(request, 'Subject assigned successfully!')
        else:
            messages.warning(request, 'This assignment already exists.')
        
        return redirect('teacher_detail', pk=teacher_id)
    
    teachers = User.objects.filter(role='teacher', is_active=True)
    subjects = Subject.objects.all()
    classes = Class.objects.all()
    
    return render(request, 'teachers/assign_subject.html', {
        'teachers': teachers,
        'subjects': subjects,
        'classes': classes,
    })


def export_teachers_csv(request):
    import csv
    from django.utils import timezone
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="teachers_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Phone', 'Status', 'Assigned Classes'])
    
    teachers = User.objects.filter(role='teacher')
    for teacher in teachers:
        classes = ', '.join([c.name for c in teacher.assigned_classes.all()])
        writer.writerow([
            teacher.username,
            teacher.first_name,
            teacher.last_name,
            teacher.email,
            teacher.phone,
            teacher.is_active,
            classes
        ])
    
    return response
