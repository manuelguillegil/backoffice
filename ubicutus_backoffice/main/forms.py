from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.forms.models import inlineformset_factory
from accounts.models import Task, UserTaskAssignRelation

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

    user = forms.ModelMultipleChoiceField(
        label="Integrante",
        queryset=User.objects.all().values_list('first_name', flat=True).exclude(username='bo_admin'),
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'init_date', 'end_date', 'status', 'user')

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['users'] = [t.pk for t in kwargs['instance'].user_set.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)
    
    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()
            instance.user_set.clear()
            instance.user_set.add(*self.cleaned_data['user'])
        
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()
        
        return instance

