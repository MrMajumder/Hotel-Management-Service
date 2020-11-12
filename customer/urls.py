from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.index, name='cusHome'),
    path('reservations/', views.res, name='cusRes'),
    path('reservations/<int:id>/', views.solores, name='cusSoloRes'),
    path('history/', views.his, name='cusHis'),
    path('services/', views.ser, name='cusSer'),
    path('services/<int:id>/', views.soloser, name='cusSoloSer'),
]
