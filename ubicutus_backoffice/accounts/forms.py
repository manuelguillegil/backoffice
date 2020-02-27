from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control form-control-user",'id': 'exampleFirstName', 'placeholder': 'Primer Nombre'}),
    )

    lastname = forms.CharField(
        label='Lastname',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control form-control-user",'id': 'exampleLastName', 'placeholder': 'Apellido'}),
    )

    email = forms.CharField(
        label="Email",
        max_length=50, 
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control form-control-user",'id': 'exampleInputEmail', 'placeholder': 'Dirección de correo'}),
    )
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.TextInput(attrs={'class': "form-control form-control-user",'id': 'exampleInputPassword', 'placeholder': 'Contraseña'}),
    )

    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        help_text="Ingrese la misma contraseña que anteriormente, para verificación.",
        widget=forms.TextInput(attrs={'class': "form-control form-control-user",'id': 'exampleRepeatPassword', 'placeholder': 'Repite tu contraseña'}),
    )

    class Meta:
        model = User
        fields = ('username', 'lastname', 'email', 'password1', 'password2')

class LoginForm(LoginView):
    email = forms.CharField(
        label='Email',
        max_length=50,
        required=True,
    )
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email', 'password')