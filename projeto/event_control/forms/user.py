from django import forms
from event_control.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'password': forms.PasswordInput()
        }

        labels = {
            'email': 'Email*',
            'password': "Senha*"
        }
