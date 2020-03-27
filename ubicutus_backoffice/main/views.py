from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import json
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Value, F, Max
#from datetime import datetime, timedelta, weekday
from datetime import datetime, timedelta
from accounts.models import *
from main.forms import RegisterTaskForm
from django.core.exceptions import ValidationError
from .forms import RegisterTimeInterval, EditTaskForm, RequestVacation, RequestAdvancement, RequestReport, TaskId
from ubicutus_backoffice.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from datetime import datetime

from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import ast
from django.core.mail import EmailMultiAlternatives



# Create your views here.
@login_required
def dashboard(request):

    worked_hours_week = 0
    worked_hours_total = 0
    completed_task = 0
    assigned_task = 0
    hours_last_five_days = 0

    users = get_user(request)
    all_tasks = Task.objects.filter(user__in=users).filter(archived=False)

    #suma de horas trabajadas por el request.user
    time_intervals = TimeInterval.objects.filter(user=request.user).filter(task__in=all_tasks)
    for i in time_intervals:
        if(i.init_time==None):
            i.init_time = datetime.now()
        if(i.end_time==None):
            i.end_time = datetime.now() #+ timedelta(days=1)
        worked_hours_total = worked_hours_total + ((i.end_time - i.init_time).total_seconds()) #- i.init_time)#hours(i.end_time, i.init_time)#(i.end_time.datetime - i.init_time.datetime).hour


    # El intervalo entre start_date y end_date es de una semana
    today = datetime.today()
    day_of_week = today.weekday()
    start_date = today - timedelta(days=day_of_week+1)
    end_date = start_date + timedelta(days=7)
    st = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    et = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    time_intervals = TimeInterval.objects.filter(
        user=request.user, 
        end_time__lte=et,  
        init_time__gte=st,
    ).filter(task__in=all_tasks)

    for i in time_intervals:
        if(i.init_time==None):
            i.init_time = datetime.now()
        if(i.end_time==None):
            i.end_time = datetime.now() #+ timedelta(days=1)
        worked_hours_week = worked_hours_week + ((i.end_time - i.init_time).total_seconds()) #- i.init_time)#hours(i.end_time, i.init_time)#(i.end_time.datetime - i.init_time.datetime).hour

    # Tareas completadas
    completed_task = Task.objects.filter(status=Task.Status.CLOSED).filter(user__in = users).filter(archived=False).count()
    
    # Tareas asignadas
    assigned_task = Task.objects.filter(user__in = users).filter(archived=False)\
    .exclude(status=Task.Status.CLOSED).count()
    
    # Horas trabajadas durante los ultimos 5 dias trabajados
    time_intervals = TimeInterval.objects.filter(user=request.user).filter(task__in=all_tasks).order_by('-init_time')

    last_day = None
    cnt = 0

    for i in time_intervals:
        if(i.init_time==None):
            i.init_time = datetime.now()
        if(i.end_time==None):
            i.end_time = datetime.now()
        if last_day != i.init_time.date():
            last_day = i.init_time.date()
            cnt+=1
        if cnt>5:
            break
        hours_last_five_days += ((i.end_time - i.init_time).total_seconds())


    # Top 5 tareas trabajadas mas recientemente, junto con su estatus
    recent_tasks_top5 = TimeInterval.objects.filter(task__in=all_tasks).filter(user=request.user)\
    .values('task').annotate(x=Max('end_time'))\
    .order_by('-x').values('task__name','task__status')[:5]


    #######################################################
    args = {'worked_hours_week': int(worked_hours_week//3600),
            'worked_hours_total': int(worked_hours_total//3600),
            'completed_task': completed_task,
            'assigned_task': assigned_task,
            'hours_last_five_days' : int(hours_last_five_days//3600),
            'recent_tasks_top5' : recent_tasks_top5}

    return render(request, 'home.html', args)

######### Views para serializar queries ####################

# Nro de tareas agrupados por status
def status_chart(request):
    empty = 0

    labels = ['Hecho', 'En curso', 'Nuevo', 'Detenido']
    data = [0, 0, 0, 0]

    queryset = Task.objects.filter(user=request.user).filter(archived=False)\
    .values('status').annotate(task_count=Count('pk'))\
    .order_by('status')

    if(not queryset):
        empty = 1

    for entry in queryset:
        if entry['status'] == 'Closed':
            data[0] = entry['task_count']
        elif entry['status'] == 'In progress':
            data[1] = entry['task_count']
        elif entry['status'] == 'Waiting':
            data[3] = entry['task_count']
        else:
            data[2] = entry['task_count']
    
    return JsonResponse(data = { 'labels': labels, 'data': data, 'empty': empty})

# Top 5 tareas que mas horas han consumido, junto con su cantidad de horas
def task_hours_chart(request):
    empty = 0

    labels = []
    data = []
    all_tasks = Task.objects.filter(archived=False)


    task_hours_set = {}

    time_intervals = TimeInterval.objects.filter(user=request.user).filter(task__in=all_tasks)

    if(not time_intervals):
        empty = 1

    for i in time_intervals:
        if(i.init_time==None):
            i.init_time = datetime.now()
        if(i.end_time==None):
            i.end_time = datetime.now()
        if i.task != None:
            if i.task not in task_hours_set:
                task_hours_set[i.task] = 0

            task_hours_set[i.task] += ((i.end_time - i.init_time).total_seconds())//3600

    task_hours_top5 = sorted(task_hours_set.items(), key = lambda x: x[1], reverse = True)
    task_hours_top5 = task_hours_top5[:5]

    for entry in task_hours_top5:
        labels.append(entry[0].name)
        data.append(entry[1])

    return JsonResponse(data = { 'labels': labels, 'data': data, 'empty': empty})

# Horas trabajadas durante la semana
def hours_worked_chart(request):
    empty = 0

    monday = 0
    tuesday = 0
    wedneday = 0
    thursday = 0
    friday = 0
    
    today = datetime.today()
    day_of_week = today.weekday()
    start_date = today - timedelta(days=day_of_week+1)
    end_date = start_date + timedelta(days=7)
    st = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    et = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    time_intervals = TimeInterval.objects.filter(
        user=request.user, 
        end_time__lte=et,  
        init_time__gte=st,
    )

    if(not time_intervals):
        empty = 1

    for time in time_intervals:
        hours = ((time.end_time - time.init_time).total_seconds())
        
        if time.end_time.weekday() == 0:
            monday += hours
        elif time.end_time.weekday() == 1:
            tuesday += hours
        elif time.end_time.weekday() == 2:
            wedneday += hours
        elif time.end_time.weekday() == 3:
            thursday += hours
        elif time.end_time.weekday() == 4:
            friday += hours
    
    labels = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
    data = [int(monday//3600), int(tuesday//3600), int(wedneday//3600), int(thursday//3600), int(friday//3600)]

    return JsonResponse(data = { 'labels': labels, 'data': data, 'empty': empty})

############################################################

def hours(end_hour, start_hour):
    end_minutes = end_hour.hour*60 + end_hour.minute
    start_minutes = start_hour.hour*60 + start_hour.minute
    return (end_minutes - start_minutes) #// 60

@login_required
def vacaciones(request):

    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = RequestVacation(request.POST)
        if form.is_valid():
            vacation = form.save(commit = False)

            if (profile.remaining_vac_days >= int(vacation.end_date.strftime("%d")) - int(vacation.init_date.strftime("%d")) and int(vacation.end_date.strftime("%d")) - int(vacation.init_date.strftime("%d")) >= 0):
                subject = 'Solicitud de vacaciones de {}'.format(str(user.username))
                original_profile = UserProfile.objects.get(id = profile.id)
                original_profile.remaining_vac_days = profile.remaining_vac_days - ( int(vacation.end_date.strftime("%d")) - int(vacation.init_date.strftime("%d")))
                original_profile.save()
                message = vacation.description
                recepient = 'jesuswahrman@gmail.com' #Arreglar
                # send_mail(subject,
                # message, EMAIL_HOST_USER, [recepient], fail_silently = False)

                subject, from_email, to = 'Solicitud de Vacaciones: ' + user.first_name, EMAIL_HOST_USER, 'jesuswahrman@gmail.com'
                text_content = 'This is an important message.'
                html_content = '<div> <div style="position: relative; left: 25%; color: #484848"> <img style="height: auto; width: 500px" src="https://www.ubicutus.com/static/home/images/ubicutus-logo_preview.png" /> <p color="#484848">Solicitd de Vacaciones:  ' + user.first_name + ' </p> <p color="#484848">Fecha de Inicio:  ' + str(vacation.init_date) + ' </p> <p color="#484848">Fecha de Fin: ' + str(vacation.end_date) + ' </p> <p color="#484848">Motivo: ' + vacation.description + ' </p> </div> </div>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('dashboard')
    else:
        form = RequestVacation()

    args = {'form' : form,
            'remaining_days' : profile.remaining_vac_days }

    return render(request,'solicitud_vacaciones.html',args)

@login_required
def adelanto(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = RequestAdvancement(request.POST)
        if form.is_valid():
            quantity = form.data['quantity']
            description = form.data['description']
            aproved = 0
            advancement = Advancement(user=request.user, quantity = quantity, description = description, aproved = aproved)
            advancementForm = form.save(commit = False)
            subject = 'Solicitud de adelanto de {}'.format(str(user.username))
            subject, from_email, to = 'Solicitud de Adelanto: ' + user.first_name, EMAIL_HOST_USER, 'jesuswahrman@gmail.com'
            text_content = 'This is an important message.'
            html_content = '<div> <div style="position: relative; left: 25%; color: #484848"> <img style="height: auto; width: 500px" src="https://www.ubicutus.com/static/home/images/ubicutus-logo_preview.png" /> <p color="#484848">Solicitd de Adelanto:  ' + user.first_name + ' </p> <p color="#484848">Cantidad:  ' + str(advancement.quantity) + ' </p> <p color="#484848">Motivo: ' + advancement.description + ' </p> </div> </div>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            try:
                advancement.full_clean()
                advancement.save()
            except ValidationError:
                form = RequestAdvancement()
            return redirect('dashboard')
    else:
        form = RequestAdvancement()

    args = {'form' : form }

    return render(request,'solicitud_adelanto.html',args)

@login_required
def consulta_horas_trabajadas(request):
    ## Por los momentos solo hacer get de todas las horas trabajadas
    time_i = TimeInterval.objects.filter(user=request.user).order_by('-init_time')
    time_intervals = []
    for t in time_i:
        time_intervals.append([t,Task.objects.get(id=t.task_id)])

 
    return render(request,'consulta_horas.html',{'time_intervals':time_intervals})

@login_required
def registrar_tareas_trabajadas(request):
  
    if request.method == "POST":
        form = RegisterTaskForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error'})


    #If the task its been created on the fly (not by its own page)
    else:
        form = RegisterTaskForm()
    
@login_required
def registrar_tareas_trabajadas_render(request):
        
    if request.method == "POST":
        form = RegisterTaskForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('tareas')
        else:
            return redirect('nueva_tarea')

    #If the task its been created on the fly (not by its own page)
    else:
        form = RegisterTaskForm()
    
    return render(request,'registrar_tarea.html',{'form':form})

@login_required
def lista_tarea(request):
    # Query to obtain the user that is requesting his tasks
    users = User.objects.filter(username=request.user.username)

    #Query to obtain all in progress tasks
    tasks_ip = Task.objects.filter(user__in = users).filter(archived=False)

    if request.method == 'POST':
        task = request.POST.get('list-hours')
        return redirect('nueva_hora', task)

    return render(request,'lista_tareas.html',{'tasks':tasks_ip})


@login_required
def registrar_nueva_hora(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = RegisterTimeInterval(request.POST)
        
        init = form.data['init_time']
        end = form.data['end_time']
        init_obj = datetime.strptime(init, '%d/%m/%Y %H:%M')
        end_obj = datetime.strptime(end, '%d/%m/%Y %H:%M')

        time_interval = TimeInterval(init_time=init_obj,end_time=end_obj,
            task=task,user=request.user)
        try:
            time_interval.full_clean()
            time_interval.save()
            return redirect('horas_trabajadas')
        except ValidationError:
            form = RegisterTimeInterval()
    else:
        form = RegisterTimeInterval()
    return render(request,'registrar_nueva_hora.html',{'form':form})

@login_required
def reporte(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = RequestReport(request.POST)
        if form.is_valid():
            date = form.data['date']
            description = form.data['description']
            aproved = 0
            reportObject = Report(user=request.user, date = date, description = description)
            advancementForm = form.save(commit = False)
            report = form.save(commit = False)
            subject = 'Reporte de falta de {}'.format(str(user.username))
            subject, from_email, to = 'Reporte de falta: ' + user.first_name, EMAIL_HOST_USER, 'jesuswahrman@gmail.com'
            text_content = 'This is an important message.'
            html_content = '<div> <div style="position: relative; left: 25%; color: #484848"> <img style="height: auto; width: 500px" src="https://www.ubicutus.com/static/home/images/ubicutus-logo_preview.png" /> <p color="#484848">Reporte de falta:  ' + user.first_name + ' </p> <p color="#484848">Fecha:  ' + str(report.date) + ' </p> <p color="#484848">Motivo: ' + report.description + ' </p> </div> </div>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            try:
                reportObject.full_clean()
                reportObject.save()
            except ValidationError:
                form = RequestReport()
            return redirect('dashboard')
    else:
        form = RequestReport()

    args = {'form' : form }

    return render(request,'reporte_faltas.html',args)

@login_required
def tareas(request):
    
    # Query to obtain the user that is requesting his tasks
    users = get_user(request)

    #Query to obtain all new tasks
    tasks_new = Task.objects.filter(status=Task.Status.NEW).filter(archived=False).filter(user__in = users) 

    #Query to obtain all in progress tasks
    tasks_ip = Task.objects.filter(status=Task.Status.INPROGRESS).filter(archived=False).filter(user__in = users) 

    #Query to obtain all waiting to be done tasks
    tasks_waiting = Task.objects.filter(status=Task.Status.WAITING).filter(archived=False).filter(user__in = users) 
    
    #Query to obtain all done tasks
    tasks_done = Task.objects.filter(status=Task.Status.CLOSED).filter(archived=False).filter(user__in = users)

    #Create task form
    form = RegisterTaskForm()

    all_tasks = Task.objects.filter(archived=False).filter(user__in = users)

    tasks_and_forms = []

    delete_form = TaskId()

    archive_form = TaskId()

    # ARREGLAR ESTOOOoOoO
    for t in all_tasks:
        tasks_and_forms.append( [ t , EditTaskForm()] )


    args = {'done': tasks_done,
            'new': tasks_new,
            'inpro': tasks_ip,
            'waiting': tasks_waiting,
            'all': all_tasks,
            'tasksWForms' : tasks_and_forms,
            'new_task_form' : form,
            'delete_form' : delete_form,
            'archive_form' : archive_form,
            'edit_task_form' : EditTaskForm()
            }

    return render(request,'tareas.html', args)

# NO USAR EESTE
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

    return render(request, 'edit_task.html', {'task': task, 'form': form})

@login_required
def editar_tarea_new(request):
    users = get_user(request)

    if request.method == 'POST':
        form = EditTaskForm(request.POST)
        pk = form.data['task_id']
        if ( Task.objects.filter(id=pk).filter(user__in = users).exists() ):
            obj = Task.objects.get(id=pk)
            obj.name = form.data['name']
            obj.description = form.data['description']
            obj.init_date = form.data['init_date']
            obj.end_date = form.data['end_date']
            obj.status = form.data['status']
            obj.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error'})
    else:
        form = EditTaskForm()

    return render(request, 'edit_task_new.html', {'form': form})


@login_required
def contador(request):
    #Query to obtain all in progress tasks
    tasks_ip = Task.objects.filter(user = request.user).filter(archived=False)

    if request.method == 'POST':
        task_id = request.POST.get('list-hours')
        task = get_object_or_404(Task, pk=task_id)

        request.user.userprofile.clock_last_task = task
        request.user.userprofile.full_clean()
        request.user.userprofile.save()
        
        # time = request.session['clock']
        # end = datetime.strptime(time, '%H:%M:%S')
        
        # end_obj = datetime.today()
        # init_obj = end_obj - timedelta(hours=end.hour, minutes=end.minute, seconds=end.second)

        # time_interval = TimeInterval(init_time=init_obj,end_time=end_obj,
        #     task=task,user=request.user)
        # try:
        #     time_interval.full_clean()
        #     time_interval.save()
        #     return redirect('horas_trabajadas')
        # except ValidationError:
        #     print("There was an error")

    return render(request,'my_time.html',{'tasks': tasks_ip})

@login_required
def eliminar_tarea(request):
    users = get_user(request)
    if request.method == 'POST':
        print("me llegó un post")
        form = TaskId(request.POST)
        pk = form.data['task_id']
        if ( Task.objects.filter(id=pk).filter(user__in = users).exists() ):
            Task.objects.filter(id=pk).delete()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error la tarea no existe'})
    else:
        form = TaskId()
        return render(request, 'delete_task.html', {'form': form})

@login_required
def archivar_tarea(request):
    users = get_user(request)
    if request.method == 'POST':
        form = TaskId(request.POST)
        pk = form.data['task_id']
        if ( Task.objects.filter(id=pk).filter(user__in = users).exists() ):
            obj = Task.objects.get(id=pk)
            obj.archived = True
            obj.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error la tarea no existe'})
    else:
        form = TaskId()
        return render(request, 'delete_task.html', {'form': form})

@login_required
def desarchivar_tarea(request):
    users = get_user(request)
    if request.method == 'POST':
        form = TaskId(request.POST)
        pk = form.data['task_id']
        if ( Task.objects.filter(id=pk).filter(user__in = users).exists() ):
            obj = Task.objects.get(id=pk)
            obj.archived = False
            obj.save()
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error la tarea no existe'})
    else:
        form = TaskId()
        return render(request, 'delete_task.html', {'form': form})


def tareas_archivadas(request):
    users = get_user(request)
    arch_tasks = Task.objects.filter(archived=True).filter(user__in = users)
    args = {
        'arch_tasks' : arch_tasks,
        'edit_task_form' : EditTaskForm(),
        'dearch_task_form' : TaskId()
    }
    return render(request, 'archived_task.html', args)


def obtener_valores(request):
    if request.method == 'POST':
        pk = request.POST.get('task_id')
        obj = Task.objects.get(id=pk)
        args = {
                'success' : 'yes',
                'name' : obj.name,
                'description' : obj.description,
                'init_date' : obj.init_date,
                'end_date' : obj.end_date,
                'status' : obj.status
               }
        return JsonResponse(args)
    else:
        return JsonResponse({'success':'no'})


@csrf_exempt
def clock_view(request): # la comparten PAUSE y RESET (y play en menor medida)
    if request.method == 'POST':

        myDict = request.user.userprofile

        newStatus = int(request.POST['clock_status'])
        myDict.clock = request.POST['clock']
        myDict.clock_status = newStatus
        clockString = myDict.clock

        if(newStatus == 1):
            myDict.save()
            request.user.save()
            return JsonResponse({'status':'success','clockString': clockString})

        task = myDict.clock_last_task

        if(task == None):
            return JsonResponse({'status':'error_task','clockString':clockString})

        last_init = myDict.clock_last_init

        if(last_init == None and newStatus!=0):
            return JsonResponse({'status':'error_time','clockString':clockString})

        # save interval
        if(last_init != None):
            interval = TimeInterval(init_time=last_init, end_time=datetime.now(), user=request.user, task=task)
            interval.full_clean()
            interval.save()

        # last init = None
        myDict.clock_last_init = None

        # if reset then task = None
        if(newStatus == 0):
            myDict.clock_last_task = None


        myDict.save()
        request.user.save()

        if(clockString != None):
            return JsonResponse({'status':'success','clockString': clockString})
        else:
            return JsonResponse({'status':'error_clock','clockString':''})

    return HttpResponse('Not Post')

@csrf_exempt
def clock_unload(request): # Cambio de Pagina
    if request.method == 'POST' and request.user.is_authenticated:
        
        stri = str(request.body)
        mydict = ast.literal_eval(stri[2:-1])
        myDict = request.user.userprofile
        
        myDict.clock_status = int(mydict['clock_status'])
        myDict.clock = mydict['clock']
        myDict.save()
        request.user.save()
        
        #print("JEJEJEJEJEJEJEJEJEJEJEJEJEJEJEJEJEJJEJEJEJEJEJEJEJEJEJE")
        #print(myDict.clock)
        #print(myDict.clock_status)
        #clockString = request.user.userprofile.clock
        clockString = "--:--:--"

        if(clockString != None):
            return JsonResponse({'status':'success','clockString': clockString})
        else:
            return JsonResponse({'status':'error_clock','clockString':''})

    return HttpResponse('Not Post')

@csrf_exempt
def clock_play(request): # PLAY 
    if request.method == 'POST':

        myDict = request.user.userprofile

        # la task se deberia guardar en la base de datos por otro lado
        #myDict.clock_last_task = request.POST['last_task']
        task = myDict.clock_last_task

        if(task == None):
            return JsonResponse({'status':'error_task','clockString':'','clock_status':0})

        last_init = myDict.clock_last_init

                                # si le das play, entonces estabas
        if(last_init != None and myDict.clock_status != 1):  # en pausa o estabas en reset, entonces last_init == None
            return JsonResponse({'status':'error_time','clockString':'','clock_status':0})

        myDict.clock_last_init = datetime.now()
        request.user.save()
        myDict.save()
        
        clockString = myDict.clock
        clock_status = myDict.clock_status

        #print("JIJIJIJIJIJIJIJIJIJIJIJIJIJIJIJIJIJJIJIJIJIJIJIJIJIJIJI")
        #print(clockString)
        #print(clock_status)

        if(clockString != None and clock_status!=None):
            return JsonResponse({
                'status':'success',
                'clockString': clockString,
                'clock_status':clock_status,
                })
        else:
            return JsonResponse({'status':'error_clock','clockString':'','clock_status':clock_status})

    return HttpResponse('Not Post')


# UTILITIES FOR THE QUERIES
def get_user(request):
    return User.objects.filter(username=request.user.username)

# VIEW HOUR FOR ADMINS
def pairIntervalHours(timeInterval):
    ## De un intervalo lo convierto en un par [intervalo,tiempo entre intervalo]
    pairlist = []
    for t in timeInterval:
        hours = t.end_time - t.init_time
        pairlist.append([t,hours])
    return pairlist

def groupByUserAndMonth(pairInterval):
    ## Agrupa por usuario y mes
    newList = []
    for pair in pairInterval:
        needToAppend=True
        for i in newList:
            if pair[0].user==i[0].user and pair[0].init_time.month==i[0].init_time.month:
                i[1]=i[1]+pair[1]
                needToAppend=False
                break
        if needToAppend:
            newList.append([pair[0],pair[1]])
    return newList

@login_required
def horas_trabajadas_admin(request):
    ## Vista de Admin
    today = datetime.now()
    time_this_month = TimeInterval.objects.filter(init_time__year=today.year,init_time__month=today.month)
    time_this_year = TimeInterval.objects.filter(init_time__year=today.year)
    time_this_week = TimeInterval.objects.filter(init_time__week=today.strftime("%V"))

    ## Convierto en pares [intervalo,horas]
    hours_in_this_month = pairIntervalHours(time_this_month)
    hours_in_this_year = pairIntervalHours(time_this_year)
    hours_in_this_week = pairIntervalHours(time_this_week)

    ## GroupBy Usuario y Mes
    hours_in_this_month = groupByUserAndMonth(hours_in_this_month)
    hours_in_this_year = groupByUserAndMonth(hours_in_this_year)
    hours_in_this_week = groupByUserAndMonth(hours_in_this_week)
 
    return render(request, 'consulta_horas_admin.html',{'hours_in_this_week':hours_in_this_week,'hours_in_this_month':hours_in_this_month,'hours_in_this_year':hours_in_this_year})


