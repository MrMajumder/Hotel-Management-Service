from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf

# Create your views here.
def soloser(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'service/servview.html', {'login' : conf.login, 'servid' : id, 'user' : conf.getuser()})


def cr_service(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    servicet = request.POST.get('service_t', 'default')
    serviced = request.POST.get('serd', 'default')
    roomid = request.POST.get('roomid', 'default')
    print(servicet)
    print(serviced)
    cursor = connection.cursor()
    returnval = cursor.callfunc('SERVICE_ENTRY', int, [servicet, serviced, conf.user_id, roomid])
    print(returnval)
    cursor.close()
    if returnval == 1:
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'srsuccess': True})
    elif returnval == 2:
        return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : [2, 4, 6, 8, 10],  'rprob': True, 'user' : conf.getuser()})
    return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : [2, 4, 6, 8, 10],  'sprob': True, 'user' : conf.getuser()})



def ca_serve(request, id):
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("CANCEL_SERVE", [id, order_count])
    suc = order_count.getvalue()
    cursor.close()
    if suc == 1:
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'scancel': True})
    return render(request, 'service/servview.html', {'login' : conf.login, 'resid' : id, 'user' : conf.getuser()}) 