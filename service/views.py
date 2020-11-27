from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
from django.db import connection

# Create your views here.
def soloser(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    sql = ("SELECT X.SERVICE_ID, X.ROOM_ID, X.BILL_ID, Y.NAME, Y.DESCRIPTION, Y.COST, X.SERVICE_ACTIVE, Y.USER_ID, (Z.FIRST_NAME || ' ' || Z.LAST_NAME) FULLNAME FROM ROOM_HB_SERV_RECEIVES X, SERVICES Y, ACCOUNT_HOLDER Z WHERE X.SERVICE_ID = Y.SERVICE_ID AND X.ACTION_ID = %s AND Z.USER_ID = Y.USER_ID" % (id))
    cursor.execute(sql)
    row = cursor.fetchall()

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
    
    return render(request, 'service/servview.html', {'login' : conf.login, 'service' : service, 'user' : conf.getuser()})
    # return render(request, 'service/servview.html', {'login' : conf.login, 'servid' : id, 'user' : conf.getuser()})


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

    
