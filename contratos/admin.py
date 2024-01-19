from django.contrib import admin
from contratos.models import Acordo, Demanda

@admin.register(Acordo)
class AcordoAdmin(admin.ModelAdmin):
    list_display = ['id','empresa','nome_acordo',]
    list_display_links = 'id', 'empresa', 'nome_acordo'
    search_fields = ['nome_acordo']
    list_filter = ['empresa','nome_acordo', ]
    list_per_page = 10
    readonly_fields = ['slug']
    filter_horizontal = ('tipo_demanda',)  # add this line to display checkboxes for the ManyToManyField


@admin.register(Demanda)
class DemandaAdmin(admin.ModelAdmin):
    list_display = ['nome_demanda', 'created', 'updated', 'disponibilidade_demanda']
    list_per_page = 10
    list_filter = ['nome_demanda']
