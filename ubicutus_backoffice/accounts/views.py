from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.core.validators import validate_email as VALIDATE_THE_EMAIL
from django.core.exceptions import ValidationError

# Create your views here.

def indexView(request):
	return render(request,'index.html')

@login_required
def dashboardView(request):
	return render(request,'dashboard.html')

def registerView(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			if (not validate_email(user.username) ):
				form = SignUpForm()
				return render(request,'register.html',{'form':form})
			else:
				form.save()
				return redirect('login')
	else:
		form = SignUpForm()
	return render(request,'register.html',{'form':form})



def validate_email(email):

	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	try:
		validate_email(email)
		return validate_ubicutus_email(email)
	except ValidationError:
		return False

def validate_ubicutus_email(email):
	if len(email)<14:
		return False
	email_reverse=email[::-1]
	ubic = "moc.sutucibu@"
	for i in range(13):
		if (email_reverse[i] != ubic[i]):
			return False
	return True

# Create your views here.
def login(request):
    return render(request,'login.html',{'variable':''})

def signup(request):
    return render(request,'register.html',{'variable':''})

def profile(request):
    return render(request,'ajustes_perfil.html',{'variable':''})
