from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions

from academics.models import Class, Subject
from .models import Exam, Result


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'class_enrolled', 'subject', 'date', 'total_marks', 'passing_marks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            Div(
                Div('exam_type', css_class='col-md-6'),
                Div('date', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('class_enrolled', css_class='col-md-6'),
                Div('subject', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('total_marks', css_class='col-md-6'),
                Div('passing_marks', css_class='col-md-6'),
                css_class='row'
            ),
            FormActions(
                Submit('submit', 'Save Exam', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'results:exam_list\' %}">Cancel</a>')
            )
        )


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'marks_obtained']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'student',
            'marks_obtained',
            FormActions(
                Submit('submit', 'Save Result', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'results:result_list\' %}">Cancel</a>')
            )
        )
