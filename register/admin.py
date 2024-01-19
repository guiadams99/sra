import csv
from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from register.models import Registro


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_per_page = 30
    readonly_fields = ('cd_funcionario','cd_cliente','dt_faturamento',)
    list_display = ['id', 'cd_funcionario', 'cd_cliente',]
    list_display_links = ['id','cd_funcionario', 'cd_cliente',]
    search_fields = ['id']
    list_filter = ['cd_funcionario', 'cd_cliente','tipo_contrato', 'atividade',]
    ordering = '-id',
    actions = ('export_as_csv', 'export_as_xlsx')

    
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response
 
    export_as_csv.short_description = "Exportar CSV"

    
    