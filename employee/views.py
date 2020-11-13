from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from hms import conf
from datetime import datetime
import time 

# Create your views here.
def profile(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})

    id = int(conf.user_id)
    cursor = connection.cursor()
    sql = ("SELECT * FROM ACCOUNT_HOLDER WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    acholder = cursor.fetchall()

    sql = ("SELECT * FROM ACCOUNT_HOLDER_PHNUMBER WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    acholderph = cursor.fetchall()

    sql = ("SELECT * FROM EMPLOYEE WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    employee = cursor.fetchall()

    cursor.close()
    dict_result = {} 
    
    dict_result['user_id'] = acholder[0][0]
    dict_result['email'] = acholder[0][1]
    dict_result['username'] = acholder[0][2]
    dict_result['name'] = acholder[0][2] + ' ' + acholder[0][3]
    dict_result['house_no'] = acholder[0][4]
    dict_result['road_no'] = acholder[0][5]
    dict_result['city'] = acholder[0][6]
    dict_result['country'] = acholder[0][7]
    dict_result['manager_id'] = employee[0][1]
    dict_result['position'] = employee[0][2]
    dict_result['work_description'] = employee[0][3]
    dict_result['salary'] = employee[0][5]

    ph_no = []
    for ph in acholderph:
        num = ph[1]
        row = {'phone_no' : num}
        ph_no.append(row)
    dict_result['phone_nums'] = ph_no
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result})

def resmanage(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'reservation/allres.html', {'login' : conf.login, 'data': [1, 3, 5, 6, 7, 9, 10, 15, 26, 28, 35, 37], 'user' : conf.getuser()})

def servmanage(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'service/allserv.html', {'login' : conf.login, 'data': [1, 3, 5, 6, 7, 9, 10, 15, 26, 28, 35, 37], 'user' : conf.getuser()})

def empreg(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'employee/empreg.html', {'login' : conf.login, 'user' : conf.getuser()})

def empmanage(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    cursor = connection.cursor()
    sql = "SELECT * FROM EMPLOYEE"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        user_id = r[0]
        first_name = r[3]
        position = r[2]
        
        row = {'user_id': user_id, 'first_name': first_name, 'position': position}
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
    
