from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions

from users.models import User
from academics.models import Class, Subject
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        label='Student'
    )
    class_enrolled = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Class'
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        label='Subject'
    )
    
    class Meta:
        model = Attendance
        fields = ['student', 'class_enrolled', 'subject', 'date', 'status', 'remarks']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div('student', css_class='col-md-6'),
                Div('class_enrolled', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('subject', css_class='col-md-6'),
                Div('date', css_class='col-md-6'),
                css_class='row'
            ),
            'status',
            'remarks',
            FormActions(
                Submit('submit', 'Save Attendance', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'attendance_list\' %}">Cancel</a>')
            )
        )


class BulkAttendanceForm(forms.Form):
    class_enrolled = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Class'
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        label='Subject'
    )
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
