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
    
    
    path('hoteloverview/', views.hoteloverview, name='emphoteloverview'),
    path('expense/', views.expense, name = 'hotelexpenses'),
    path('exentry/', views.exentry, name = 'hotelexpenseentry'),
    path('eattend/', views.eattend, name = 'employeeattendence'),
    path('fire/', views.fire, name = 'employeefire'),
    path('workh/', views.workh, name = 'workhistory'),
    path('servEx/', views.serveEx, name = 'serviceExecuted'),
    path('empsalary/', views.empsalary, name = 'employeesalary'),
    path('empsalaryentry/', views.empsalaryentry, name = 'employeesalaryentry'),
    path('empproedit/', views.eproedit, name = 'employeerprofileEdit'),
    path('empprochange/', views.eprochange, name = 'employeerprofilechange'),
]