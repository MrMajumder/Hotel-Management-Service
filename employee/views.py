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

def resmanage(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    
    cursor = connection.cursor()
    sql = ("SELECT RESERVATION_ID, USER_ID, RESERVATION_ACTIVE FROM RESERVATION")
    cursor.execute(sql)
    table = cursor.fetchall()

    cursor.close()

    data = []
    for row in table:
        res = {}
        res['resid'] = row[0]
        res['cusid'] = row[1]
        res['isactive'] = row[2]
        data.append(res)

    data = sorted(data, key=lambda item: int(item['resid']))

    return render(request, 'reservation/allres.html', {'login' : conf.login, 'data': data, 'user' : conf.getuser()})

def servmanage(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    cursor = connection.cursor()
    sql = ("SELECT * FROM ROOM_HB_SERV_RECEIVES")
    cursor.execute(sql)
    table = cursor.fetchall()

    cursor.close()

    data = []
    for row in table:
        res = {}
        res['servid'] = row[0]
        res['roomid'] = row[1]
        res['billid'] = row[2]
        res['isactive'] = row[3]
        res['actionid'] = row[4]
        data.append(res)
    
    data = sorted(data, key=lambda item: int(item['servid']))

    return render(request, 'service/allserv.html', {'login' : conf.login, 'data': data, 'user' : conf.getuser()})

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
    today = str(time.strftime("%Y-%m-%d"))
    print(today)
    return render(request, 'employee/expense.html', {'login' : conf.login, 'mindate':today, 'user' : conf.getuser()})

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

def mansalary(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def eproedit(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/empedit.html', {'login' : conf.login, 'user' : conf.getuser()})

def empdetails(request, id):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/empdetails.html', {'login' : conf.login, 'empid' : id, 'user' : conf.getuser()})
    
