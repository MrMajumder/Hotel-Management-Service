from django.shortcuts import render
from hms import conf

# Create your views here.
def index(request):
    return render(request, 'reservation/index.html', {'login' : conf.login, 'user' : conf.getuser()})

def reserv(request):
    return render(request, 'reservation/createReserv.html', {'login' : conf.login, 'user' : conf.getuser()})