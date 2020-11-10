from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('customer/', include('customer.urls')),
    path('employee/', include('employee.urls')),
    path('reservation/', include('reservation.urls')),
    path('service/', include('service.urls')),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/',views.signup, name='signup'),
    path('signsuccess/', views.insert, name='inserted'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loginsuccess/', views.enter_account, name='enter_account')
]
