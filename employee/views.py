from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from hms import conf

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

    sql = ("SELECT * FROM ACCOUNT_HOLDER_EMAIL WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    acholderemail = cursor.fetchall()

    sql = ("SELECT * FROM EMPLOYEE WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    employee = cursor.fetchall()

    sql = ("SELECT * FROM LOG_IN WHERE LOGIN_ID=%s" % acholder[0][1])
    cursor.execute(sql)
    xx = cursor.fetchall()

    cursor.close()
    dict_result = {} 
    
    dict_result['user_id'] = acholder[0][0]
    dict_result['username'] = xx[0][1]
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

    emails = []
    for email in acholderemail:
        em = email[1]
        row = {'email' : em}
        emails.append(row)
    dict_result['emails'] = emails
    return render(request, 'employee/profile.html', {'login' : conf.login, 'user' : conf.getuser(), 'allval' : dict_result})

def resmanage(request):
    return render(request, 'employee/resmanage.html', {'login' : conf.login, 'user' : conf.getuser()})

def servmanage(request):
    return render(request, 'employee/servmanage.html', {'login' : conf.login, 'user' : conf.getuser()})

def empreg(request):
    return render(request, 'employee/empreg.html', {'login' : conf.login, 'user' : conf.getuser()})

def empmanage(request):
    return render(request, 'employee/empmanage.html', {'login' : conf.login, 'user' : conf.getuser()})

def hoteloverview(request):
    return render(request, 'employee/hoteloverview.html', {'login' : conf.login, 'user' : conf.getuser()})

def expense(request):
    return render(request, 'employee/expense.html', {'login' : conf.login, 'user' : conf.getuser()})

def eattend(request):
    return render(request, 'employee/eattend.html', {'login' : conf.login, 'user' : conf.getuser()})

def fire(request):
    return render(request, 'employee/fire.html', {'login' : conf.login, 'user' : conf.getuser()})
    

def workh(request):
    return render(request, 'employee/workh.html', {'login' : conf.login, 'user' : conf.getuser()})

def serveEx(request):
    return render(request, 'employee/serveEx.html', {'login' : conf.login, 'user' : conf.getuser()})

def empsalary(request):
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})

def mansalary(request):
    return render(request, 'employee/salary.html', {'login' : conf.login, 'user' : conf.getuser()})
