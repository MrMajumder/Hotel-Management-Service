from django.shortcuts import render
from django.http import HttpResponse
from hms import conf

# Create your views here.
def profile(request):
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser()})

def resmanage(request):
    return render(request, 'employee/resmanage.html', {'login' : conf.login, 'user' : conf.getuser()})

def servmanage(request):
    return render(request, 'employee/servmanage.html', {'login' : conf.login, 'user' : conf.getuser()})

def empreg(request):
    return render(request, 'employee/empreg.html', {'login' : conf.login, 'user' : conf.getuser()})

def empmanage(request):
    return render(request, 'employee/empmanage.html', {'login' : conf.login, 'user' : conf.getuser()})

def hoteloverview(request):
    return render(request, 'employee/hoteloverview.html', {'login' : conf.login, 'user' : conf.getuser()})
