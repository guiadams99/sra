from django.urls import path
from register.views import *

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro',),
]
