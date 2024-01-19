from django.urls import path, include
from cliente.views import *
from django.shortcuts import redirect
from django.urls import path
from .views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name ='dashboard'),
]

