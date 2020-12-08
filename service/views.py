from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
from django.db import connection
from datetime import datetime
from employee import views

# Create your views here.
def soloser(request, id, completesuccess = None):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    sql = ("SELECT X.SERVICE_ID, X.ROOM_ID, X.BILL_ID, Y.NAME, Y.DESCRIPTION, Y.COST, X.SERVICE_ACTIVE, X.EMP_ID, (Z.FIRST_NAME || ' ' || Z.LAST_NAME) FULLNAME FROM ROOM_HB_SERV_RECEIVES X, SERVICES Y, ACCOUNT_HOLDER Z WHERE X.SERVICE_ID = Y.SERVICE_ID AND X.ACTION_ID = %s AND Z.USER_ID = X.EMP_ID" % (id))
    cursor.execute(sql)
    row = cursor.fetchall()
    cursor.close()
    service = {}
    service['servid'] = row[0][0]
    service['roomid'] = row[0][1]
    service['billid'] = row[0][2]
    service['name'] = row[0][3]
    service['description'] = row[0][4]
    service['cost'] = row[0][5]
    service['isactive'] = row[0][6]
    service['empid'] = row[0][7]
    service['empname'] = row[0][8]
    service['actionid'] = id
    
    return render(request, 'service/servview.html', {'login' : conf.login, 'service' : service, 'completesuccess' : completesuccess, 'user' : conf.getuser()})
    # return render(request, 'service/servview.html', {'login' : conf.login, 'servid' : id, 'user' : conf.getuser()})


def cr_service(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    servicet = request.POST.get('service_t', 'default')
    serviced = request.POST.get('serd', 'default')
    roomid = request.POST.get('roomid', 'default')

    cursor = connection.cursor()
    returnval = cursor.callfunc('SERVICE_ENTRY', int, [servicet, serviced, int(conf.user_id), int(roomid)])
    cursor.close()
    data = getserv()

    if returnval == 1:
        return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser(), 'srsuccess': True})
    elif returnval == 2:
        return render(request, 'service/cusservhome.html', {'login' : conf.login, 'rprob': True, 'data' : data, 'user' : conf.getuser()})
    return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : data,  'sprob': True, 'user' : conf.getuser()})

def completeservice(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    print('action id ', id)
    cursor = connection.cursor()
    sql = ("UPDATE ROOM_HB_SERV_RECEIVES SET SERVICE_ACTIVE = 3 WHERE ACTION_ID = %s" % id)
    cursor.execute(sql)
    cursor.close()

    return soloser(request, id, True)

def ca_serve(request, id):
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("CANCEL_SERVE", [id, order_count])
    suc = order_count.getvalue()
    cursor.close()
    data = getserv()
    if suc == 0:
        if(conf.role == 'customer'):
            return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser(), 'scancel': True})
        else:
            
            # return render(request, 'service/allserv.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser(), 'scancel': True})
            return views.servmanage(request, 0, True)
    return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    
def getserv():
    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT X.ACTION_ID, X.SERVICE_ID, Z.NAME, X.ROOM_ID, Y.RESERVATION_ID, X.SERVICE_DATE, X.SERVICE_ACTIVE FROM ROOM_HB_SERV_RECEIVES X, HOTEL_BILL Y, SERVICES Z WHERE X.BILL_ID = ANY(SELECT BILL_ID FROM HOTEL_BILL WHERE RESERVATION_ID = ANY(SELECT RESERVATION_ID FROM RESERVATION WHERE USER_ID = %s)) AND X.BILL_ID = Y.BILL_ID AND X.SERVICE_ACTIVE IN (1, 3) AND Z.SERVICE_ID = X.SERVICE_ID" % id)
    cursor.execute(sql)
    table = cursor.fetchall()
    cursor.close()
    data = []
    for row in table:
        ser = {}
        ser['actionid'] = row[0]
        ser['servid'] = row[1]
        ser['name'] = row[2]
        ser['roomid'] = row[3]
        ser['resid'] = row[4]
        ser['servdate'] = row[5].date()
        ser['isactive'] = row[6]
        data.append(ser)
    
    data = sorted(data, key=lambda item: int(item['servid']))
    return data