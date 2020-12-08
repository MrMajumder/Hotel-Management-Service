from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from hms import conf
from datetime import datetime
import time 

# Create your views here.
def profile(request, id, fire = None):
    if(conf.login == False or conf.role == 'customer'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    id = int(id)
    dict_result = getemployeedata(id)
    
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result, 'fire' : fire})

def resmanage(request, id):
    if(conf.login == False or conf.role == 'customer'  or conf.role == 'employee' or id > 1 or id < 0):
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

def servmanage(request, id, scancel = None):
    if(conf.login == False or conf.role == 'customer' or id > 1 or id < 0):
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

def empmanage(request, mode, fire = None, esign = None):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee' or mode < 0 or mode > 1):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    id = int(conf.user_id)
    sql = "SELECT X.USER_ID, (X.FIRST_NAME || ' ' || X.LAST_NAME), Y.POSITION FROM ACCOUNT_HOLDER X, EMPLOYEE Y WHERE X.USER_ID = Y.USER_ID AND X.LOGIN_EMAIL IS NOT NULL AND X.USER_ID <>" + str(id)
    msg = "Showing results for : all employees "
    if(conf.role == 'manager'):
        sql = sql + " AND Y.MANAGER_ID = " + str(id)
        msg = msg + "under manager id : " + str(id) 
    
    if(mode == 1):
        emptype = request.POST.get('emptype', '')
        empid = request.POST.get('empid', '')
        if(emptype != 'All'):
            sql = sql + " AND Y.POSITION = " + str("\'" + emptype + "\'")
        msg = msg + " and employee type: " + str(emptype)
        if(empid != ''):
            sql = sql + " AND X.USER_ID = " + str(empid)
            msg = msg + " and employee id : " + str(empid)
    
    cursor = connection.cursor()
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
    
    dict_result = sorted(dict_result, key=lambda item: int(item['user_id']))
    
    return render(request, 'employee/empmanage.html', {'login' : conf.login, 'employees': dict_result, 'msg' : msg, 'user' : conf.getuser(), 'fire' : fire, 'esign' : esign})

#---------------------------
#This  part is untouched yet
#---------------------------

def hoteloverview(request, id, ent = None, delete = None, update = None):
    if(conf.login == False or conf.role == 'customer' or conf.role == 'employee' or id < 0 or id > 5):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    if(id < 2):     #rooms, id = 0: all, id = 1: query
        sql = "SELECT ROOM_ID, ROOM_TYPE, CAPACITY, RESERVATION_ID FROM ROOM"
        msg = "Showing results for rooms "
        
        if(id == 1):
            roomtype = request.POST.get('roomtype', '')
            vacancy = request.POST.get('vacancy', '')
            if((roomtype and roomtype != 'All') or (vacancy and vacancy != 'All')):
                sql = sql + " WHERE "
                msg = msg + " where "
            if(roomtype != 'All'):
                sql = sql + " ROOM_TYPE = " + str("\'" + roomtype + "\'")
                msg = msg + " room type : " + str(roomtype)
            else:
                msg = msg + "room type : All "
            if((roomtype and roomtype != 'All') and (vacancy and vacancy != 'All')):
                sql = sql + " AND "
                msg = msg + " and "
            if(vacancy == 'Vacant'):
                sql = sql + " RESERVATION_ID IS NULL "
                msg = msg + " room type : vacant "
            elif(vacancy == "Not Vacant"):
                sql = sql + " RESERVATION_ID IS NOT NULL "
                msg = msg + " room type : not vacant " 
            else:
                msg = msg + "room type : All "

        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        data = []

        for r in result:
            room_id     = r[0]
            rtype       = r[1]
            capacity    = r[2]
            vacant      = r[3]
            row = {'room_id': room_id, 'type': rtype, 'capacity': capacity, 'isvacant' : vacant}
            data.append(row)
        
        data = sorted(data, key=lambda item: int(item['room_id']))
        mode = 'room'
    elif(id < 4):   #income, id = 2: all, id = 3: query
        sql = "SELECT A.BILL_ID, B.BILL_DATE, A.RESERVATION_ID, B.COST, A.DUE, (B.COST - A.DUE) FROM HOTEL_BILL A, BILL B WHERE A.BILL_ID = B.BILL_ID"
        msg = "Showing results for income records "

        if(id == 3):
            billid = request.POST.get('billid', '')
            date = request.POST.get('date', '')
            msg = msg + " where "
            if(billid):
                sql = sql + " AND A.BILL_ID = " + str(billid)
                msg = msg + "bill id : " + str(billid)
            if(date):
                sql = sql + " AND TRUNC(B.BILL_DATE) = TO_DATE(" + str("\'" + date + "\', 'YYYY-MM-DD') ")
                msg = msg + " bill date = " + str("\"" + date + "\"")
            
        
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        record = []
        totalcost = 0

        for r in result:
            d = {}
            d['billid'] = r[0]
            d['date'] = r[1].date()
            d['resid'] = r[2]
            d['cost'] = r[3]
            d['due'] = r[4]
            d['income'] = r[5]
            totalcost = totalcost + int(r[5])
            record.append(d)
        
        record = sorted(record, key=lambda item: int(item['billid']))
        data = {}
        data['data'] = record
        data['totalcost'] = totalcost
        mode = 'income'
    else:           #expense, id = 4: all, id = 5: query
        sql = "SELECT A.BILL_ID, B.BILL_DATE, A.EXPENSE_TYPE, A.DESCRIPTION, A.USER_ID, B.COST FROM EXPENSES A, BILL B WHERE A.BILL_ID = B.BILL_ID"
        msg = "Showing results for expense records "

        if(id == 5):
            billid = request.POST.get('billid', '')
            empid = request.POST.get('empid', '')
            date = request.POST.get('date', '')
            if(billid):
                sql = sql + " AND A.BILL_ID = " + str(billid)
                msg = msg + " and bill id : " + str(billid)
            if(empid):
                sql = sql + " AND A.USER_ID = " + str(empid)
                msg = msg + " and employee id : " + str(empid)
            if(date):
                sql = sql + " AND TRUNC(B.BILL_DATE) = TO_DATE(" + str("\'" + date + "\', 'YYYY-MM-DD') ")
                msg = msg + " and bill date = " + str("\"" + date + "\"")
        
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        record = []
        totalcost = 0

        for r in result:
            d = {}
            d['billid'] = r[0]
            d['date'] = r[1].date()
            d['type'] = r[2]
            d['desc'] = r[3]
            d['uid'] = r[4]
            d['cost'] = r[5]
            totalcost = totalcost + int(r[5])
            record.append(d)
        
        record = sorted(record, key=lambda item: int(item['billid']))
        data = {}
        data['data'] = record
        data['totalcost'] = totalcost
        mode = 'expense'

    return render(request, 'employee/hoteloverview.html', {'login' : conf.login, 'user' : conf.getuser(), 'data' : data, 'mode' : mode, 'msg' : msg, 'delete' : delete, 'ent' : ent, 'update':update})

def expense(request):
    if(conf.login == False or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/expense.html', {'login' : conf.login, 'mindate':conf.today, 'user' : conf.getuser()})


def exentry(request):
    if(conf.login == False or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    extype = request.POST.get('extype', '')
    exdes = request.POST.get('exdes', 'default')
    excost = request.POST.get('excost', 'default')
    exdate = request.POST.get('exdate', 'default')
    cursor = connection.cursor()
    cursor.callproc("NEW_EXPENSE_ENTRY", [conf.user_id, excost, extype, exdes, exdate])
    cursor.close()
    return render(request, 'employee/expense.html', {'login' : conf.login, 'mindate':conf.today, 'user' : conf.getuser(), 'exsuccess' : True})


def fire(request, id):
    if(conf.login == False or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    inputt = cursor.var(int).var
    cursor.callproc("FIRE_EMPLOYEE", [id, inputt])
    output = inputt.getvalue()
    cursor.close()
    if output == 1:
        return empmanage(request, 0, True, False)
    else:
        return profile(request, int(id), True)
    

def workh(request, id):
    if(conf.login == False or conf.role == 'customer' or id < 0 or id > 1):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    
    sql = "SELECT * FROM WORK_HISTORY WHERE USER_ID = " + str(conf.user_id)
    msg = "Showing results for salary records "
    
    if(id == 1):
        month = request.POST.get('month', '')
        year = request.POST.get('year', '')
        if(month or year):
            if(month):
                sql = sql + " AND MONTH = " + str("\'" + month + "\'")
                msg = msg + " , month : " + str(month)
            if(year):
                sql = sql + " AND YEAR = " + str("\'" + year + "\'")
                msg = msg + " , year : " + str(year)

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    dic = {}
    data = []
    totalcost = 0

    for r in result:
        month       = r[1]
        year        = r[2]
        salary      = r[3]
        row = {'month': month, 'year': year, 'salary': salary}
        totalcost = totalcost + int(r[3])
        data.append(row)
    
    data = sorted(data, key=lambda item: int(item['room_id']))
    dic['data'] = data
    dic['totalcost'] = totalcost
    return render(request, 'employee/workh.html', {'login' : conf.login, 'data' : data, 'msg' : msg, 'user' : conf.getuser()})

def serveEx(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/serveEx.html', {'login' : conf.login, 'user' : conf.getuser()})

#---------------------------
#This bottom part is updated
#---------------------------


def eattend(request, empid):
    if(conf.login == False or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    data = getemployeeworkinfo(empid)

    return render(request, 'employee/eattend.html', {'login' : conf.login, 'user' : conf.getuser(), 'data' : data})

def empsalary(request, id):
    if(conf.login == False or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    cursor = connection.cursor()
    out = cursor.var(int).var
    cursor.callproc("SALARY_PAY", [conf.user_id, id, out])
    output = out.getvalue()
    cursor.close()
    id = int(id)
    dict_result = getemployeedata(id)
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result, 'fire' : fire, 'output' : output})
   

def eprochange(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    empid = request.POST.get('id', '')
    salary = request.POST.get('salary', '')
    poschange = request.POST.get('poschange', '')
    workd = request.POST.get('workd', '')
    if(poschange == "No change"):
        poschange = ''
    cursor = connection.cursor()
    cursor.callproc("EMP_PROFILE_EDIT", [empid, salary, poschange, workd])
    cursor.close()
    # return render(request, 'employee/profile/'+empid+'/.html', {'login' : conf.login, 'user' : conf.getuser(), 'prsuccess' : True})
    if(empid == ''):
        empid = id
    dict_result = getemployeedata(int(empid))
    
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result, 'epsuccess' : True})


    


def eproedit(request, empid):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    data = getemployeeworkinfo(empid)
    return render(request, 'employee/empedit.html', {'login' : conf.login, 'user' : conf.getuser(), 'data' : data})


def roomdelete(request, id):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee' or conf.role == 'manager'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    cursor.callproc("ROOM_DELETE", [id])
    cursor.close()
    return hoteloverview(request, 0, False, True, False)

def roomform(request):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee' or conf.role == 'manager'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/roomform.html', {'login' : conf.login, 'user' : conf.getuser()})


def roomentry(request):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee' or conf.role == 'manager'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    rtype = request.POST.get('rtype', '')
    rent = request.POST.get('rent', '')
    floor = request.POST.get('floor', '')
    build = request.POST.get('building', '')
    capacity = request.POST.get('capa', '')
    bed = request.POST.get('bed', '')
    ac = request.POST.get('ac','')
    cursor = connection.cursor()
    cursor.callproc("ROOM_ENTRY", [build, floor, capacity, bed, rent, rtype, ac])
    cursor.close()
    return hoteloverview(request, 0, True, False, False)


def comp(request, id, alert = None):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee' ):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    sql = "SELECT * FROM COMPLAIN WHERE CHECKK = 0"

    if(id == 1):
        comtype = request.POST.get('comtype', '')
        if(comtype != 'All'):
            comtype = (str("\'"+comtype+"\'"))
            sql = sql + (" AND COMPTYPE = %s" % comtype)

    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        comp_id = r[0]
        cus_id = r[1]
        complain = r[2]
        comtype = r[3]
        cdate = r[4]
        row = {'comp_no': comp_id, 'cusid': cus_id, 'complain': complain, 'comtype' : comtype, 'compdate' : cdate}
        dict_result.append(row)
    

    conf.ncount = len(dict_result)
    dict_result = sorted(dict_result, key=lambda item: int(item['comp_no']))
    return render(request, 'employee/complains.html', {'login' : conf.login, 'user' : conf.getuser(), 'complains' : dict_result, 'alert' : alert})

def comresolve(request, id):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    sql = ("UPDATE COMPLAIN SET CHECKK = 1 WHERE COMP_ID = %s" %int(id))
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    return comp(request, True)


def updateroom(request, id):
    if(conf.login == False  or conf.role == 'customer' or conf.role == 'employee' or conf.role == 'manager'):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})


    rtype = request.POST.get('roomtype', '')
    capacity = request.POST.get('capacity', '')
    air = request.POST.get('air', '')
    bed = request.POST.get('bed', '')
    rent = request.POST.get('rent', '')
    cursor = connection.cursor()
    cursor.callproc("UPDATE_ROOM", [int(id), rtype, capacity, air, bed, rent])
    cursor.close()
    return hoteloverview(request, 0, False, False, True)
    


def getemployeeworkinfo(empid):
    cursor = connection.cursor()
    sql = "SELECT X.USER_ID, (X.FIRST_NAME || ' ' || X.LAST_NAME), Y.POSITION, Y.BASE_SALARY, Y.WORK_DESCRIPTION FROM ACCOUNT_HOLDER X, EMPLOYEE Y WHERE X.USER_ID = Y.USER_ID AND X.USER_ID =" + str(empid)
    cursor.execute(sql)
    table = cursor.fetchall()
    cursor.close()

    data = {}
    data['empid'] = table[0][0]
    data['name'] = table[0][1]
    data['position'] = table[0][2]
    data['prevsal'] = table[0][3]
    data['workdesc'] = table[0][4]

    return data

def getemployeedata(id):
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

    return dict_result

