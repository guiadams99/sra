from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from authenticacao.models import Users


class Funcionario(models.Model):
    usuario = models.OneToOneField("authenticacao.Users", on_delete=models.PROTECT,verbose_name="Usuário",blank=True, null=True)
    nome = models.CharField(max_length=40, blank=True, null=True) #
    email = models.CharField(max_length=45, blank=True, null=True) #
    endereco = models.CharField(max_length=40, blank=True, null=True)
    cidade = models.CharField(max_length=20, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    complemento = models.CharField(max_length=40, blank=True, null=True)
    rg = models.CharField(max_length=9, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    data_nascimento = models.DateTimeField()
    data_admissao = models.DateTimeField()
    fone_res = models.CharField(max_length=13, blank=True, null=True)
    fone_cel = models.CharField(max_length=13, blank=True, null=True)
    carro = models.CharField(max_length=25, blank=True, null=True)
    placa_carro = models.CharField(max_length=8, blank=True, null=True)
    ativo = models.CharField(max_length=1, blank=True, null=True)


    created_user = models.DateTimeField(auto_now_add=True, blank=True, null=True) #
    updated_user = models.DateTimeField(auto_now=True, blank=True, null=True) #
    disponibilidade_user = models.BooleanField(default=True, blank=True, null=True) #


    @staticmethod
    def empresas_ativas():
        return Funcionario.objects.filter(disponibilidade=True, blank=True, null=True) #

    class Meta:
        verbose_name = "Funcionario"
        index_together = (('id'),)
        db_table = "funcionario"
        
    def __str__(self):
        return self.nome or id


