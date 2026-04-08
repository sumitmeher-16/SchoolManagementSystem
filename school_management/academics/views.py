from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse

from users.models import User
from academics.models import Class, Subject, Enrollment, TeacherSubjectAssignment
from .forms import ClassForm, SubjectForm, EnrollmentForm


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def class_list(request):
    classes = Class.objects.all().order_by('name', 'section')
    search = request.GET.get('search')
    
    if search:
        classes = classes.filter(
            Q(name__icontains=search) |
            Q(section__icontains=search) |
            Q(academic_year__icontains=search)
        )
    
    context = {
        'classes': classes,
        'search': search,
    }
    return render(request, 'academics/class_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save()
            messages.success(request, f'Class {class_obj.name}-{class_obj.section} created successfully!')
            return redirect('academics:class_list')
    else:
        form = ClassForm()
    return render(request, 'academics/class_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def class_update(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Class {class_obj.name}-{class_obj.section} updated successfully!')
            return redirect('academics:class_list')
    else:
        form = ClassForm(instance=class_obj)
    return render(request, 'academics/class_form.html', {'form': form, 'action': 'Update', 'class_obj': class_obj})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def class_delete(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_obj.delete()
        messages.success(request, 'Class deleted successfully!')
        return redirect('class_list')
    return render(request, 'academics/class_confirm_delete.html', {'class_obj': class_obj})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def class_detail(request, pk):
    class_obj = get_object_or_404(Class, pk=pk)
    enrollments = Enrollment.objects.filter(class_enrolled=class_obj, status='active').select_related('student')
    assignments = TeacherSubjectAssignment.objects.filter(class_assigned=class_obj).select_related('teacher', 'subject')
    
    context = {
        'class_obj': class_obj,
        'enrollments': enrollments,
        'assignments': assignments,
    }
    return render(request, 'academics/class_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def subject_list(request):
    subjects = Subject.objects.all().order_by('name')
    search = request.GET.get('search')
    
    if search:
        subjects = subjects.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )
    
    context = {
        'subjects': subjects,
        'search': search,
    }
    return render(request, 'academics/subject_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject {subject.name} created successfully!')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'academics/subject_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject {subject.name} updated successfully!')
            return redirect('academics:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'academics/subject_form.html', {'form': form, 'action': 'Update', 'subject': subject})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subject_list')
    return render(request, 'academics/subject_confirm_delete.html', {'subject': subject})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def enroll_student(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            class_obj = form.cleaned_data['class_enrolled']
            roll_number = form.cleaned_data.get('roll_number')
            
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                class_enrolled=class_obj,
                defaults={'roll_number': roll_number}
            )
            
            if created:
                messages.success(request, 'Student enrolled successfully!')
            else:
                messages.warning(request, 'Student is already enrolled in this class.')
            
            return redirect('academics:class_detail', pk=class_obj.pk)
    else:
        form = EnrollmentForm()
    
    return render(request, 'academics/enroll_student.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def enrollment_list(request):
    enrollments = Enrollment.objects.all().select_related('student', 'class_enrolled').order_by('-enrollment_date')
    class_filter = request.GET.get('class')
    status_filter = request.GET.get('status')
    
    if class_filter:
        enrollments = enrollments.filter(class_enrolled_id=class_filter)
    if status_filter:
        enrollments = enrollments.filter(status=status_filter)
    
    context = {
        'enrollments': enrollments,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
        'status_filter': status_filter,
    }
    return render(request, 'academics/enrollment_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def update_enrollment_status(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        enrollment.status = new_status
        enrollment.save()
        messages.success(request, f'Enrollment status updated to {new_status}')
    return redirect('academics:enrollment_list')


def get_class_students(request, class_id):
    enrollments = Enrollment.objects.filter(class_enrolled_id=class_id, status='active').select_related('student')
    students = [{'id': e.student.id, 'name': e.student.get_full_name(), 'roll_number': e.roll_number} for e in enrollments]
    return JsonResponse({'students': students})
