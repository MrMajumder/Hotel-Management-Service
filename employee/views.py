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

def expense(request):
    return render(request, 'employee/expense.html', {'login' : conf.login, 'user' : conf.getuser()})

def eattend(request):
    return render(request, 'employee/eattend.html', {'login' : conf.login, 'user' : conf.getuser()})

def fire(request):
    return render(request, 'employee/fire.html', {'login' : conf.login, 'user' : conf.getuser()})
    

def workh(request):
    return render(request, 'employee/workh.html', {'login' : conf.login, 'user' : conf.getuser()})

def serveEx(request):
    return render(request, 'employee/serveEx.html', {'login' : conf.login, 'user' : conf.getuser()})

def empsalary(request):
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def mansalary(request):
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def eproedit(request):
    return render(request, 'employee/empedit.html', {'login' : conf.login, 'user' : conf.getuser()})