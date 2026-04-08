from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions

from users.models import User
from academics.models import Class
from .models import FeeCategory, FeeStructure, FeePayment


class FeeCategoryForm(forms.ModelForm):
    class Meta:
        model = FeeCategory
        fields = ['name', 'description', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'description',
            'is_active',
            FormActions(
                Submit('submit', 'Save Category', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'fees:fee_category_list\' %}">Cancel</a>')
            )
        )


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['fee_category', 'class_enrolled', 'amount', 'duration', 'academic_year', 'due_date', 'is_active']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div('fee_category', css_class='col-md-6'),
                Div('class_enrolled', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('amount', css_class='col-md-4'),
                Div('duration', css_class='col-md-4'),
                Div('academic_year', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('due_date', css_class='col-md-6'),
                Div('is_active', css_class='col-md-6'),
                css_class='row'
            ),
            FormActions(
                Submit('submit', 'Save Structure', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'fees:fee_structure_list\' %}">Cancel</a>')
            )
        )


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_structure', 'amount', 'payment_method', 'transaction_id', 'remarks']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div('student', css_class='col-md-6'),
                Div('fee_structure', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('amount', css_class='col-md-6'),
                Div('payment_method', css_class='col-md-6'),
                css_class='row'
            ),
            'transaction_id',
            'remarks',
            FormActions(
                Submit('submit', 'Collect Fee', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'fees:fee_payment_list\' %}">Cancel</a>')
            )
        )
