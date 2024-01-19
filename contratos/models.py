from django.db import models

from cliente.models import Cliente
from django.utils.text import slugify




class Demanda(models.Model):
    nome_demanda = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    disponibilidade_demanda = models.BooleanField(default=True)
    
    @staticmethod
    def clientes_ativas():
        return Demanda.objects.filter(disponibilidade_demanda=True, blank=True, null=True) 

    def __str__(self):
        return self.nome_demanda


class Acordo(models.Model):
    nome_acordo = models.CharField(max_length=100)
    descrição_acordo = models.TextField(blank=True)
    empresa = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    categoria = models.CharField(
        default= "C",
        max_length=1,
        choices= (
            ('C', 'Contrato'),
            ('B', 'Banco de Horas'),
            ('P', 'Projeto'),
            ('E', 'Especial'),
            
        )
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    disponibilidade_acordo = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    tipo_demanda = models.ManyToManyField(Demanda)

    def save(self, *args, **kwargs):
        # Concatena o nome do acordo com o nome da empresa
        slug_str = "{} {}".format(self.nome_acordo, self.empresa)
        # Gera o slug usando a função slugify()
        self.slug = slugify(slug_str)
        super(Acordo, self).save(*args, **kwargs)

    class Meta:
        ordering = ('nome_acordo',)
        index_together = (('id', 'slug'),)
        verbose_name_plural= 'acordos'

    @staticmethod
    def clientes_ativas():
        return Acordo.objects.filter(disponibilidade_acordo=True, blank=True, null=True)     

    def __str__(self):
        return self.nome_acordo



