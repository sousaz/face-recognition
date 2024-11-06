from django import forms
from event_control.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    labels = {
        'email': 'Email*',
        'password': "Senha*"
    }
