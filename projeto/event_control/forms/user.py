from typing import Any
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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({ 'placeholder': 'Digite seu email' })
        self.fields['password'].widget.attrs.update({ 'placeholder': 'Digite sua senha' })

class UserAuthForm(forms.Form):
    email = forms.EmailField(
        max_length=255, 
        required=True, 
        label='Email*',
        widget=forms.EmailInput(attrs={ 'placeholder': 'Email' })
    )
    password = forms.CharField(
        max_length=255,
        required=True,
        label='Senha*',
        widget=forms.PasswordInput(attrs={ 'placeholder': 'Senha' }),
    )

