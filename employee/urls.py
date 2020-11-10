from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.profile, name='emphome'),
    path('resmanage/', views.resmanage, name='empresmanage'),
    path('servmanage/', views.servmanage, name='empservmanage'),
    path('empreg/', views.empreg, name='empempreg'),
    path('empmanage/', views.empmanage, name='empempmanage'),
    path('hoteloverview/', views.hoteloverview, name='emphoteloverview'),
    path('expense/', views.expense, name = 'hotelexpenses'),
    path('eattend/', views.eattend, name = 'employeeattendence'),
    path('fire/', views.fire, name = 'employeefire'),
    path('workh/', views.workh, name = 'workhistory'),
    path('servEx/', views.serveEx, name = 'serviceExecuted')
]