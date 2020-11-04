from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from hms import conf

# Create your views here.
def index(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    print(conf.user_id)
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

    sql = ("SELECT * FROM CUSTOMER WHERE USER_ID=%s" % id)
    cursor.execute(sql)
    customer = cursor.fetchall()

    sql = ("SELECT * FROM LOG_IN WHERE LOGIN_ID=%s" % acholder[0][1])
    cursor.execute(sql)
    xx = cursor.fetchall()

    cursor.close()
    dict_result = {} 
    
    dict_result['user_id'] = acholder[0][0]
    dict_result['username'] = xx[0][1]
    dict_result['name'] = acholder[0][2]
    dict_result['house_no'] = acholder[0][3]
    dict_result['road_no'] = acholder[0][4]
    dict_result['city'] = acholder[0][5]
    dict_result['country'] = acholder[0][6]
    dict_result['id_card_no'] = customer[0][1]
    dict_result['passport_no'] = customer[0][2]
    dict_result['credit_card_no'] = customer[0][3]

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
    return render(request, 'customer/index.html', {'login' : conf.login, 'user' : dict_result})

def res(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'customer/reservation.html', {'login' : conf.login, 'user' : conf.getuser()})

def his(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'customer/history.html', {'login' : conf.login, 'user' : conf.getuser()})

def ser(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'customer/service.html', {'login' : conf.login, 'user' : conf.getuser()})

def com(request):
    if(conf.login == False):
        return render(request, 'index.html', {'login' : conf.login, 'user' : conf.getuser()})
    return render(request, 'customer/complaint.html', {'login' : conf.login, 'user' : conf.getuser()})
