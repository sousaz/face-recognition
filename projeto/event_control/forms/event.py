from django import forms
from event_control.models import *
from datetime import datetime

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"

        labels = {
            'name': 'Nome do evento*',
            'description': 'Descrição do evento*',
            'register_type': 'Tipo de registro*',
        }

        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'De um breve descrição do evento', 'rows': 4, 'cols': 40}),
        }

    start_date = forms.DateTimeField(
        required=True,
        label='Data de Início*',
        initial=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        widget=forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'}),
    )

    end_date = forms.DateTimeField(
        label='Data de encerramento*',
        required=False,
        widget=forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'})
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({ 'placeholder': 'Digite o nome do evento' })



