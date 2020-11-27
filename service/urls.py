from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.soloser, name='servAppHome'),
     path('cr_service/', views.cr_service, name='createservice'),
     path('ca_serve<int:id>/', views.ca_serve, name='cancelservice')
]
