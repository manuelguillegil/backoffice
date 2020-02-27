from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class EditUserDataForm(forms.ModelForm):
    
    username = forms.CharField(
        label='Username',
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', 
        max_length=152,
        required=True, 
    )   

    first_name = forms.CharField(
        label='FirstName',
        help_text='Required. 150 characters or fewer. Letters only.', 
        max_length=152,
        required=True, 
    )

    last_name = forms.CharField(
        label='LastName',
        help_text='Required. 150 characters or fewer. Letters only.', 
        max_length=152,
        required=True, 
    )   

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class EditProfileForm(forms.ModelForm):
    
    position = forms.CharField(
        label='Position',
        help_text='Required. 150 characters or fewer. Letters only.', 
        max_length=152,
        required=True, 
    )   

    class Meta:
        model = UserProfile
        fields = ('position',)