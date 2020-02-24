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
			print(user.username)
			if (not validate_email(user.username) ):
				form = SignUpForm()
				return render(request,'registration/register.html',{'form':form})
			else:
				form.save()
				return redirect('login_url')
	else:
		form = SignUpForm()
	return render(request,'registration/register.html',{'form':form})



def validate_email(email):

	from django.core.validators import validate_email
	from django.core.exceptions import ValidationError
	print (email)
	try:
		validate_email(email)
		print ("bienn")
		return validate_ubicutus_email(email)
	except ValidationError:
		print ("hola2")
		return False

def validate_ubicutus_email(email):
	print ("hola")
	if len(email)<14:
		return False
	email_reverse=email[::-1]
	ubic = "moc.sutucibu@"
	for i in range(13):
		if (email_reverse[i] != ubic[i]):
			return False
	print("cool")
	return True;