from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from crispy_forms.bootstrap import FormActions

from users.models import User
from academics.models import Class


class StudentForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 
                  'address', 'date_of_birth', 'photo', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Div(
                Div('username', css_class='col-md-6'),
                Div('email', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('first_name', css_class='col-md-6'),
                Div('last_name', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('phone', css_class='col-md-6'),
                Div('date_of_birth', css_class='col-md-6'),
                css_class='row'
            ),
            'address',
            'photo',
            Div(
                Div('password1', css_class='col-md-6'),
                Div('password2', css_class='col-md-6'),
                css_class='row'
            ),
            FormActions(
                Submit('submit', 'Save Student', css_class='btn-primary px-4'),
                HTML('<a class="btn btn-secondary ms-2" href="{% url \'students:student_list\' %}">Cancel</a>')
            )
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['id']
    
    class_id = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Select Class',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    roll_number = forms.CharField(max_length=20, label='Roll Number')
