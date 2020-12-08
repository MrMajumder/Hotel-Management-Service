from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/<int:id>/', views.profile, name='emphome'),
    path('resmanage/<int:id>/', views.resmanage, name='empresmanage'),
    path('servmanage/<int:id>/', views.servmanage, name='empservmanage'),
    path('empmanage/<int:mode>/', views.empmanage, name='empempmanage'),
    path('empsalary/<int:empid>/', views.empsalary, name = 'employeesalary'),
    path('empproedit/<int:empid>/', views.eproedit, name = 'employeerprofileEdit'),
    path('eattend/<int:empid>/', views.eattend, name = 'employeeattendence'),
    path('hoteloverview/<int:id>/', views.hoteloverview, name='emphoteloverview'),
    path('roomdelete<int:id>/', views.roomdelete, name='roomdelete'),
    path('roomform/', views.roomform, name='roomform'),
    path('roomentry/', views.roomentry, name='roomentry'),
    path('expense/', views.expense, name = 'hotelexpenses'),
    path('exentry/', views.exentry, name = 'hotelexpenseentry'),
    path('eattend/', views.eattend, name = 'employeeattendence'),
    path('fire<int:id>/', views.fire, name = 'employeefire'),
    path('workh/<int:id>/', views.workh, name = 'workhistory'),
    path('servEx/', views.serveEx, name = 'serviceExecuted'),
    path('empsalary<int:id>/', views.empsalary, name = 'employeesalary'),
    path('empproedit/', views.eproedit, name = 'employeerprofileEdit'),
    path('empprochange/<int:id>/', views.eprochange, name = 'employeerprofilechange'),
    path('complain<int:id>/', views.comp, name = 'complains'),
    path('comresolve<int:id>/', views.comresolve, name = 'complainsresolve'),
    path('updateroom<int:id>/', views.updateroom, name = 'updateroom'),

]