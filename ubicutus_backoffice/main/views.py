from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Value, F
#from datetime import datetime, timedelta, weekday
from datetime import datetime, timedelta
from accounts.models import *
from main.forms import RegisterTaskForm
from .forms import RegisterTimeInterval, EditTaskForm
from django.forms import modelformset_factory



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


##    completed_task = Task.objects.filter(status='Closed', usertaskassignrelation__user=request.user).count()

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
	## Por los momentos solo hacer get de todas las horas trabajadas
	time_intervals = TimeInterval.objects.filter(user=request.user)
	time_intervals_dummie = [{
		'id': 10,
		'init_time': '10/03/2020 05:00',
		'end_time': '11/03/2020 05:00',
		'task_id': 10,
		'user_id': 1
	},
	{
		'id': 11,
		'init_time': '10/03/2020 05:00',
		'end_time': '11/03/2020 05:00',
		'task_id': 7,
		'user_id': 2
	},
	{
		'id': 12,
		'init_time': '10/03/2020 05:00',
		'end_time': '11/03/2020 05:00',
		'task_id': 9,
		'user_id': 3
	}]

	task_dummie = {
		'id': 10,
		'name': 'Backoffice - Frontend',
		'description': 'Desarrollar Backoffice',
		'date': '11/03/2020 05:00',
		'progress': 'CLOSED'
	}
	return render(request,'consulta_horas.html',{'time_intervals':time_intervals_dummie, 'tasks': task_dummie})

@login_required
def registrar_tareas_trabajadas(request):

	if request.POST.get('action') == 'post':
		args = {
			'name'        : request.POST.get('task_name'),
			'description' : request.POST.get('task_description'),
			'init_date'   : request.POST.get('task_init_date'),
			'end_date'    : request.POST.get('task_end_date'),
			'status'      : request.POST.get('end_init_date'),
			'user'        : [str(request.user.id)]
		}
		form = RegisterTaskForm(args)
		print(request.POST)

		if form.is_valid():
			form.save()
			args['status'] = 'success'
			args['errorMsg'] = 'Everything ok'
			return JsonResponse(args)
		else:
			args['status'] = 'error'
			args['errorMsg'] = 'Error de validación de campos'
			return JsonResponse(args)
		
	if request.method == "POST":
		form = RegisterTaskForm(request.POST)
		print(request.POST)
		if form.is_valid():
			form.save()
			return redirect('horas_trabajadas')
	#If the task its been created on the fly (not by its own page)
	else:
		form = RegisterTaskForm()
	return render(request,'registrar_tarea.html',{'form':form})

@login_required
def lista_tarea(request):
	# Query to obtain the user that is requesting his tasks
	users = User.objects.filter(username=request.user.username)

	#Query to obtain all in progress tasks
	tasks_ip = Task.objects.filter(status=Task.Status.INPROGRESS).filter(user__in = users)
	return render(request,'lista_tareas.html',{'tasks':tasks_ip})


@login_required
def registrar_nueva_hora(request, pk):
	task = get_object_or_404(Task, pk=pk)
	if request.method == 'POST':
		form = RegisterTimeInterval(request.POST)
		if form.is_valid():
			time_interval = form.save(commit=False)
			time_interval.task_id = task
			time_interval.user_id = request.user
			time_interval.save()
			return redirect('tareas')
	else:
		form = RegisterTimeInterval()
	return render(request,'registrar_nueva_hora.html',{'form':form})

@login_required
def reporte(request):
	return render(request,'reporte_faltas.html',{'variable':''})

@login_required
def tareas(request):
    
	# Query to obtain the user that is requesting his tasks
	users = User.objects.filter(username=request.user.username)

	#Query to obtain all new tasks
	tasks_new = Task.objects.filter(status=Task.Status.NEW).filter(user__in = users) 

	#Query to obtain all in progress tasks
	tasks_ip = Task.objects.filter(status=Task.Status.INPROGRESS).filter(user__in = users) 

	#Query to obtain all waiting to be done tasks
	tasks_waiting = Task.objects.filter(status=Task.Status.WAITING).filter(user__in = users) 
    
	#Query to obtain all done tasks
	tasks_done = Task.objects.filter(status=Task.Status.CLOSED).filter(user__in = users)

	#Create task form
	form = RegisterTaskForm()

	all_tasks = Task.objects.filter().filter(user__in = users)

	tasks_and_forms = []
	for t in all_tasks:
		tasks_and_forms.append( [ t , EditTaskForm(instance=t)] )


	args = {'done': tasks_done,
            'new': tasks_new,
            'inpro': tasks_ip,
            'waiting': tasks_waiting,
            'all': all_tasks,
            'tasksWForms' : tasks_and_forms,
			'new_task_form' : form
            }

	return render(request,'tareas.html', args)


@login_required
def editar_tarea(request,pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tareas')  
    else:
        form = EditTaskForm(instance=task)

    return render(request, 'edit_task.html', {'tasks': task, 'form': form})


def miviewloca(request):
	formset = modelformset_factory(Task, fields=('id','name', 'description', 'init_date', 'end_date') )
	form = formset()
	return render(request, 'mihtmlloco.html', {'form':form} )