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


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cpf', 'dtInclusao']
    search_fields = ['user__first_name']
#    list_filter = ['rede_social']
admin.site.register(Usuario, UsuarioAdmin)


class Usuario_RedeSocialAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'rede_social', 'endereco']
    search_fields = ['user__first_name']
    list_filter = ['rede_social']
admin.site.register(Usuario_RedeSocial, Usuario_RedeSocialAdmin)


class Usuario_GraduacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'curso', 'dtInicio', 'dtFim', 'dtInclusao']
    search_fields = ['user__first_name']
    list_filter = ['curso']
admin.site.register(Usuario_Graduacao, Usuario_GraduacaoAdmin)


class Tipo_InformeAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'dtInclusao']
    search_fields = ['descricao']
admin.site.register(Tipo_Informe, Tipo_InformeAdmin)


class InformeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tipoInforme', 'texto', 'dtInclusao']
    search_fields = ['user__first_name', 'texto']
    list_filter = ['tipoInforme']
admin.site.register(Informe, InformeAdmin)


class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']
admin.site.register(Cargo, CargoAdmin)


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'pais', 'cidade', 'dtInclusao']
    search_fields = ['user__first_name']
admin.site.register(Empresa, EmpresaAdmin)


class Usuario_EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'empresa', 'cargo', 'dtInicio', 'dtFim', 'dtInclusao']
    search_fields = ['user__first_name']
admin.site.register(Usuario_Empresa, Usuario_EmpresaAdmin)
