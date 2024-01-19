from django.db import models

class Cliente(models.Model):
    nome_fantasia = models.CharField(max_length=50, blank=True, null=True) #
    razao_social = models.CharField(max_length=50, blank=True, null=True)
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    endereço = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=20, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    complemento = models.CharField(max_length=40, blank=True, null=True)
    inscr_estadual = models.CharField(max_length=14, blank=True, null=True)
    fone = models.CharField(max_length=13, blank=True, null=True)
    contato_financeiro = models.CharField(max_length=25, blank=True, null=True)
    contato_diretoria = models.CharField(max_length=25, blank=True, null=True)
    contato_informatica_gerencial = models.CharField(max_length=25, blank=True, null=True)
    contato_informatica_tecnico = models.CharField(max_length=25, blank=True, null=True)
    tipo = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)


    slug = models.SlugField(max_length=200, blank=True, null=True) #
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True) #
    updated = models.DateTimeField(auto_now=True, blank=True, null=True) # 
    disponibilidade = models.BooleanField(default=True, blank=True, null=True) #

    class Meta:
        ordering = ('nome_fantasia',)
        index_together = (('id', 'slug'),)
        verbose_name_plural= 'clientes'

    def __str__(self):
        return self.nome_fantasia or id

    @staticmethod
    def clientes_ativas():
        return Cliente.objects.filter(disponibilidade=True, blank=True, null=True) #
