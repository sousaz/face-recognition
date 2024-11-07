from django import forms
from event_control.views import *
from event_control.forms.user import UserForm
from event_control.models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'course', 'photo']

        labels = {
            'name': 'Nome*',
            'student_id': 'Matricula*',
            'course': 'Curso*',
            'photo': 'Uma selfie sua*'
        }
        
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
        label="Curso*"
    )