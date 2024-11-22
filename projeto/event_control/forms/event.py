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
            'min_hours': 'Horas minimas para o certificado*',
            'workload': 'Carga horaria do evento*',
            'min_attendance': 'Presenças minimas para o certificado*'
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
        initial=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        widget=forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'})
    )

    min_hours = forms.TimeField(
        label='Horas minimas para o certificado*',
        required=False,
        widget=forms.TimeInput(format=('%H:%M'), attrs={'type': 'time'})
    )

    workload = forms.TimeField(
        label='Carga horaria do evento*',
        required=True,
        widget=forms.TimeInput(format=('%H:%M'), attrs={'type': 'time'})
    )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({ 'placeholder': 'Digite o nome do evento' })
        self.fields['min_attendance'].widget.attrs.update({ 'placeholder': 'Digite o número mínimo de presenças' })
        self.fields['min_attendance'].required = False




