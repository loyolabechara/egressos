from django.contrib import admin
from .models import *

# Register your models here.

class Tipo_FormacaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'dtInclusao']
    search_fields = ['descricao']
admin.site.register(Tipo_Formacao, Tipo_FormacaoAdmin)


class CursoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipoFormacao', 'nome', 'dtInclusao']
    search_fields = ['nome']
    list_filter = ['tipoFormacao']
admin.site.register(Curso, CursoAdmin)


class NivelAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'dtInclusao']
    search_fields = ['descricao']
admin.site.register(Nivel, NivelAdmin)


class NivelCursoAdmin(admin.ModelAdmin):
    list_display = ['id', 'curso', 'nivel', 'dtInclusao']
    search_fields = ['curso__nome']
    list_filter = ['nivel']
admin.site.register(NivelCurso, NivelCursoAdmin)


class Linha_PesquisaAdmin(admin.ModelAdmin):
    list_display = ['id', 'curso', 'descricao', 'dtInclusao']
    search_fields = ['descricao']
    list_filter = ['curso']
admin.site.register(Linha_Pesquisa, Linha_PesquisaAdmin)


class Area_De_ConcentracaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'linhaDePesquisa', 'descricao', 'dtInclusao']
    search_fields = ['descricao']
    list_filter = ['linhaDePesquisa']
admin.site.register(Area_De_Concentracao, Area_De_ConcentracaoAdmin)
