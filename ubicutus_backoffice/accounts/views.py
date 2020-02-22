from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html',{'variable':''})

def signup(request):
    return render(request,'register.html',{'variable':''})