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
