from django.shortcuts import render
from hms import conf

# Create your views here.
def solores(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'reservation/resview.html', {'login' : conf.login, 'resid' : id, 'user' : conf.getuser()})
