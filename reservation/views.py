from django.shortcuts import render
from django.db import connection
from hms import conf

# Create your views here.


def solores(request, id):
    if(conf.login == False):
       return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser()})

    cursor = connection.cursor()
    sql = ("SELECT RESERVATION.*, GETROOMS(%s), GETSERV(%s), GETSERVROOMS(%s), GETSERVACTIONID(%s) FROM RESERVATION WHERE RESERVATION_ID = %s" % (id, id, id, id, id))
    cursor.execute(sql)
    row = cursor.fetchall()

    res = {}
    res['resid'] = row[0][0]
    res['guest_no'] = row[0][1]
    res['arrivaldate'] = row[0][2]
    res['departuredate'] = row[0][3]
    res['resactive'] = row[0][4]

    if not row[0][6]:
        res['roomcnt'] = '0'
    if not row[0][7]:
        res['servcnt'] = '0'

    rooms = row[0][6]
    if not rooms:
        res['rooms'] = []
    else:
        rooms = rooms.split(',')
        res['rooms'] = [int(room) for room in rooms]
    res['rooms'] = sorted(res['rooms'])
    service = []
    res['services'] = []
    if  row[0][7]:
        service.append([int(x) for x in (row[0][7].split(','))])
        service.append([int(x) for x in (row[0][8].split(','))])
        service.append([int(x) for x in (row[0][9].split(','))])
       
        for i in range(len(service[0])):
            s = {}
            s['actionid'] = service[2][i]
            s['serviceid'] = service[0][i]
            s['roomid'] = service[1][i]
            res['services'].append(s)

    res['services'] = sorted(res['services'], key=lambda item: int(item['serviceid']))

    return render(request, 'reservation/resview.html', {'login' : conf.login, 'res' : res, 'user' : conf.getuser()})




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

        