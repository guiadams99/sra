
from django.contrib import admin
from django.urls import path, include
from register.views import *
from cliente.views import *
from contratos.views import *
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index',),
    path('accounts/', include('django.contrib.auth.urls')),
    path('funcionario/', include('funcionario.urls')),
    path('cliente/', include('cliente.urls')),
    path('registro/', include('register.urls')),
    path("registro/<int:id>/", informacoes_atividade, name='informacoes_atividade',),
    path('lista_tipo_contrato_cliente/', lista_tipo_contrato_cliente, name="lista_tipo_contrato_cliente"),
    path('lista_atividade_tipo_contrato/', lista_atividade_tipo_contrato,name="lista_atividade_tipo_contrato"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
