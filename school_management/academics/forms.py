from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions

from users.models import User
from .models import Class, Subject, Enrollment


class ClassForm(forms.ModelForm):
    class_teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(role='teacher', is_active=True),
        required=False,
        label='Class Teacher'
    )
    
    class Meta:
        model = Class
        fields = ['name', 'section', 'class_teacher', 'subjects', 'academic_year']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-md-6'),
                Div('section', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('academic_year', css_class='col-md-6'),
                Div('class_teacher', css_class='col-md-6'),
                css_class='row'
            ),
            'subjects',
            FormActions(
                Submit('submit', 'Save Class', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'academics:class_list\' %}">Cancel</a>')
            )
        )


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'code',
            'description',
            FormActions(
                Submit('submit', 'Save Subject', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'academics:subject_list\' %}">Cancel</a>')
            )
        )


class EnrollmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        label='Student'
    )
    class_enrolled = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Class'
    )
    
    class Meta:
        model = Enrollment
        fields = ['student', 'class_enrolled', 'roll_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'student',
            'class_enrolled',
            'roll_number',
            FormActions(
                Submit('submit', 'Enroll Student', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'academics:enrollment_list\' %}">Cancel</a>')
            )
        )
