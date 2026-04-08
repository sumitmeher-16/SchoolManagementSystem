from django.contrib import admin
from .models import FeeCategory, FeeStructure, FeePayment, FeeWaiver


@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['fee_category', 'class_enrolled', 'amount', 'duration', 'academic_year']
    list_filter = ['duration', 'academic_year', 'class_enrolled']


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'amount', 'status', 'payment_date']
    list_filter = ['status', 'payment_date']


@admin.register(FeeWaiver)
class FeeWaiverAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_payment', 'waiver_amount', 'approved_by']
