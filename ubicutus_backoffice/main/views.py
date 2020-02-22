from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'base_site.html',{'variable':''})

def dashboard(request):
    return render(request,'dashboard/index.html',{'variable':''})