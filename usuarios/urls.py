from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('entrar', views.entrar, name='entrar'),
    path('sair', views.sair, name='sair'),
    #
    path('', views.inicio, name='inicio'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('mostra_usuario/<int:id>', views.mostra_usuario, name='mostra_usuario'),

    path('cadastro_altera', views.cadastro_altera, name='cadastro_altera'),
    path('rede_social_atualiza', views.rede_social_atualiza, name='rede_social_atualiza'),
    #
    path('academico', views.academico, name='academico'),
    path('academico_inclui', views.academico_inclui, name='academico_inclui'),
    path('academico_inclui_graduacao/<int:id>', views.academico_inclui_graduacao, name='academico_inclui_graduacao'),
    path('academico_inclui_pos/<int:id>', views.academico_inclui_pos, name='academico_inclui_pos'),
    #
    path('profissional', views.profissional, name='profissional'),
    path('profissional_inclui', views.profissional_inclui, name='profissional_inclui'),
    #
    path('informes', views.informes, name='informes'),
    path('informes_inclui', views.informes_inclui, name='informes_inclui'),
    #
    path('termos_uso', views.termos_uso, name='termos_uso'),
    path('politica_privacidade', views.politica_privacidade, name='politica_privacidade'),
#    path('fale_conosco', views.fale_conosco, name='fale_conosco'),
    #
    path('ajax/load_cidades/', views.load_cidades, name = 'ajax_load_cidades'),
    #
#    path('carrega_pais', views.carrega_pais, name='carrega_pais'),
]