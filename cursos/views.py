from django.shortcuts import render

# Create your views here.

def inicio(request):

    if request.user.is_authenticated:
        return render(request, 'usuarios/inicio_logado.html')
    else:
        return render(request, 'usuarios/inicio.html')
