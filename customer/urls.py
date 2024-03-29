from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.index, name='cusHome'),
    path('reservations/', views.res, name='cusRes'),
    path('history/<int:id>/', views.his, name='cusHis'),
    path('services/', views.ser, name='cusSer'),
    path('complain/', views.com, name='cusCom'),
    path('filecomp/', views.fcom, name='cusFileCom'),
]
