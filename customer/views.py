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
    sql = ("SELECT X.*, Y.*, Z.* FROM ACCOUNT_HOLDER X, ACCOUNT_HOLDER_PHNUMBER Y, CUSTOMER Z WHERE X.USER_ID=%s AND X.USER_ID = Y.USER_ID AND X.USER_ID = Z.USER_ID;" % id )
    cursor.execute(sql)
    acholder = cursor.fetchall()

    cursor.close()
    dict_result = {} 
    
    dict_result['user_id'] = acholder[0][0]
    dict_result['email'] = acholder[0][1]
    dict_result['name'] = acholder[0][2] + ' ' + acholder[0][3]
    dict_result['house_no'] = acholder[0][4]
    dict_result['road_no'] = acholder[0][5]
    dict_result['city'] = acholder[0][6]
    dict_result['country'] = acholder[0][7]
    dict_result['id_card_no'] = acholder[0][11]
    dict_result['passport_no'] = acholder[0][12]
    dict_result['credit_card_no'] = acholder[0][13]

    ph_no = []
    for ph in acholder:
        num = ph[9]
        row = {'phone_no' : num}
        ph_no.append(row)
    dict_result['phone_nums'] = ph_no

    return render(request, 'customer/index.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result})

def res(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    today = str(time.strftime("%Y-%m-%d"))
    print(today)

    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT * FROM RESERVATION WHERE USER_ID=%s AND RESERVATION_ACTIVE = 1" % id)
    cursor.execute(sql)
    table = cursor.fetchall()

    data = []
    for row in table:
        res = {}
        res['resid'] = row[0]
        res['guest_no'] = row[1]
        res['arrivaldate'] = row[2]
        res['departuredate'] = row[3]
        res['resactive'] = row[4]
        data.append(res)
    
    data = sorted(data, key=lambda item: int(item['resid']))

    return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : data, 'mindate' : today, 'user' : conf.getuser()})

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
    
    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT X.ACTION_ID, X.SERVICE_ID, Z.NAME, X.ROOM_ID, Y.RESERVATION_ID FROM ROOM_HB_SERV_RECEIVES X, HOTEL_BILL Y, SERVICES Z WHERE X.BILL_ID = ANY(SELECT BILL_ID FROM HOTEL_BILL WHERE RESERVATION_ID = ANY(SELECT RESERVATION_ID FROM RESERVATION WHERE USER_ID = %s)) AND X.BILL_ID = Y.BILL_ID AND X.SERVICE_ACTIVE = 1 AND Z.SERVICE_ID = X.SERVICE_ID" % id)
    cursor.execute(sql)
    table = cursor.fetchall()
    print(table)
    data = []
    for row in table:
        ser = {}
        ser['actionid'] = row[0]
        ser['servid'] = row[1]
        ser['name'] = row[2]
        ser['roomid'] = row[3]
        ser['resid'] = row[4]
        data.append(ser)
    
    data = sorted(data, key=lambda item: int(item['servid']))

    return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser()})

def soloser(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'service/servview.html', {'login' : conf.login, 'servid' : id, 'user' : conf.getuser()})



