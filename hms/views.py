from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
from hms import hashing
from hms import funcs
from employee import views
from datetime import datetime


def index(request):
    return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser()})


def contact(request):
    return render(request, 'contact.html', {'login': conf.login, 'user': conf.getuser()})


def signup(request):
    if(conf.login == True and (conf.role == 'manager' or conf.role == 'director')):
        return render(request, 'signup.html', {'login': conf.login, 'sign': True, 'user': conf.getuser(), 'ementry': True})
    if(conf.login == False):
        return render(request, 'signup.html', {'login': conf.login, 'sign': True, 'user': conf.getuser()})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'about.html', {'login': conf.login, 'user': conf.getuser()})



def login(request):
    if(conf.login == False):
        #print('i am inside the right jayga')
        return render(request, 'login.html', {'login': conf.login, 'alerttoggle': True, 'user': conf.getuser()})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def roomdetails(request, id):
    if(conf.login == False):
        return render(request, 'login.html', {'login': conf.login, 'alerttoggle': True, 'user': conf.getuser()})

    cursor = connection.cursor()
    sql = ("SELECT * FROM ROOM WHERE ROOM_ID = %s" % (id))
    cursor.execute(sql)
    row = cursor.fetchall()

    room = {}
    room['roomid'] = row[0][0]
    room['building'] = row[0][1]
    room['floor'] = row[0][2]
    room['capacity'] = row[0][3]
    room['ac'] = row[0][4]
    room['bed_no'] = row[0][5]
    room['rent'] = row[0][6]
    room['reservation_id'] = row[0][7]
    room['type'] = row[0][8]

    return render(request, 'roomview.html', {'login': conf.login, 'alerttoggle': True, 'room' : room, 'user': conf.getuser()})

def logout(request):
    if(conf.login):
        conf.login = False
        conf.user_id = conf.username = conf.name = conf.email = conf.role = ''
    return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser()})


def enter_account(request):
    if(conf.login == True):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    email = request.POST.get('email', 'default')
    password = request.POST.get('password', 'default')
    Atype = request.POST.get('AcCheck', 'default')
    cursor = connection.cursor()
    sql = "SELECT * FROM LOG_IN "
    e = (str("\'"+(email)+"\'"))
    sql = ("SELECT A.*, B.* ")
    if(Atype == 'employee'):
         sql = sql + ", (SELECT PERMISSION FROM EMPLOYEE WHERE EMPLOYEE.USER_ID = B.USER_ID) "
    sql = sql + (" FROM LOG_IN A, ACCOUNT_HOLDER B WHERE A.LOGIN_EMAIL = B.LOGIN_EMAIL AND A.LOGIN_EMAIL = %s" %(e))
    cursor.execute(sql)
    r = cursor.fetchall()
    
    
    if(r and r[0][0] == email and hashing.verify_password(r[0][1], password) and r[0][2] == Atype):
        
        conf.role = Atype
        conf.login = True
        conf.user_id = r[0][3]
        conf.email = r[0][4]
        conf.username = r[0][5]
        conf.name = r[0][5] + ' ' + r[0][6]
        
        if(Atype == 'employee'):
            if(r[0][11] == '1'):
                conf.role = 'director'
            if(r[0][11] == '2'):
                conf.role = 'manager'
        if(conf.role == 'manager' or conf.role == 'director'):
            sql = "SELECT COUNT(*) FROM COMPLAIN WHERE CHECKK = 0"
            cursor.execute(sql)
            r = cursor.fetchall()
            print(r)
            conf.ncount = r[0][0]

        cursor.close()
        return render(request, 'index.html', {'login' : conf.login, 'logins' : True, 'user' : conf.getuser()})
    cursor.close()
    return render(request, 'login.html', {'login' : conf.login, 'user' : conf.getuser()})


def delete(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'delete.html', {'login' : conf.login, 'user' : conf.getuser(), 'employee' : False})
    

def cdelete(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("DELETE_ACCOUNT", [conf.user_id, order_count])
    num = order_count.getvalue()
    cursor.close()
    if num == 1:
        if(conf.login):
            conf.login = False
            conf.user_id = conf.username = conf.name = conf.email = conf.role = ''
        return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser(), 'delete' : True})
    return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser(), 'employee' : False, 'deleteu': True}) 

def edit(request, uid):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    data = getbasicuserinfo(uid)
    data['role'] = conf.role 
    return render(request, 'edit.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser()})


def cedit(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
   
    opass       = request.POST.get('oldpass', '')
    name        = request.POST.get('fname', 'default')
    lastname    = request.POST.get('lname', 'default')
    password    = request.POST.get('pass', 'default')
    repassword  = request.POST.get('repass', 'default')
    phnumber    = request.POST.get('phnumber1', 'default')
    city        = request.POST.get('city', '')
    country     = request.POST.get('country', '')
    house       = request.POST.get('house', '')
    road        = request.POST.get('road', '')
    idcard      = request.POST.get('idcard', '')
    credit      = request.POST.get('creditcard', '')
    passport    = request.POST.get('passport', '')
    
    cursor = connection.cursor()
    sql = "SELECT L.LOGIN_PASSWORD FROM LOG_IN L, ACCOUNT_HOLDER A WHERE L.LOGIN_EMAIL = A.LOGIN_EMAIL AND A.USER_ID = %s" % int(conf.user_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    data = getbasicuserinfo(int(conf.user_id))
    data['role'] = conf.role 
    
    if(password == repassword and  hashing.verify_password(result[0][0], opass)):
        if(password != ""):
            password = hashing.hash_password(password)
        cursor = connection.cursor()
        cursor.callproc("EDIT_ACCOUNT", [conf.user_id, name, lastname, password, house, road, city, country, idcard, credit, passport, phnumber, conf.role])
        
        if phnumber != "":
            phnumber = funcs.split(phnumber)
            for i in phnumber:
                s = funcs.rspace(i)
                cursor.callproc("PH_NUMBER_INSERT", [conf.user_id, int(s)])
            
        cursor.close()
        if name != '':
            conf.username = name

        
        return render(request, 'edit.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser(), 'success' : True})
        
    else:
        return render(request, 'edit.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser(), 'unsuccess' : True})
    
def billshow(request, resid):
    if(conf.login == False):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #do stuff here to show the bill
    data = getbilltable(resid)
    
    return render(request, 'billinfo.html', {'login' : conf.login, 'data' : data, 'user' : conf.getuser()})

def billpay(request, resid):
    if(conf.login == False):
        return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser()})
    pay = request.POST.get('payment', 0)
    print('pay ', pay)
    if pay == '':
        pay = 0
    cursor = connection.cursor()
    success = cursor.callfunc("UPDATEDUE", int, [pay, resid])
    cursor.close()
    data = getbilltable(resid)

    return render(request, 'billinfo.html', {'login' : conf.login, 'success' : success, 'data' : data, 'user' : conf.getuser()})

def getbilltable(resid):
    cursor = connection.cursor()
    sql = ("SELECT C.RESERVATION_ID, C.ARRIVAL_DATE, C.DEPARTURE_DATE, D.FNAME, D.CNO, D.PNO, B.BILL_ID, B.COST, B.BILL_DATE, B.VAT_PERCENTAGE, A.DUE, E.ROOM_ID, E.ROOM_TYPE, E.CAPACITY, E.RENT, C.RESERVATION_ACTIVE FROM HOTEL_BILL A, BILL B, RESERVATION C, (SELECT C.USER_ID USID, (A.FIRST_NAME || ' ' || A.LAST_NAME) FNAME, C.ID_CARD_NO CNO, P.PH_NUMBER PNO FROM CUSTOMER C, ACCOUNT_HOLDER A, ACCOUNT_HOLDER_PHNUMBER P WHERE C.USER_ID = A.USER_ID AND A.USER_ID = P.USER_ID AND ROWNUM <= 1) D, ROOM E, BOOKED_ROOMS F WHERE A.BILL_ID = B.BILL_ID AND A.RESERVATION_ID = C.RESERVATION_ID AND D.USID = C.USER_ID AND C.RESERVATION_ID = F.RESERVATION_ID AND F.ROOM_ID = E.ROOM_ID AND A.RESERVATION_ID = %s" % (resid))
    cursor.execute(sql)
    row = cursor.fetchall()
    sql = ("SELECT M.SERVICE_ID, N.NAME, M.ROOM_ID, N.COST FROM ROOM_HB_SERV_RECEIVES M, SERVICES N, HOTEL_BILL O WHERE M.SERVICE_ID = N.SERVICE_ID AND O.BILL_ID = M.BILL_ID AND M.SERVICE_ACTIVE IN (1, 3) AND O.RESERVATION_ID = %s" % (resid))
    cursor.execute(sql)
    servicetable = cursor.fetchall()
    cursor.close()
    data = {}
    data['resid'] = row[0][0]
    data['arrdate'] = row[0][1].date()
    data['depdate'] = row[0][2].date()
    data['cusname'] = row[0][3]
    data['cusidcard'] = row[0][4]
    data['cusphno'] = row[0][5]
    data['billid'] = row[0][6]
    data['totalcost'] = row[0][7]
    data['billdate'] = row[0][8].date()
    data['vat'] = row[0][9]
    data['due'] = row[0][10]
    data['paid'] = int(data['totalcost']) - int(data['due'])
    data['resactive'] = row[0][15]


    data['rooms'] = []
    for ro in row:
        r = {}
        r['roomid'] = ro[11]
        r['type'] = ro[12]
        r['capacity'] = ro[13]
        r['rent'] = ro[14]
        data['rooms'].append(r)
    
    data['rooms'] = sorted(data['rooms'], key=lambda item: int(item['roomid']))
    
    data['services'] = []
    for ro in servicetable:
        s = {}
        s['servid'] = ro[0]
        s['name'] = ro[1]
        s['roomid'] = ro[2]
        s['cost'] = ro[3]
        data['services'].append(s)

    data['services'] = sorted(data['services'], key=lambda item: int(item['servid']))
    return data

def update_server(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login': conf.login, 'user': conf.getuser()})
    cursor = connection.cursor()
    order_count = cursor.var(int).var
    cursor.callproc("UPDATE_SERVER_DATE", [order_count])
    suc = order_count.getvalue()
    cursor.close()
    if(suc == 1):
        return render(request, 'index.html', {'login' : conf.login, 'server' : True, 'user' : conf.getuser()})

def newinsert1(request):
    if(conf.login and (conf.role != 'manager' and conf.role != 'director')):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    name = request.POST.get('user', 'default')
    lastname = request.POST.get('lastn', 'default')
    password = request.POST.get('pass', 'default')
    repassword = request.POST.get('repass', 'default')
    email = request.POST.get('email', 'default')
    phnumber = request.POST.get('phnumber', 'default')
    city = request.POST.get('city', '')
    country = request.POST.get('country', '')
    house = request.POST.get('house', '')
    road = request.POST.get('road', '')
    position = request.POST.get('position', '')
    salary = request.POST.get('salary', '')
    workd = request.POST.get('workd', '')
    idcard = request.POST.get('idcard', '')
    credit = request.POST.get('creditcard', '')
    passport = request.POST.get('passport', '')
    permission = ''
    if(conf.role != 'manager' and conf.role != 'director'):
        conf.role_set('customer')

    if(conf.role == 'manager' or conf.role == 'director'):
        if(position == "Manager"):
            permission = 2
        else:
            permission = 3
        
    if(password == repassword):
        cursor = connection.cursor()
        password = hashing.hash_password(password)
        role = 'customer'
        if(conf.role == 'manager' or conf.role == 'director'):
            role = 'employee'
        order_count = cursor.var(int).var
        cursor.callproc("INSERT_ACCOUNTHOLDER", [email, name, lastname, password, house, road, city, country, role, idcard, credit, passport, conf.user_id, position, workd, permission, salary,order_count])
        suc = order_count.getvalue()
        if suc == 0:
            if(conf.login == True and (conf.role == 'manager' or conf.role == 'director')):
                return render(request, 'signup.html', {'login': conf.login, 'user': conf.getuser(), 'ementry': True, 'exist': True})
            return render(request, 'signup.html', {'exist': True})
        phnumber = funcs.split(phnumber)
        for i in phnumber:
            s = funcs.rspace(i)
            cursor.callproc("NEW_PH_NUMBER_INSERT", [int(s)])
        cursor.close()
        if(conf.role == 'manager' or conf.role == 'director'):
            return views.empmanage(request, 0, False, True)
        return render(request, 'index.html', {'login': conf.login, 'sign': True, 'user': conf.getuser()})

    return render(request, 'signup.html', {'login': conf.login, 'sign': False, 'user': conf.getuser()})


def getbasicuserinfo(id):
    cursor = connection.cursor()
    sql = "SELECT A.FIRST_NAME, A.LAST_NAME, A.HOUSE_NO, A.ROAD_NO, A.CITY, A.COUNTRY, B.PH_NUMBER FROM ACCOUNT_HOLDER A, ACCOUNT_HOLDER_PHNUMBER B WHERE A.USER_ID = B.USER_ID AND A.USER_ID = " + str(id)
    cursor.execute(sql)
    table = cursor.fetchall()
    cursor.close()

    data = {}
    data['firstname'] = table[0][0]
    data['lastname'] = table[0][1]
    data['house'] = table[0][2]
    data['road'] = table[0][3]
    data['city'] = table[0][4]
    data['country'] = table[0][5]

    phno = []
    for r in table:
        ph = {}
        ph['ph'] = r[6]
        phno.append(ph)

    data['phno'] = phno
    return data