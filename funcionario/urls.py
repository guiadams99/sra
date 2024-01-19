from django.urls import path
from . import views
from .views import CustomPasswordChangeView

urlpatterns = [
    # outras URLs aqui
    path('change_password/', views.change_password, name='change_password'),
]
