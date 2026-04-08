from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum
from django.utils import timezone

from users.models import User
from academics.models import Class, Enrollment
from fees.models import FeeCategory, FeeStructure, FeePayment, FeeWaiver
from .forms import FeeCategoryForm, FeeStructureForm, FeePaymentForm


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_category_list(request):
    categories = FeeCategory.objects.all().order_by('name')
    return render(request, 'fees/fee_category_list.html', {'categories': categories})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_category_create(request):
    if request.method == 'POST':
        form = FeeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee category created successfully!')
            return redirect('fees:fee_category_list')
    else:
        form = FeeCategoryForm()
    return render(request, 'fees/fee_category_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_category_update(request, pk):
    category = get_object_or_404(FeeCategory, pk=pk)
    if request.method == 'POST':
        form = FeeCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee category updated successfully!')
            return redirect('fees:fee_category_list')
    else:
        form = FeeCategoryForm(instance=category)
    return render(request, 'fees/fee_category_form.html', {'form': form, 'action': 'Update'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_structure_list(request):
    structures = FeeStructure.objects.all().select_related('fee_category', 'class_enrolled').order_by('-academic_year')
    class_filter = request.GET.get('class')
    
    if class_filter:
        structures = structures.filter(class_enrolled_id=class_filter)
    
    context = {
        'structures': structures,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
    }
    return render(request, 'fees/fee_structure_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_structure_create(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure created successfully!')
            return redirect('fees:fee_structure_list')
    else:
        form = FeeStructureForm()
    return render(request, 'fees/fee_structure_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_structure_update(request, pk):
    structure = get_object_or_404(FeeStructure, pk=pk)
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure updated successfully!')
            return redirect('fees:fee_structure_list')
    else:
        form = FeeStructureForm(instance=structure)
    return render(request, 'fees/fee_structure_form.html', {'form': form, 'action': 'Update'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def collect_fee(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.collected_by = request.user
            payment.status = 'paid'
            payment.save()
            messages.success(request, f'Fee collected successfully! Transaction ID: {payment.transaction_id}')
            return redirect('fees:fee_payment_list')
    else:
        form = FeePaymentForm()
    return render(request, 'fees/collect_fee.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_payment_list(request):
    payments = FeePayment.objects.all().select_related('student', 'fee_structure', 'fee_structure__fee_category', 'fee_structure__class_enrolled').order_by('-created_at')
    
    class_filter = request.GET.get('class')
    status_filter = request.GET.get('status')
    student_filter = request.GET.get('student')
    
    if class_filter:
        payments = payments.filter(fee_structure__class_enrolled_id=class_filter)
    if status_filter:
        payments = payments.filter(status=status_filter)
    if student_filter:
        payments = payments.filter(student_id=student_filter)
    
    total_collected = payments.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'payments': payments,
        'classes': Class.objects.all(),
        'students': User.objects.filter(role='student'),
        'class_filter': class_filter,
        'status_filter': status_filter,
        'student_filter': student_filter,
        'total_collected': total_collected,
    }
    return render(request, 'fees/fee_payment_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def update_payment_status(request, pk):
    payment = get_object_or_404(FeePayment, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        payment.status = new_status
        if new_status == 'paid':
            payment.payment_date = timezone.now().date()
        payment.save()
        messages.success(request, f'Payment status updated to {new_status}')
    return redirect('fee_payment_list')


def student_fees(request):
    student = request.user
    payments = FeePayment.objects.filter(student=student).select_related('fee_structure', 'fee_structure__fee_category').order_by('-created_at')
    
    total_pending = payments.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
    total_paid = payments.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'payments': payments,
        'total_pending': total_pending,
        'total_paid': total_paid,
    }
    return render(request, 'fees/student_fees.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def fee_report(request):
    class_filter = request.GET.get('class')
    status_filter = request.GET.get('status')
    
    payments = FeePayment.objects.all()
    
    if class_filter:
        payments = payments.filter(fee_structure__class_enrolled_id=class_filter)
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    summary = payments.values(
        'fee_structure__fee_category__name',
        'fee_structure__class_enrolled__name'
    ).annotate(
        total_amount=Sum('amount'),
        count=Sum(1)
    )
    
    total_amount = payments.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'summary': summary,
        'total_amount': total_amount,
        'classes': Class.objects.all(),
        'class_filter': class_filter,
        'status_filter': status_filter,
    }
    return render(request, 'fees/fee_report.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def generate_fee_invoice(request, pk):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    payment = get_object_or_404(FeePayment, pk=pk)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{payment.transaction_id}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph("School Management System - Fee Receipt", styles['Heading1']))
    elements.append(Spacer(1, 20))
    
    info = [
        ["Receipt No:", payment.transaction_id or 'N/A'],
        ["Student:", payment.student.get_full_name()],
        ["Class:", f"{payment.fee_structure.class_enrolled.name}-{payment.fee_structure.class_enrolled.section}"],
        ["Fee Type:", payment.fee_structure.fee_category.name],
        ["Amount:", f"${payment.amount}"],
        ["Status:", payment.status.capitalize()],
        ["Date:", str(payment.payment_date or timezone.now().date())],
    ]
    
    table = Table(info, colWidths=[150, 300])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response
