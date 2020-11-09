from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf
from hms import hashing
from hms import funcs

def index(request):
    return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

def contact(request):
    return render(request, 'contact.html', {'login' : conf.login, 'user' : conf.getuser()})

def signup(request):
    if(conf.login == True and conf.role == 'manager'):
        return render(request, 'signup.html', {'login' : conf.login, 'sign' : True, 'user' : conf.getuser(), 'manager' : True})
    if(conf.login == False):
        return render(request, 'signup.html', {'login' : conf.login, 'sign' : True, 'user' : conf.getuser()})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def about(request):
    return render(request, 'about.html', {'login' : conf.login, 'user' : conf.getuser()})

def insert(request):
    if(conf.login and conf.role != 'manager'):
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
    idcard = request.POST.get('idcard', '')
    credit = request.POST.get('creditcard', '')
    passport = request.POST.get('passport', '')
    city = request.POST.get('city', '')
    country = request.POST.get('country', '')
    house = request.POST.get('house', '')
    road = request.POST.get('road', '')
    if(conf.role != 'manager'):
        conf.role_set('customer')
    
    if(conf.role == 'manager'):
        position = request.POST.get('position', '')
        permission = request.POST.get('permission', 'NO')
        salary = request.POST.get('salary', '')
        mid = request.POST.get('mid', '')
        workd = request.POST.get('workd', '')
        print(position)
        print(permission)
    
    if(password == repassword):
        cursor = connection.cursor()
        sql = "INSERT INTO LOG_IN VALUES(%s, %s, %s, %s)"
        password = hashing.hash_password(password)
        # print(password)
        role = 'customer'
        if(conf.role == 'manager'):
            role = 'employee'
        cursor.execute(sql, [count + 100, name, password, role])
        sql1 = "INSERT INTO ACCOUNT_HOLDER VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql1, [count + 1, count + 100, name, lastname, house, road, city, country])
        phnumber = funcs.split(phnumber)
        for i in phnumber:
            s = funcs.rspace(i)
            # print(s)
            sql2="INSERT INTO ACCOUNT_HOLDER_PHNUMBER VALUES(%s, %s)"
            cursor.execute(sql2, [count + 1, int(s)])
        sql3 = "INSERT INTO ACCOUNT_HOLDER_EMAIL VALUES(%s, %s)"
        cursor.execute(sql3, [count + 1, email])
        sql4 = "INSERT INTO CUSTOMER VALUES(%s, %s, %s, %s)"
        cursor.execute(sql4, [count + 1, idcard, credit, passport])
        if(conf.role == 'manager'):
            sql5 = "INSERT INTO EMPLOYEE VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql5, [count + 1, mid, position, workd, permission, salary, '', ''])
            print('hello2')

        connection.commit()
        cursor.close()
        return render(request, 'index.html', {'loginid' :count + 100, 'login' : conf.login, 'sign' : True, 'user' : conf.getuser()})

    return render(request, 'signup.html', {'sign' : False})
    
def login(request):
    if(conf.login == False):
        #print('i am inside the right jayga')
        return render(request, 'login.html', {'login' : conf.login, 'alerttoggle' : True, 'user' : conf.getuser()})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout(request):
    if(conf.login):
        conf.login = False        
        conf.user_id = conf.username = conf.name = conf.email = conf.role = ''
    return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

def enter_account(request):
    if(conf.login == True):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    id = request.POST.get('id', 'default')
    password = request.POST.get('password', 'default')
    Atype = request.POST.get('AcCheck', 'default')
    id = int(id)
    cursor = connection.cursor()
    sql = "SELECT * FROM LOG_IN"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    cursor.close()

    for r in result:
        if(r[0] == id and hashing.verify_password(r[2], password) and r[3] == Atype):
            conf.role = 'customer'
            conf.login = True
            cursor = connection.cursor()
            sql = ("SELECT * FROM ACCOUNT_HOLDER WHERE LOGIN_ID=%s" %r[0])
            cursor.execute(sql)
            us = cursor.fetchall()
            sql = ("SELECT EMAIL FROM ACCOUNT_HOLDER_EMAIL WHERE USER_ID=%s" %us[0][0])
            cursor.execute(sql)
            em = cursor.fetchall()
            conf.user_id = us[0][0]
            conf.username = r[1]
            conf.name = us[0][2]
            conf.email = em[0][0]
            print(Atype)
            if(Atype == 'employee'):
                conf.role = Atype
                print(conf.role)
                sql = ("SELECT PERMISSION FROM EMPLOYEE WHERE USER_ID=%s" %us[0][0])
                cursor.execute(sql)
                mi = cursor.fetchall()
                print(mi)
                print(mi[0][0])
                if(mi[0][0] == 'YES'):
                    conf.role = 'manager'
                    print(conf.role)
            cursor.close()
            
            #conf.userenter(us[0][0], r[1], us[0][2], em[0])
            #print('this is name after doing log in ', conf.name)
            return render(request, 'index.html', {'login' : conf.login, 'logins' : True, 'user' : conf.getuser()})
    return render(request, 'login.html', {'login' : conf.login, 'user' : conf.getuser()})
