from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
#    path('cadastro', views.cadastro, name='cadastro'),
#    path('cadastro_altera', views.cadastro_altera, name='cadastro_altera'),
    #
    path('termos_uso', views.termos_uso, name='termos_uso'),
    path('politica_privacidade', views.politica_privacidade, name='politica_privacidade'),
    path('fale_conosco', views.fale_conosco, name='fale_conosco'),
    #
    path('ajax/load_cidades/', views.load_cidades, name = 'ajax_load_cidades'),
]