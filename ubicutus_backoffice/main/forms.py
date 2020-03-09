from django import forms
from accounts.models import *

class RegisterTimeInterval(forms.ModelForm):
    init_time = forms.DateTimeField(
        required=True,
        widget=forms.DateInput(attrs={'class': "form-control form-control-user",
        'id': 'task-id',
        'placeholder': 'Fecha de inicio',
        'type': 'date'
        }),
        )
    end_time = forms.DateTimeField(
        required=True,
        widget=forms.DateInput(attrs={'class': "form-control form-control-user",
        'id': 'task-id',
        'placeholder': 'Fecha de fin',
        'type': 'date'
        }),
    )

    class Meta:
        model = TimeInterval
        fields = ['init_time', 'end_time', 'task']