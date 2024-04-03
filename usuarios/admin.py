from django.contrib import admin
from .models import *

# Register your models here.

class PaisAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sigla']
    search_fields = ['nome']
admin.site.register(Pais, PaisAdmin)


class EstadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pais', 'nome', 'uf']
    search_fields = ['nome']
    list_filter = ['pais']
admin.site.register(Estado, EstadoAdmin)


class CidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'estado', 'nome']
    search_fields = ['nome']
    list_filter = ['estado']
admin.site.register(Cidade, CidadeAdmin)


class Rede_SocialAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']
admin.site.register(Rede_Social, Rede_SocialAdmin)
