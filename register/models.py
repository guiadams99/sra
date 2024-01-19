from django.db import models
from cliente.models import Cliente
from contratos.models import Acordo, Demanda
from funcionario.models import Funcionario
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, time, timedelta
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_status(value):
    valid_statuses = ['1', '4', '3']
    if value not in valid_statuses:
        raise ValidationError('O status selecionado não é válido.')


class Registro(models.Model):
    # Funcionario
    registrado_por = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        verbose_name="Usuário",
        blank=True,
        null=True,
    )
    cd_funcionario = models.IntegerField(
        verbose_name="ID Funcionario", blank=True, null=True
    )
    # empresas
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, limit_choices_to={'disponibilidade': True})

    cd_cliente = models.IntegerField(verbose_name="ID Cliente", blank=True, null=True)

    def __str__(self):
        return self.nome_fantasia or id
    # Conexão
    tipo_contrato = models.ForeignKey(
        Acordo, on_delete=models.PROTECT, verbose_name="Tipo de Acordo", blank=True, null=True,
        limit_choices_to={'disponibilidade_acordo': True}
    )

    atividade = models.ForeignKey(
        Demanda, on_delete=models.PROTECT, verbose_name="Atividade", blank=True, null=True, 
        limit_choices_to={'disponibilidade_demanda': True}
    )

    # DADOS LEGADOS

    def update_ids(self):
        if self.registrado_por:
            self.cd_funcionario = self.registrado_por.id
        if self.cliente:
            self.cd_cliente = self.cliente.id

    def save(self, *args, **kwargs):
        self.update_ids()
        super().save(*args, **kwargs)



    dt_agenda = models.DateField(verbose_name="Data", blank=True, null=True)
    status = models.CharField(
        default="1",
        max_length=1,
        choices=(
            ("1", "Produtiva"),
            ("2", "Contrato"),
            ("3", "Estudo"),
            ("4", "Bonificada"),
            ("5", "Projeto"),
        ),
        validators=[validate_status],
    )


    descricao = models.TextField(blank=True, null=True, verbose_name="Descricão")
    
    formato = models.CharField(
        default="R",
        null=True,
        blank=True,
        max_length=1,
        choices=(("R", "Remoto"), ("P", "Presencial"),),
    )

    chamado = models.CharField(verbose_name="Nº GLPI", blank=True, null=True, max_length=5, validators=[RegexValidator(r'^\d{1,5}$', message='Insira até 5 dígitos.')])
   
    alimentacao = models.FloatField(verbose_name="Alimentação", blank=True, null=True)
    hospedagem = models.FloatField(verbose_name="Hospedagem", blank=True, null=True)
    pedagio = models.FloatField(verbose_name="Pedágio", blank=True, null=True)
    outros = models.FloatField(verbose_name="Outros", blank=True, null=True)
    obs_km = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Obs KM"
    )
    total_km = models.CharField( verbose_name="Obs KM", blank=True, null=True, max_length=5, validators=[RegexValidator(r'^\d{1,5}$', message='Insira até 5 dígitos.')])
    obs = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Observações"
    )
    dt_faturamento = models.DateTimeField(
        verbose_name="Log de Registro", auto_now=True
    )

    class Meta:
        ordering = ("dt_agenda",)
        index_together = (("id",),)
        verbose_name_plural = "Registros"


    hr_inicio_01 = models.TimeField(verbose_name="Início do Primeiro Horário", blank=True, null=True)
    hr_fim_01 = models.TimeField(verbose_name="Fim do Primeiro Horário", blank=True, null=True)

    hr_inicio_02 = models.TimeField(verbose_name="Início do Segundo Horário", blank=True, null=True)
    hr_fim_02 = models.TimeField(verbose_name="Fim do Segundo Horário", blank=True, null=True)

    hr_inicio_03 = models.TimeField(verbose_name="Início do Terceiro Horário", blank=True, null=True)
    hr_fim_03 = models.TimeField(verbose_name="Fim do Terceiro Horário", blank=True, null=True)

    hr_inicio_04 = models.TimeField(verbose_name="Início do Quarto Horário", blank=True, null=True)
    hr_fim_04 = models.TimeField(verbose_name="Fim do Quarto Horário", blank=True, null=True)

    horas_bruto = models.TimeField("Horas Bruto", blank=True, null=True)
    
    def save(self,*args,**kwargs):
        horario_base = "00:00:00"
        base_subtracao = datetime.strptime(horario_base, "%H:%M:%S")

        somatoria = timedelta(hours=0, minutes=0, seconds=0)

        if self.hr_inicio_01 and self.hr_fim_01:
            time1 = datetime.combine(base_subtracao,self.hr_inicio_01)
            time2 = datetime.combine(base_subtracao,self.hr_fim_01)
            somatoria += time2 - time1
        if self.hr_inicio_02 and self.hr_fim_02:
            time3 = datetime.combine(base_subtracao,self.hr_inicio_02)
            time4 = datetime.combine(base_subtracao,self.hr_fim_02)
            somatoria += time4 - time3
        if self.hr_inicio_03 and self.hr_fim_03:
            time5 = datetime.combine(base_subtracao,self.hr_inicio_03)
            time6 = datetime.combine(base_subtracao,self.hr_fim_03)
            somatoria += time6 - time5
        if self.hr_inicio_04 and self.hr_fim_04:
            time7 = datetime.combine(base_subtracao,self.hr_inicio_04)
            time8 = datetime.combine(base_subtracao,self.hr_fim_04)
            somatoria += time8 - time7

        horas, resto = divmod(somatoria.seconds, 3600)
        minutos, segundos = divmod(resto, 60)

        # Cria um objeto time com as horas, minutos e segundos
        self.horas_bruto = time(horas, minutos, segundos)

        super(Registro, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


@receiver(pre_save, sender=Registro)
def update_registro_ids(sender, instance, **kwargs):
    instance.update_ids()