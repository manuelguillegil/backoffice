from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'home.html',{'variable':''})

def dashboard(request):
    return render(request,'dashboard/index.html',{'variable':''})

def vacaciones(request):
    return render(request,'solicitud_vacaciones.html',{'variable':''})

def adelanto(request):
    return render(request,'solicitud_adelanto.html',{'variable':''})

def consulta_horas_trabajadas(request):
    return render(request,'consulta_horas.html',{'variable':''})

def registro_horas_trabajadas(request):
    return render(request,'registro_horas.html',{'variable':''})

def reporte(request):
    return render(request,'reporte_faltas.html',{'variable':''})