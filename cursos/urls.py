from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.inicio, name='inicio'),
#    path('cadastrar', views.cadastrar, name='cadastrar'),
]