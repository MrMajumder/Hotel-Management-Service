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
    path('signsuccess/', views.newinsert1, name='inserted'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loginsuccess/', views.enter_account, name='enter_account'),
    path('deletion/', views.delete, name='delete'),
    path('delete/', views.cdelete, name='confirmdelete'),
    path('edition/<int:uid>/', views.edit, name='edit'),
    path('editform/', views.cedit, name='confirmedit'),
    path('room/<int:id>/', views.roomdetails, name='roomdetails'),
    path('bill/<int:resid>/', views.billshow, name='billshow'),
    path('billpay/<int:resid>', views.billpay, name='billpay'),
    path('updateserver/', views.update_server, name='updateserver'),
]
