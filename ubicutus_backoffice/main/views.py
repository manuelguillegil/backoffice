from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Value, F
#from datetime import datetime, timedelta, weekday
from datetime import datetime, timedelta
from accounts.models import *
from main.forms import RegisterTaskForm


# Create your views here.
@login_required
def dashboard(request):
    worked_hours_week = 0#34
    worked_hours_total = 0#215
    completed_task = 0#30

    #suma de horas trabajadas por el request.user
    time_intervals = TimeInterval.objects.filter(user=request.user)#.aggregate(a=Sum((timeinterval.end_time.hour-timeinterval.init_time.hour)))
    for i in time_intervals:
        if(i.init_time==None):
            i.init_time = datetime.now()
        if(i.end_time==None):
            i.end_time = datetime.now() #+ timedelta(days=1)   
        worked_hours_total = worked_hours_total + ((i.end_time - i.init_time).total_seconds())//3600 #- i.init_time)#hours(i.end_time, i.init_time)#(i.end_time.datetime - i.init_time.datetime).hour


    # El intervalo entre start_date y end_date es de lunes a viernes
    today = datetime.today()
    day_of_week = today.weekday()
    start_date = today - timedelta(days=day_of_week+1)
    end_date = start_date + timedelta(days=5)
    st = start_date
    et = end_date
    time_intervals = TimeInterval.objects.filter(user=request.user, end_time__lte=et,  init_time__gte=st)

    for i in time_intervals:
        if(i.init_time==None):
            i.init_time = datetime.now()
        if(i.end_time==None):
            i.end_time = datetime.now() #+ timedelta(days=1)   
        worked_hours_week = worked_hours_week + ((i.end_time - i.init_time).total_seconds())//3600 #- i.init_time)#hours(i.end_time, i.init_time)#(i.end_time.datetime - i.init_time.datetime).hour


    completed_task = Task.objects.filter(status='Closed', usertaskassignrelation__user=request.user).count()

    args = {'worked_hours_week': int(worked_hours_week), 
            'worked_hours_total': int(worked_hours_total), 
            'completed_task': completed_task }

    return render(request, 'home.html', args)

def hours(end_hour, start_hour):
    end_minutes = end_hour.hour*60 + end_hour.minute
    start_minutes = start_hour.hour*60 + start_hour.minute
    return (end_minutes - start_minutes) #// 60

@login_required
def vacaciones(request):
    return render(request,'solicitud_vacaciones.html',{'variable':''})

@login_required
def adelanto(request):
    return render(request,'solicitud_adelanto.html',{'variable':''})

@login_required
def consulta_horas_trabajadas(request):
    return render(request,'consulta_horas.html',{'variable':''})

@login_required
def registro_horas_trabajadas(request):
    if request.method == "POST":
        form = RegisterTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('horas_trabajadas')
    else:
        form = RegisterTaskForm()
    return render(request,'registro_horas.html',{'form':form})

@login_required
def reporte(request):
    return render(request,'reporte_faltas.html',{'variable':''})

@login_required
def tareas(request):
    """
    #Check the username and the loged user
    if request.user.username != username:
        return redirect('dashboard')
    
    #try to get the user data if exists
    usr = get_object_or_404(UserTaskAssignRelation, username=User.username)

    #Try to get the user stats:
    usr_stats = get_object_or_404(User_stats, Email=usr.email)

    if request.method == 'POST':
        
        form = EditUserDataForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return redirect('user_data')  
    else:
        form = EditUserDataForm(instance=user_info)
    return render(request, 'dashboard/index.html', {'User_information': user_info, 'form': form, 'stat':usr_stats})"""
    return render(request,'tareas.html',{'variable':''})