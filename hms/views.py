from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
from hms import hashing
from hms import funcs


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


def insert(request):
    if(conf.login and (conf.role != 'manager' and conf.role != 'director')):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    cursor = connection.cursor()
    sql = "SELECT count(*) FROM ACCOUNT_HOLDER"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    r = result
    (count,) = r[0]
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
    if(conf.role != 'manager' and conf.role != 'director'):
        conf.role_set('customer')

    if(conf.role == 'manager' or conf.role == 'director'):
        position = request.POST.get('position', '')
        if(position == "MANAGER"):
            permission = 2
        else:
            permission = 3
        salary = request.POST.get('salary', '')
        workd = request.POST.get('workd', '')
        print(position)
        
    else:
        idcard = request.POST.get('idcard', '')
        credit = request.POST.get('creditcard', '')
        passport = request.POST.get('passport', '')

    if(password == repassword):
        cursor = connection.cursor()
        sql = "INSERT INTO LOG_IN VALUES(%s, %s, %s)"
        password = hashing.hash_password(password)
        role = 'customer'
        if(conf.role == 'manager' or conf.role == 'director'):
            role = 'employee'
        cursor.execute(sql, [email, password, role])
        sql1 = "INSERT INTO ACCOUNT_HOLDER VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql1, [count + 1, email, name, lastname, house, road, city, country])
        phnumber = funcs.split(phnumber)
        for i in phnumber:
            s = funcs.rspace(i)
            sql2 = "INSERT INTO ACCOUNT_HOLDER_PHNUMBER VALUES(%s, %s)"
            cursor.execute(sql2, [count + 1, int(s)])
        if(conf.role == 'manager' or conf.role == 'director'):
            print(count + 1, conf.user_id, position, workd, permission, salary)
            sql5 = "INSERT INTO EMPLOYEE VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql5, [count + 1, conf.user_id, position, workd, permission, salary, '', ''])
            
        else:
            sql4 = "INSERT INTO CUSTOMER VALUES(%s, %s, %s, %s)"
            cursor.execute(sql4, [count + 1, idcard, credit, passport])

        connection.commit()
        cursor.close()
        return render(request, 'index.html', {'loginid': count + 100, 'login': conf.login, 'sign': True, 'user': conf.getuser()})

    return render(request, 'signup.html', {'sign': False})


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
    sql = "SELECT * FROM LOG_IN"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
#  hashing.verify_password(r[1], password)
    for r in result:
        if(r[0] == email and  hashing.verify_password(r[1], password) and r[2] == Atype):
            
            conf.role = 'customer'
            conf.login = True
            cursor = connection.cursor()
            e = (str("\'"+(r[0])+"\'"))
            sql = ("SELECT * FROM ACCOUNT_HOLDER WHERE LOGIN_EMAIL=%s" %e)
           
            try:
                cursor.execute(sql)
            except :
                return render(request, 'login.html', {'login' : conf.login, 'user' : conf.getuser()})
            us = cursor.fetchall()
            conf.user_id = us[0][0]
            conf.username = us[0][2]
            conf.name = us[0][2] + ' ' + us[0][3]
            conf.email = us[0][1]
            print(Atype)
            if(Atype == 'employee'):
                conf.role = Atype
                print(conf.role)
                sql = ("SELECT PERMISSION FROM EMPLOYEE WHERE USER_ID=%s" %
                       us[0][0])
                cursor.execute(sql)
                mi = cursor.fetchall()
                print(mi)
                print(mi[0][0])
                if(mi[0][0] == '1'):
                    conf.role = 'director'
                if(mi[0][0] == '2'):
                    conf.role = 'manager'
                    print(conf.role)
            cursor.close()

            #conf.userenter(us[0][0], r[1], us[0][2], em[0])
            #print('this is name after doing log in ', conf.name)
            return render(request, 'index.html', {'login' : conf.login, 'logins' : True, 'user' : conf.getuser()})
    return render(request, 'login.html', {'login' : conf.login, 'user' : conf.getuser()})


def delete(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'delete.html', {'login' : conf.login, 'user' : conf.getuser()})

def edit(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    if(conf.role == 'customer'):
        return render(request, 'edit.html', {'login' : conf.login, 'customer' : True, 'user' : conf.getuser()})
    return render(request, 'edit.html', {'login' : conf.login,  'user' : conf.getuser()})

