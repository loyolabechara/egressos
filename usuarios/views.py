from django.shortcuts import render

# Create your views here.

def termos_uso(request):

    return render(request, 'usuarios/termos_uso.html')


def politica_privacidade(request):

    return render(request, 'usuarios/politica_privacidade.html')


def inicio(request):

    if request.user.is_authenticated:
        return render(request, 'usuarios/inicio_logado.html')
    else:
        return render(request, 'usuarios/inicio.html')
