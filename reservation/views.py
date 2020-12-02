from django.shortcuts import render
from django.db import connection
from hms import conf
from datetime import datetime

# Create your views here.


def solores(request, id):
    if(conf.login == False):
       return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser()})

    res = getres(id)
    
    return render(request, 'reservation/resview.html', {'login' : conf.login, 'res' : res, 'user' : conf.getuser()})




def cr_reserve(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    roomt = request.POST.get('room_t', 'default')
    adate = request.POST.get('a_date', 'default')
    ddate = request.POST.get('d_date', 'default')
    
    data = getallres()

    if adate >= ddate:
        return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : data, 'mindate' : conf.today, 'date': True, 'user' : conf.getuser()})

    # cursor = connection.cursor()
    # order_count = cursor.var(int).var
    # cursor.callproc("RESERV_ENTRY", [guests, conf.user_id, adate, ddate, roomt, order_count])
    # suc = order_count.getvalue()
    ADate = (str("\'"+adate+"\'"))
    DDate = (str("\'"+ddate+"\'"))
    
    cursor = connection.cursor()
    sql = ("SELECT ROOM_ID, CAPACITY, ROOM_TYPE, RENT FROM ROOM WHERE ROOM_ID NOT IN (SELECT B.ROOM_ID FROM BOOKED_ROOMS B, RESERVATION R WHERE R.RESERVATION_ID = B.RESERVATION_ID AND ROOM_SEARCH(B.ROOM_ID, %s, %s) <> %s AND (R.RESERVATION_ACTIVE = %s OR R.RESERVATION_ACTIVE = %s))" % (ADate, DDate, 1, 0, 1))
    if roomt != "":
        e = (str("\'"+roomt+"\'"))
        sql = sql + " AND ROOM_TYPE = " + e


    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    dict_result = []
    num = 0
    for r in result:
        room_id = r[0]
        capacity = r[1]
        r_type = r[2]
        rent = r[3]
        num = num + 1
        row = {'room_id': room_id, 'capacity': capacity, 'rtype': r_type, 'rent' : rent, 'num' : num}
        dict_result.append(row)
    conf.adate = adate
    conf.ddate = ddate
    
    if len(dict_result) == 0:
        return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : data, 'mindate' : conf.today, 'room': True, 'user' : conf.getuser()})

    return render(request, 'reservation/roomreserv.html', {'login' : conf.login, 'rooms': dict_result, 'adate' : adate, 'ddate': ddate,  'user' : conf.getuser()})
    
    
    # print results
def roomentry(request, id, adate, ddate):
    cursor = connection.cursor()
    num = 0
    ADate = (str("\'"+conf.adate+"\'"))
    DDate = (str("\'"+conf.ddate+"\'"))

    for x in range(id):
        rid = request.POST.get(str(x+1), '')
        if rid != "":
            print(rid)
            sql = ("SELECT ROOM_SEARCH(%s, %s, %s) FROM DUAL" % (int(rid), ADate, DDate))
            cursor.execute(sql)
            result = cursor.fetchall()
            returnval = result[0][0]
            if(returnval == 1):
                order_count = cursor.var(int).var
                cursor.callproc("NEW_RESERV_ENTRYS", [conf.user_id, conf.adate, conf.ddate, num, int(rid), order_count])
                num = order_count.getvalue()

    # cursor = connection.cursor()
    # order_count = cursor.var(int).var
    # cursor.callproc("RESERV_ENTRY", [guests, conf.user_id, adate, ddate, roomt, order_count])
    # suc = order_count.getvalue()
    cursor.close()
    data = getallres()
    
    return render(request, 'reservation/cusreshome.html', {'login' : conf.login, 'data' : data, 'mindate' : conf.today, 'rsuccess' : True, 'user' : conf.getuser()})


def canreserv(request, id):
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("CANCEL_RESERV", [id, order_count])
    suc = order_count.getvalue()
    cursor.close()
    if suc == 1:
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'rcancel': True})
    
    res = getres(id)

    return render(request, 'reservation/resview.html', {'login' : conf.login, 'res' : res, 'user' : conf.getuser(), 'cancelu' : True}) 

def getres(id):
    cursor = connection.cursor()
    sql = ("SELECT A.ARRIVAL_DATE, A.DEPARTURE_DATE, A.RESERVATION_ACTIVE, A.USER_ID, B.* FROM RESERVATION A, (SELECT N.ROOM_ID, N.RESERVATION_ID, M.ROOM_TYPE, M.CAPACITY FROM ROOM M, BOOKED_ROOMS N WHERE M.ROOM_ID = N.ROOM_ID) B WHERE A.RESERVATION_ID = B.RESERVATION_ID AND A.RESERVATION_ID = %s" % (id))
    cursor.execute(sql)
    roomtable = cursor.fetchall()
    sql = ("SELECT M.ACTION_ID, M.SERVICE_ID, O.RESERVATION_ID, N.NAME, M.ROOM_ID, M.SERVICE_ACTIVE FROM ROOM_HB_SERV_RECEIVES M, SERVICES N, HOTEL_BILL O WHERE M.SERVICE_ID = N.SERVICE_ID AND O.BILL_ID = M.BILL_ID AND O.RESERVATION_ID = %s" %(id))
    cursor.execute(sql)
    servicetable = cursor.fetchall()
    cursor.close()

    res = {}
    res['resid'] = roomtable[0][5]
    res['arrivaldate'] = roomtable[0][0].date()
    res['departuredate'] = roomtable[0][1].date()
    res['resactive'] = roomtable[0][2]

    room = []
    for row in roomtable:
        r = {}
        r['roomid'] = row[4]
        r['type'] = row[6]
        r['capacity'] = row[7]
        room.append(r)

    res['rooms'] = sorted(room, key=lambda item: int(item['roomid']))
    
    service = []
       
    for row in servicetable:
        s = {}
        s['actionid'] = row[0]
        s['serviceid'] = row[1]
        s['roomid'] = row[4]
        s['name'] = row[3]
        s['isactive'] = row[5]
        service.append(s)

    res['services'] = sorted(service, key=lambda item: int(item['serviceid']))
    return res


def getallres():
    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT * FROM RESERVATION WHERE USER_ID=%s AND RESERVATION_ACTIVE IN (0, 1, 2, 3)" % id)
    cursor.execute(sql)
    table = cursor.fetchall()
    cursor.close()

    data = []
    for row in table:
        res = {}
        res['resid'] = row[0]
        res['guest_no'] = row[1]
        res['arrivaldate'] = row[2].date()
        res['departuredate'] = row[3].date()
        res['isactive'] = row[4]
        data.append(res)
    
    data = sorted(data, key=lambda item: int(item['resid']))
    return data

        