from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id','nome_fantasia','created','updated','disponibilidade',]
    list_filter = ['disponibilidade', 'created', 'updated']
    list_editable = ['disponibilidade']
    prepopulated_fields = {'slug':('nome_fantasia',)}
    search_fields = ['nome_fantasia']