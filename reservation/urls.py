from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.solores, name='resHome'),
    path('cr_reserve/', views.cr_reserve, name='createreservation'),
    path('creserv<int:id>/', views.canreserv, name='cancelreservation')
]
