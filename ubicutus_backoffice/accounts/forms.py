from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import UserProfile
#CAMBIAR USERNAME PARA QUE SEA EL EMAIL Y PASAR EL REGISTER A ACCOUNTS
class SignUpForm(UserCreationForm):
    name = forms.CharField(
        label='name',
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

    username = forms.CharField(
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
        fields = ('name', 'lastname', 'username', 'password1', 'password2')

class LoginForm(LoginView):
    username = forms.CharField(
        label='Username',
        max_length=50,
        required=True,
    )
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
    )

    class Meta:
        model = User
        fields = ('username', 'password')


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
