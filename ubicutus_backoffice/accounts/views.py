from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,  EditUserDataForm, EditProfileForm
from django.contrib.auth.models import User
from django.core.validators import validate_email as VALIDATE_THE_EMAIL
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
@csrf_protect
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


@login_required
def profile(request):
    return render(request,'ajustes_perfil.html',{'variable':''})


@login_required
def edit_user_data(request):

    user = request.user
    profile = user.userprofile
    
    if request.method == 'POST':
        user_form = EditUserDataForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_data')  
    else:
        user_form = EditUserDataForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

    args = {'user_info': user, 'profile_info': profile,
            'user_form': user_form, 'profile_form': profile_form }

    return render(request, 'edit_user_data.html', args)



@login_required
def user_data(request):

    user = request.user
    profile = user.userprofile

    args = { 'user_info': user, 'profile_info': profile }

    return render(request, 'user_data.html', args)

@login_required
def my_time(request):

    # user = request.user
    # profile = user.userprofile

    # args = { 'user_info': user, 'profile_info': profile }

    return render(request, 'my_time.html')


# Funciones para validar email
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

# Funcion para enviar emails
# Esto aún tengo que editarlo
def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')