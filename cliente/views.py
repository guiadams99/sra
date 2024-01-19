from django.contrib.auth.decorators import login_required
from cliente.models import Cliente
from contratos.models import Acordo, Demanda
from funcionario.models import Funcionario
from register.models import Registro
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.shortcuts import render
import json
from datetime import datetime, time, timedelta
from django.db.models import Count, F, Value
from django.db.models.functions import Concat


@login_required
def index(request):
    todos_registros = Registro.objects.order_by('-dt_agenda').filter(
        registrado_por = request.user.funcionario
    )

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        todos_registros = todos_registros.filter(
            dt_agenda__range=[start_date, end_date]
        )

    context = {
        "nome_pagina": "SRA",
    }

    if start_date and end_date:
        context["todos_registros"] = todos_registros

    return render(request, 'index.html', context)


@login_required
def dashboard(request):
    registros = Registro.objects.order_by('-id')
    clientes = Cliente.objects.filter(disponibilidade=True)
    acordos = Acordo.objects.filter(disponibilidade_acordo=True)
    demandas = Demanda.objects.filter(disponibilidade_demanda=True)

    # Obter os valores dos filtros
    id = request.GET.get('id')
    cliente_id = request.GET.get('cliente')
    cd_cliente = request.GET.get('cd_cliente')
    cliente_nome_fantasia = request.GET.get('nome_fantasia')
    registrado_por_nome = request.GET.get('registrado_por_nome')
    tipo_contrato = request.GET.get('tipo_contrato')
    atividade = request.GET.get('atividade')
    status = request.GET.get('status')
    chamado = request.GET.get('chamado')
    formato = request.GET.get('formato')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    cliente_selecionado = None
    if cliente_id:
        cliente_selecionado = int(cliente_id)

    tipo_contrato_selecionado = None
    if tipo_contrato:
        tipo_contrato_selecionado = int(tipo_contrato)

    atividade_selecionada = None
    if atividade:
        atividade_selecionada = int(atividade)

    # Criar lista de queries para aplicar filtros múltiplos simultaneamente
    queries = []
    if id:
        queries.append(Q(id=id))
    if cliente_id:
        queries.append(Q(cliente_id=cliente_id) | Q(cd_cliente=cliente_id))
    if cliente_nome_fantasia:
        queries.append(Q(cliente__nome_fantasia__icontains=cliente_nome_fantasia))
    if registrado_por_nome:
        queries.append(Q(registrado_por__nome__icontains=registrado_por_nome))
    if tipo_contrato:
        queries.append(Q(tipo_contrato=tipo_contrato))
    if atividade:
        queries.append(Q(atividade=atividade))
    if status:
        queries.append(Q(status=status))
    if chamado:
        queries.append(Q(chamado=chamado))
    if formato:
        queries.append(Q(formato=formato))
    if start_date and end_date:
        queries.append(Q(dt_agenda__range=[start_date, end_date]))
    
    # Aplicar filtros simultaneamente usando Q
    if queries:
        query = queries.pop()
        for q in queries:
            query &= q
        registros = registros.filter(query)

    # Verificar se algum filtro foi aplicado
    has_filters = bool(request.GET)


    context = {
        "nome_pagina": "Dashboard",
        "registros": registros,
        "clientes": clientes,
        "acordos": acordos,
        "demandas": demandas,
        "has_filters": has_filters,
        "id": id,
        "cliente_nome_fantasia": cliente_nome_fantasia,
        "registrado_por_nome": registrado_por_nome,
        "cd_cliente": cd_cliente,
        "cliente_id": cliente_id,
        "tipo_contrato": tipo_contrato,
        "atividade": atividade,
        "start_date": start_date,
        "end_date" : end_date,
        "chamado" : chamado,
        "formato" : formato,
        "cliente_selecionado": cliente_selecionado, # adiciona a variável cliente_selecionado ao contexto
        "tipo_contrato_selecionado": tipo_contrato_selecionado,
        "atividade_selecionada": atividade_selecionada,
            }

    return render(request, 'dashboard.html', context)


@csrf_exempt
def lista_tipo_contrato_cliente_filtro(request):
    if not request.method == "POST":
        return Http404()
    
    id_cliente = request.POST.get('id_cliente')
    tipo_contrato = Acordo.objects.filter(empresa__id = id_cliente)
    data = {'dados': [{'id_tipo_contrato': i.id, 'tipo_contrato': i.nome_acordo} for i in tipo_contrato]}
    
    return JsonResponse(data)


@csrf_exempt
def lista_atividade_tipo_contrato_filtro(request):
    if not request.method == "POST":
        return Http404()

    id_tipo_contrato = request.POST.get('id_tipo_contrato')
    registro = Acordo.objects.get(id=id_tipo_contrato)
    demandas = registro.tipo_demanda.all()
    data = {'dados': [{'id_atividade': i.id, 'atividade': i.nome_demanda} for i in demandas]}
    return JsonResponse(data)







