from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    return render(request,'home.html',{'variable':''})

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
    return render(request,'registro_horas.html',{'variable':''})

@login_required
def reporte(request):
    return render(request,'reporte_faltas.html',{'variable':''})

@login_required
def tareas(request):
    return render(request,'tareas.html',{'variable':''})