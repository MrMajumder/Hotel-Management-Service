from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
import time
from datetime import datetime
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
    sql = ("SELECT * FROM RESERVATION WHERE USER_ID=%s AND RESERVATION_ACTIVE IN (0, 1, 2, 3   )" % id)
    cursor.execute(sql)
    table = cursor.fetchall()
    cursor.close()

    data = []
    for row in table:
        res = {}
        res['resid'] = row[0]
        res['arrivaldate'] = row[2].date()
        res['departuredate'] = row[3].date()
        res['isactive'] = row[4]
        data.append(res)
    
    data = sorted(data, key=lambda item: int(item['resid']))

    return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : data, 'mindate' : today, 'user' : conf.getuser()})

def solores(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'reservation/resview.html', {'login' : conf.login, 'resid' : id, 'user' : conf.getuser()})

def his(request, id):
    id = int(id)
    if(conf.login == False or id > 3 or id < 0):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    #id = 0 : res all, 1 : res query, 2: serv all, 3 : serv query
    if(id <= 1):
        #   Part for Reservation Showing
        sql = ("SELECT RESERVATION_ID, RESERVATION_ACTIVE, ARRIVAL_DATE, DEPARTURE_DATE FROM RESERVATION WHERE USER_ID = %s" %(int(conf.user_id)))
        msg = "Showing results for : all reservations "
        if(id == 1):
            arrdate = request.POST.get('arrdate', '')
            depdate = request.POST.get('depdate', '')
            restype = request.POST.get('restype', '')

            if(arrdate or depdate or restype):
                msg = msg + " with"
                if(arrdate):
                    sql = sql + " AND ARRIVAL_DATE >= TO_DATE(" + str("\'" + arrdate + "\', 'YYYY-MM-DD') ")
                    msg = msg + " arrival date >= " + str("\"" + arrdate + "\", ")
                if(depdate):
                    sql = sql + " AND DEPARTURE_DATE <= TO_DATE(" + str("\'" + depdate + "\', 'YYYY-MM-DD') ")
                    msg = msg + " departure date <= " + str("\"" + depdate + "\", ")
                if(restype == 'Active'):
                    sql = sql + " AND RESERVATION_ACTIVE = 1 "
                    msg = msg + " and type = Active "
                elif(restype == 'Pending'):
                    sql = sql + " AND RESERVATION_ACTIVE = 0 "
                    msg = msg + " and type = Inactive "
                elif(restype == 'Cancelled'):
                    sql = sql + " AND RESERVATION_ACTIVE = 2 "
                    msg = msg + " and type = Cancelled "
                elif(restype == 'Completed'):
                    sql = sql + " AND RESERVATION_ACTIVE = 3 "
                    msg = msg + " and type = Completed "
                else:
                    msg = msg + " and type = All "
        cursor = connection.cursor()
        cursor.execute(sql)
        table = cursor.fetchall()
        cursor.close()

        data = []
        for row in table:
            r = {}
            r['resid'] = row[0]
            r['isactive'] = row[1]
            r['arrdate'] = row[2].date()
            r['depdate'] = row[3].date()
            data.append(r)

        data = sorted(data, key=lambda item: int(item['resid']))

        return render(request, 'reservation/allres.html', {'login' : conf.login,'data' : data, 'msg' : msg, 'user' : conf.getuser()})
    #--------------------
    #--------------------
    #--------------------
    else:
        #   Part for Service Showing
        sql = ("SELECT * FROM ROOM_HB_SERV_RECEIVES WHERE BILL_ID IN (SELECT BILL_ID FROM HOTEL_BILL, RESERVATION WHERE HOTEL_BILL.RESERVATION_ID = RESERVATION.RESERVATION_ID AND RESERVATION.USER_ID = %s)" %(int(conf.user_id)))
        msg = "Showing results for : all reservations "
        if(id == 3):
            serdate = request.POST.get('servdate', '')
            sertype = request.POST.get('sertype', '')

            if(serdate or sertype):
                msg = msg + " with"
                if(serdate):
                    sql = sql + " AND TRUNC(SERVICE_DATE) = TO_DATE(" + str("\'" + serdate + "\', 'YYYY-MM-DD') ")
                    msg = msg + " service execution date = " + str("\"" + serdate + "\", ")
                if(sertype == 'Active'):
                    sql = sql + " AND SERVICE_ACTIVE = 1 "
                    msg = msg + " type = Active "
                elif(sertype == 'Cancelled'):
                    sql = sql + " AND SERVICE_ACTIVE = 2 "
                    msg = msg + " type = Cancelled "
                elif(sertype == 'Completed'):
                    sql = sql + " AND SERVICE_ACTIVE = 3 "
                    msg = msg + " type = Completed "
                else:
                    msg = msg + " type = All "
        print(sql)
        cursor = connection.cursor()
        cursor.execute(sql)
        table = cursor.fetchall()
        cursor.close()

        data = []
        for row in table:
            ser = {}
            ser['servid'] = row[0]
            ser['roomid'] = row[1]
            ser['billid'] = row[2]
            ser['isactive'] = row[3]
            ser['actionid'] = row[4]
            ser['servdate'] = row[5]
            data.append(ser)

        data = sorted(data, key=lambda item: int(item['servid']))

        return render(request, 'service/allserv.html', {'login' : conf.login,'data' : data, 'msg' : msg, 'user' : conf.getuser()})


def ser(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT X.ACTION_ID, X.SERVICE_ID, Z.NAME, X.ROOM_ID, Y.RESERVATION_ID FROM ROOM_HB_SERV_RECEIVES X, HOTEL_BILL Y, SERVICES Z WHERE X.BILL_ID = ANY(SELECT BILL_ID FROM HOTEL_BILL WHERE RESERVATION_ID = ANY(SELECT RESERVATION_ID FROM RESERVATION WHERE USER_ID = %s)) AND X.BILL_ID = Y.BILL_ID AND X.SERVICE_ACTIVE = 1 AND Z.SERVICE_ID = X.SERVICE_ID" % id)
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
        data.append(ser)
    
    data = sorted(data, key=lambda item: int(item['servid']))

    return render(request, 'service/cusservhome.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser()})

def soloser(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'service/servview.html', {'login' : conf.login, 'servid' : id, 'user' : conf.getuser()})

def com(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'customer/complaint.html', {'login' : conf.login, 'data' : [2, 4, 6, 8, 10], 'user' : conf.getuser()})

def fcom(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    complain = request.POST.get('comp', 'default')
    cursor = connection.cursor()
    cursor.callproc("NEW_COMPLAIN", [conf.user_id, complain])
    cursor.close()
    return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'comp' : True})



