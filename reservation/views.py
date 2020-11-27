from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf

# Create your views here.
def solores(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'reservation/resview.html', {'login' : conf.login, 'resid' : id, 'user' : conf.getuser()})



def cr_reserve(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    dict_result = {} 
    roomt = request.POST.get('room_t', 'default')
    guests = request.POST.get('no_of_g', 'default')
    adate = request.POST.get('a_date', 'default')
    ddate = request.POST.get('d_date', 'default')
    dict_result['room'] = False
    dict_result['date'] = False
    dict_result['guest'] = False
    if adate > ddate:
        dict_result['date'] = True
        return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : [1, 3, 5], 'mindate' : conf.today, 'prob': dict_result, 'user' : conf.getuser()})


    print(roomt)
    print(guests)
    print(adate)
    print(ddate)
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("RESERV_ENTRY", [guests, conf.user_id, adate, ddate, roomt, order_count])
    suc = order_count.getvalue()
    cursor.close()
    if suc == 0:
        dict_result['room'] = True
    elif suc == 2:
        dict_result['guest'] = True
    else :
         return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'rsuccess': True})
    
    # print results
    print("Printing laptop details")
    
    print('hello1')
    return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : [1, 3, 5], 'mindate' : conf.today, 'prob': dict_result, 'user' : conf.getuser()})



def canreserv(request, id):
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("CANCEL_RESERV", [id, order_count])
    suc = order_count.getvalue()
    cursor.close()
    if suc == 1:
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'rcancel': True})
    return render(request, 'reservation/resview.html', {'login' : conf.login, 'resid' : id, 'user' : conf.getuser()}) 

