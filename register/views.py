from django.contrib import messages
from django.forms import TimeField
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cliente, Registro, Acordo, Demanda, Funcionario
from datetime import datetime, time
from django.shortcuts import render
from .models import Registro
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth.models import Group

def email(registro):
    email_group = Group.objects.get(name='email')

    to_emails = [
        membro.email
        for membro in email_group.user_set.all()
    ]

    # Criar um objeto EmailMessage
    email = EmailMessage(
        subject='Atividade registrada ID {} por {}'.format(registro.id, registro.registrado_por.nome),
        body=render_to_string('email.html', {
            'registro': registro,
        }),
        from_email='seu_endereço_de_email@gmail.com',
        to=to_emails,
    )

    # Enviar o e-mail
    email.send()


@login_required
def cadastro(request):
    if request.method == 'POST':
        # Recuperar os dados do formulário
        registrado_por = request.user.funcionario
        cliente_id = request.POST.get('cliente')
        tipo_contrato_id = request.POST.get('tipo_contrato')
        atividade_id = request.POST.get('atividade')
        dt_agenda_str = request.POST.get('dt_agenda')
        status = request.POST.get('status')
        descricao = request.POST.get('descricao')
        formato = request.POST.get('formato')
        chamado = request.POST.get('chamado')
        if not chamado:
            chamado = None
        alimentacao = request.POST.get('alimentacao')
        if not alimentacao:
            alimentacao = None
        hospedagem = request.POST.get('hospedagem')
        if not hospedagem:
            hospedagem = None
        pedagio = request.POST.get('pedagio')
        if not pedagio:
            pedagio = None
        outros = request.POST.get('outros')
        if not outros:
            outros = None
        obs_km = request.POST.get('obs_km')
        total_km = request.POST.get('total_km')
        if not total_km:
            total_km = None
        obs = request.POST.get('obs')
        # Converter as strings de hora em objetos datetime.time
        hr_inicio_01 = request.POST.get('hr_inicio_01') + ':00' if request.POST.get('hr_inicio_01') else None
        hr_fim_01 = request.POST.get('hr_fim_01') + ':00' if request.POST.get('hr_fim_01') else None
        hr_inicio_02 = request.POST.get('hr_inicio_02') + ':00' if request.POST.get('hr_inicio_02') else None
        hr_fim_02 = request.POST.get('hr_fim_02') + ':00' if request.POST.get('hr_fim_02') else None
        hr_inicio_03 = request.POST.get('hr_inicio_03') + ':00' if request.POST.get('hr_inicio_03') else None
        hr_fim_03 = request.POST.get('hr_fim_03') + ':00' if request.POST.get('hr_fim_03') else None
        hr_inicio_04 = request.POST.get('hr_inicio_04') + ':00' if request.POST.get('hr_inicio_04') else None
        hr_fim_04 = request.POST.get('hr_fim_04') + ':00' if request.POST.get('hr_fim_04') else None


        # Função para converter a string de tempo em objeto datetime.time
        def parse_time(time_str):
            if time_str:
                return time.fromisoformat(time_str)
            return None

        # Verificar se os campos obrigatórios foram preenchidos corretamente
        if not cliente_id or cliente_id == '-------':
            messages.error(request, 'Por favor, selecione um cliente.')
            return redirect('cadastro')

        if not tipo_contrato_id or tipo_contrato_id == '-------':
            messages.error(request, 'Por favor, selecione um tipo de contrato.')
            return redirect('cadastro')

        if not atividade_id or atividade_id == '-------':
            messages.error(request, 'Por favor, selecione uma atividade.')
            return redirect('cadastro')

        if not dt_agenda_str:
            messages.error(request, 'É obrigatório selecionar uma data para a agenda.')
            return redirect('cadastro')

        try:
            dt_agenda = datetime.strptime(dt_agenda_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'A data fornecida é inválida.')
            return redirect('cadastro')

        # Verificar se o campo status contém um valor válido
        if status not in ['1', '3', '4']:
            messages.error(request, 'Por favor, selecione um status válido.')
            return redirect('cadastro')

        # Verificar se o campo formato contém um valor válido
        if formato not in ['R', 'P']:
            messages.error(request, 'Por favor, selecione um formato válido.')
            return redirect('cadastro')
        
        if not hr_inicio_01:
            messages.error(request, 'Por favor, preencha a hora de início 01.')
            return redirect('cadastro')

        if not hr_fim_01:
            messages.error(request, 'Por favor, preencha a hora de término 01.')
            return redirect('cadastro')

        if hr_inicio_02 and not hr_fim_02:
            messages.error(request, 'Por favor, preencha a hora de término 02.')
            return redirect('cadastro')

        if hr_inicio_03 and not hr_fim_03:
            messages.error(request, 'Por favor, preencha a hora de término 03.')
            return redirect('cadastro')

        if hr_inicio_04 and not hr_fim_04:
            messages.error(request, 'Por favor, preencha a hora de término 04.')
            return redirect('cadastro')

        # Criar uma instância do modelo Registro com os dados preenchidos
        registro = Registro(
            registrado_por=registrado_por,
            cliente_id=cliente_id,
            tipo_contrato_id=tipo_contrato_id,
            atividade_id=atividade_id,
            dt_agenda=dt_agenda,
            status=status,
            descricao=descricao,
            formato=formato,
            chamado=chamado,
            alimentacao=alimentacao,
            hospedagem=hospedagem,
            pedagio=pedagio,
            outros=outros,
            obs_km=obs_km,
            total_km=total_km,
            obs=obs,
            hr_inicio_01=parse_time(hr_inicio_01),
            hr_fim_01=parse_time(hr_fim_01),
            hr_inicio_02=parse_time(hr_inicio_02),
            hr_fim_02=parse_time(hr_fim_02),
            hr_inicio_03=parse_time(hr_inicio_03),
            hr_fim_03=parse_time(hr_fim_03),
            hr_inicio_04=parse_time(hr_inicio_04),
            hr_fim_04=parse_time(hr_fim_04),
        )

        # Salvar o registro no banco de dados
        registro.save()

        email(registro)

        messages.success(
            request,
            "Atividade registrada com sucesso"
        )

        return redirect("index")  # Alterar para pagina do funcionario

    # Recuperar os dados necessários para preencher as opções do formulário
    funcionarios = Funcionario.objects.all()
    clientes = Cliente.objects.filter(disponibilidade=True)
    acordos = Acordo.objects.filter(disponibilidade_acordo=True)
    demandas = Demanda.objects.filter(disponibilidade_demanda=True)

    context = {
        'funcionarios': funcionarios,
        'clientes': clientes,
        'acordos': acordos,
        'demandas': demandas,
    }

    # Renderizar o formulário vazio
    return render(request, 'cadastro_os.html', context)



@login_required
def informacoes_atividade(request, id):

    registro = get_object_or_404(
        Registro,
        id=id
    )
    context = {
        "nome_pagina": "Informações de Registro",
        "registro": registro,
    }

    return render(request, "informacoes_atividade.html", context)

@csrf_exempt
def lista_tipo_contrato_cliente(request):
    if not request.method == "POST":
        return Http404()
    
    id_cliente = request.POST.get('id_cliente')
    tipo_contrato = Acordo.objects.filter(empresa__id = id_cliente)
    data = {'dados': [{'id_tipo_contrato': i.id, 'tipo_contrato': i.nome_acordo} for i in tipo_contrato]}
    
    return JsonResponse(data)


@csrf_exempt
def lista_atividade_tipo_contrato(request):
    if not request.method == "POST":
        return Http404()

    id_tipo_contrato = request.POST.get('id_tipo_contrato')
    registro = Acordo.objects.get(id=id_tipo_contrato)
    demandas = registro.tipo_demanda.all()
    data = {'dados': [{'id_atividade': i.id, 'atividade': i.nome_demanda} for i in demandas]}
    return JsonResponse(data)


