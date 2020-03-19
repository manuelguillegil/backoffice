from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.forms.models import inlineformset_factory
from accounts.models import *
from django.forms.widgets import *

class RegisterTaskForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre",
        max_length=60,
        required= True,
    )

    description = forms.CharField(
        label="Descripción",
        max_length=1000,
        widget=forms.Textarea,
        required=True,
    )

    init_date = forms.DateField(
        label="Fecha de inicio",
        required=True
    )

    end_date = forms.DateField(
        label="Fecha de finalización",
        required=False
    )

    status = forms.ChoiceField(
        label='Status', 
        required=True,
        choices=Task.Status.choices,
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'init_date', 'end_date', 'status')

class RegisterTimeInterval(forms.ModelForm):
    init_time = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'class': "form-control form-control-user",
        'id': 'task-id',
        'placeholder': 'Fecha de inicio',
        'type': 'datetime-local'
        }),
        )
    end_time = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'class': "form-control form-control-user",
        'id': 'task-id',
        'placeholder': 'Fecha de fin',
        'type': 'datetime-local'
        }),
        )


    class Meta:
        model = TimeInterval
        fields = ['init_time', 'end_time']

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'init_date', 'end_date', 'status')


class RequestVacation(forms.ModelForm):

    init_date = forms.DateField(
        label="Fecha inicial",
        required=True
    )

    end_date = forms.DateField(
        label="Fecha final",
        required=False
    )

    description = forms.CharField(
        label="Información adicional",
        max_length=1000,
        widget=forms.Textarea,
        required=True,
    )

    class Meta:
        model = Vacation
        fields = ('init_date','end_date','description')

class RequestAdvancement(forms.ModelForm):

    quantity = forms.CharField(
        label="Cantidad ($)",
        max_length=60,
        required= True,
    )

    description = forms.CharField(
        label="Información adicional",
        max_length=1000,
        widget=forms.Textarea,
        required=True,
    )

    class Meta:
        model = Advancement
        fields = ('quantity','description')

class RequestReport(forms.ModelForm):

    date = forms.DateField(
        label="Día de falta",
        required=True
    )

    description = forms.CharField(
        label="Motivo",
        max_length=1000,
        widget=forms.Textarea,
        required=True,
    )

    class Meta:
        model = Report
        fields = ('date','description')