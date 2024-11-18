from django import forms
from event_control.views import *
from event_control.models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'course', 'photo']

        labels = {
            'name': 'Nome completo*',
            'student_id': 'Matricula*',
            'course': 'Curso*',
            'photo': 'Uma selfie sua*'
        }
        
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
        label="Curso*"
    )
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({ 'placeholder': 'Digite seu nome' })
        self.fields['student_id'].widget.attrs.update({ 'placeholder': 'Digite a sua matricula' })

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['photo']

        labels = {
            'photo': 'Nova selfie sua*'
        }
    
    def clean_photo(self):
        return self.cleaned_data.get('photo')
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'course', 'photo']

        labels = {
            'name': 'Nome completo',
            'student_id': 'Matricula',
            'course': 'Curso',
            'photo': 'Uma selfie sua'
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True