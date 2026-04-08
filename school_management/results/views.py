from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Avg, Max, Min
from django.utils import timezone

from users.models import User
from academics.models import Class, Subject, Enrollment, TeacherSubjectAssignment
from results.models import Exam, Result, StudentPerformance
from .forms import ExamForm, ResultForm


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def exam_list(request):
    exams = Exam.objects.all().select_related('class_enrolled', 'subject', 'created_by').order_by('-date')
    class_filter = request.GET.get('class')
    exam_type = request.GET.get('type')
    
    if class_filter:
        exams = exams.filter(class_enrolled_id=class_filter)
    if exam_type:
        exams = exams.filter(exam_type=exam_type)
    
    context = {
        'exams': exams,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
        'exam_type': exam_type,
    }
    return render(request, 'results/exam_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            messages.success(request, f'Exam {exam.name} created successfully!')
            return redirect('results:exam_list')
    else:
        form = ExamForm()
        if request.user.is_teacher:
            form.fields['class_enrolled'].queryset = Class.objects.filter(
                Q(class_teacher=request.user) |
                Q(teacher_assignments__teacher=request.user)
            ).distinct()
    
    return render(request, 'results/exam_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, f'Exam {exam.name} updated successfully!')
            return redirect('results:exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'results/exam_form.html', {'form': form, 'action': 'Update', 'exam': exam})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully!')
        return redirect('exam_list')
    return render(request, 'results/exam_confirm_delete.html', {'exam': exam})


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def add_results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        marks = request.POST.get('marks')
        
        Result.objects.update_or_create(
            student_id=student_id,
            exam=exam,
            defaults={'marks_obtained': marks}
        )
        messages.success(request, 'Result added successfully!')
        return redirect('add_results', exam_id=exam_id)
    
    enrollments = Enrollment.objects.filter(class_enrolled=exam.class_enrolled, status='active').select_related('student')
    
    results = Result.objects.filter(exam=exam).select_related('student')
    students_with_results = results.values_list('student_id', flat=True)
    
    context = {
        'exam': exam,
        'enrollments': enrollments,
        'results': results,
        'students_with_results': list(students_with_results),
    }
    return render(request, 'results/add_results.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def bulk_add_results(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    if request.method == 'POST':
        marks_data = request.POST.get('marks_data')
        if marks_data:
            import json
            marks_dict = json.loads(marks_data)
            for student_id, marks in marks_dict.items():
                Result.objects.update_or_create(
                    student_id=student_id,
                    exam=exam,
                    defaults={'marks_obtained': marks}
                )
        messages.success(request, 'Results saved successfully!')
        return redirect('exam_list')
    
    enrollments = Enrollment.objects.filter(class_enrolled=exam.class_enrolled, status='active').select_related('student')
    results = {r.student_id: r.marks_obtained for r in Result.objects.filter(exam=exam)}
    
    context = {
        'exam': exam,
        'enrollments': enrollments,
        'results': results,
    }
    return render(request, 'results/bulk_add_results.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def result_list(request):
    results = Result.objects.all().select_related('student', 'exam', 'exam__class_enrolled', 'exam__subject').order_by('-created_at')
    
    class_filter = request.GET.get('class')
    student_filter = request.GET.get('student')
    
    if class_filter:
        results = results.filter(exam__class_enrolled_id=class_filter)
    if student_filter:
        results = results.filter(student_id=student_filter)
    
    context = {
        'results': results,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
        'student_filter': student_filter,
    }
    return render(request, 'results/result_list.html', context)


def student_results(request):
    student = request.user
    results = Result.objects.filter(student=student).select_related('exam', 'exam__class_enrolled', 'exam__subject').order_by('-created_at')
    
    exams = Exam.objects.filter(class_enrolled__enrollments__student=student).distinct()
    
    context = {
        'results': results,
        'exams': exams,
    }
    return render(request, 'results/student_results.html', context)


@login_required
def result_detail(request, student_id):
    if request.user.is_admin_user or request.user.is_teacher:
        student = get_object_or_404(User, pk=student_id, role='student')
    else:
        student = request.user
    
    results = Result.objects.filter(student=student).select_related('exam', 'exam__class_enrolled', 'exam__subject').order_by('-exam__date')
    
    context = {
        'student': student,
        'results': results,
    }
    return render(request, 'results/result_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user or u.is_teacher)
def generate_report_card(request, student_id):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    
    student = get_object_or_404(User, pk=student_id, role='student')
    enrollment = Enrollment.objects.filter(student=student, status='active').first()
    
    results = Result.objects.filter(student=student).select_related('exam', 'exam__subject')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_card_{student.username}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    
    elements.append(Paragraph("School Management System", title_style))
    elements.append(Paragraph(f"Report Card - {student.get_full_name()}", styles['Heading2']))
    elements.append(Spacer(1, 20))
    
    if enrollment:
        elements.append(Paragraph(f"Class: {enrollment.class_enrolled.name}-{enrollment.class_enrolled.section}", styles['Normal']))
        elements.append(Paragraph(f"Roll No: {enrollment.roll_number}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    data = [['Subject', 'Exam', 'Total Marks', 'Obtained', 'Percentage', 'Status']]
    for result in results:
        data.append([
            result.exam.subject.name,
            result.exam.name,
            str(result.exam.total_marks),
            str(result.marks_obtained),
            f"{result.percentage}%",
            result.status
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response
