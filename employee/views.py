from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from hms import conf
from datetime import datetime
import time 

# Create your views here.
def profile(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    id = int(id)
    cursor = connection.cursor()
    sql = ("SELECT * FROM ACCOUNT_HOLDER X, ACCOUNT_HOLDER_PHNUMBER Y, EMPLOYEE Z WHERE X.USER_ID=%s AND X.USER_ID = Y.USER_ID AND X.USER_ID = Z.USER_ID" % id)
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
    dict_result['manager_id'] = acholder[0][11]
    dict_result['position'] = acholder[0][12]
    dict_result['work_description'] = acholder[0][13]
    dict_result['salary'] = acholder[0][15]

    ph_no = []
    for ph in acholder:
        num = ph[9]
        row = {'phone_no' : num}
        ph_no.append(row)
    dict_result['phone_nums'] = ph_no
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result})

def resmanage(request, id):
    if(conf.login == False or id > 1 or id < 0):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    sql = ("SELECT RESERVATION_ID, RESERVATION_ACTIVE, ARRIVAL_DATE, DEPARTURE_DATE, USER_ID FROM RESERVATION ")
    msg = "Showing results for : all reservations "
    if(id == 1):
        arrdate = request.POST.get('arrdate', '')
        depdate = request.POST.get('depdate', '')
        restype = request.POST.get('restype', '')

        if(arrdate or depdate or restype):
            msg = msg + " with"
            sql = sql + " WHERE "
            if(arrdate):
                sql = sql + " ARRIVAL_DATE >= TO_DATE(" + str("\'" + arrdate + "\', 'YYYY-MM-DD') ")
                msg = msg + " arrival date >= " + str("\"" + arrdate + "\", ")
            if(arrdate and depdate):
                sql = sql + " AND "
            if(depdate):
                sql = sql + " DEPARTURE_DATE <= TO_DATE(" + str("\'" + depdate + "\', 'YYYY-MM-DD') ")
                msg = msg + " departure date <= " + str("\"" + depdate + "\", ")
            if(restype and restype != 'All' and depdate):
                sql = sql + " AND "
            if(restype == 'Active'):
                sql = sql + "  RESERVATION_ACTIVE = 1 "
                msg = msg + " type = Active "
            elif(restype == 'Pending'):
                sql = sql + " RESERVATION_ACTIVE = 0 "
                msg = msg + " type = Inactive "
            elif(restype == 'Cancelled'):
                sql = sql + " RESERVATION_ACTIVE = 2 "
                msg = msg + " type = Cancelled "
            elif(restype == 'Completed'):
                sql = sql + " RESERVATION_ACTIVE = 3 "
                msg = msg + " type = Completed "
            else:
                msg = msg + " type = All "
    cursor = connection.cursor()
    print('baler dynamic sql ta dekhe nao ', sql)
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

def servmanage(request, id, scancel=None):
    if(conf.login == False or id > 1 or id < 0):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    sql = "SELECT * FROM ROOM_HB_SERV_RECEIVES "
    msg = "Showing results for : all reservations "
    if(id == 1):
        serdate = request.POST.get('servdate', '')
        sertype = request.POST.get('sertype', '')

        if(serdate or (sertype and sertype != 'All')):
            msg = msg + " with"
            sql = sql + " WHERE "
            if(serdate):
                sql = sql + " TRUNC(SERVICE_DATE) = TO_DATE(" + str("\'" + serdate + "\', 'YYYY-MM-DD') ")
                msg = msg + " service execution date = " + str("\"" + serdate + "\", ")
            if(serdate and sertype and sertype != 'All'):
                sql = sql + " AND "
            if(sertype == 'Active'):
                sql = sql + " SERVICE_ACTIVE = 1 "
                msg = msg + " type = Active "
            elif(sertype == 'Cancelled'):
                sql = sql + " SERVICE_ACTIVE = 2 "
                msg = msg + " type = Cancelled "
            elif(sertype == 'Completed'):
                sql = sql + " SERVICE_ACTIVE = 3 "
                msg = msg + " type = Completed "
            else:
                msg = msg + " type = All "
            if(conf.role != 'manager' and conf.role != 'director'):
                sql = sql + " AND EMP_ID = " + str(conf.user_id)
        else:
            if(conf.role != 'manager' and conf.role != 'director'):
                sql = sql + " WHERE EMP_ID = " + str(conf.user_id)
    else:
        if(conf.role != 'manager' and conf.role != 'director'):
            sql = sql + " WHERE EMP_ID = " + str(conf.user_id)
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

    return render(request, 'service/allserv.html', {'login' : conf.login,'data' : data, 'msg' : msg,  'scancel': scancel, 'user' : conf.getuser()})

def empreg(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/empreg.html', {'login' : conf.login, 'user' : conf.getuser()})

def empmanage(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = "SELECT X.USER_ID, (X.FIRST_NAME || ' ' || X.LAST_NAME), Y.POSITION FROM ACCOUNT_HOLDER X, EMPLOYEE Y WHERE X.USER_ID = Y.USER_ID AND X.USER_ID <>" + str(id)
    if(conf.role == 'manager'):
        sql = sql + " AND Y.MANAGER_ID = " + str(id)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        user_id = r[0]
        name = r[1]
        position = r[2]
        row = {'user_id': user_id, 'name': name, 'position': position}
        dict_result.append(row)
    
    return render(request, 'employee/empmanage.html', {'login' : conf.login, 'employees': dict_result, 'user' : conf.getuser()})

def hoteloverview(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/hoteloverview.html', {'login' : conf.login, 'user' : conf.getuser()})

def expense(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/expense.html', {'login' : conf.login, 'mindate':conf.today, 'user' : conf.getuser()})


def exentry(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    extype = request.POST.get('extype', '')
    exdes = request.POST.get('exdes', 'default')
    excost = request.POST.get('excost', 'default')
    exdate = request.POST.get('exdate', 'default')
    cursor = connection.cursor()
    cursor.callproc("NEW_EXPENSE_ENTRY", [conf.user_id, excost, extype, exdes, exdate])
    cursor.close()
    return render(request, 'employee/expense.html', {'login' : conf.login, 'mindate':conf.today, 'user' : conf.getuser(), 'exsuccess' : True})


def eattend(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/eattend.html', {'login' : conf.login, 'user' : conf.getuser()})

def fire(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/fire.html', {'login' : conf.login, 'user' : conf.getuser()})
    

def workh(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/workh.html', {'login' : conf.login, 'user' : conf.getuser()})

def serveEx(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/serveEx.html', {'login' : conf.login, 'user' : conf.getuser()})

def empsalary(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def empsalaryentry(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    empid = request.POST.get('empid', '')
    salary = request.POST.get('salary', '')
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def mansalary(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def eproedit(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/empedit.html', {'login' : conf.login, 'user' : conf.getuser()})

def eprochange(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    empid = request.POST.get('id', '')
    salary = request.POST.get('salary', '')
    poschange = request.POST.get('poschange', '')
    if(poschange == "No change"):
        poschange = ''
    cursor = connection.cursor()
    cursor.callproc("EMP_PROFILE_EDIT", [empid, salary, poschange])
    cursor.close()
    return render(request, 'employee/empedit.html', {'login' : conf.login, 'user' : conf.getuser(), 'prsuccess' : True})

def empdetails(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/empdetails.html', {'login' : conf.login, 'empid' : id, 'user' : conf.getuser()})
    
