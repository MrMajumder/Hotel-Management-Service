from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
from datetime import datetime
import time 

# Create your views here.
def index(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT * FROM ACCOUNT_HOLDER WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    acholder = cursor.fetchall()

    sql = ("SELECT * FROM ACCOUNT_HOLDER_PHNUMBER WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    acholderph = cursor.fetchall()

    sql = ("SELECT * FROM CUSTOMER WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    customer = cursor.fetchall()

    cursor.close()
    dict_result = {} 
    
    dict_result['user_id'] = acholder[0][0]
    dict_result['email'] = acholder[0][1]
    dict_result['username'] = acholder[0][2]
    dict_result['name'] = acholder[0][2] + ' ' + acholder[0][3]
    dict_result['house_no'] = acholder[0][4]
    dict_result['road_no'] = acholder[0][5]
    dict_result['city'] = acholder[0][6]
    dict_result['country'] = acholder[0][7]
    dict_result['id_card_no'] = customer[0][1]
    dict_result['passport_no'] = customer[0][2]
    dict_result['credit_card_no'] = customer[0][3]

    ph_no = []
    for ph in acholderph:
        num = ph[1]
        row = {'phone_no' : num}
        ph_no.append(row)
    dict_result['phone_nums'] = ph_no

    return render(request, 'customer/index.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result})

def res(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    today = str(time.strftime("%Y-%m-%d"))
    print(today)
    return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : [1, 3, 5], 'mindate' : today, 'user' : conf.getuser()})

def solores(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'reservation/resview.html', {'login' : conf.login, 'resid' : id, 'user' : conf.getuser()})

def his(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'customer/history.html', {'login' : conf.login, 'user' : conf.getuser()})

def ser(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : [2, 4, 6, 8, 10], 'user' : conf.getuser()})

def soloser(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'service/servview.html', {'login' : conf.login, 'servid' : id, 'user' : conf.getuser()})



