from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .models import *
from .functions import trataErro

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

def cadastrar(request):
    if request.method == 'POST':
        form = CadastrarForm(request.POST)
        if form.is_valid():
            print('captcha:', request.POST.get('captcha'))
            try:
                cidade = Cidade.objects.get(id=request.POST.get('cidade'))
            except Exception as e:
                trataErro(request, e, form)

            try:
                user = User.objects.create_user(request.POST.get('email'), request.POST.get('email'), request.POST.get('senha'))

                # Update fields and then save again
                user.first_name = request.POST.get('nome')
                user.last_name = request.POST.get('nome')
                user.save()

                usuario = form.save(commit=False)
                usuario.user = user
                usuario.cidade = cidade
                usuario.save()
                form.save_m2m()

                messages.success(request, 'Conta criada.')

                return redirect(reverse("usuarios:inicio"))

            except Exception as e:
                erro = str(e).split(', ')

                if erro[0] == '(1062':
                    messages.error(request, 'Erro: Usuário já existe.')
                else:
                    # Se teve erro:
                    print('Erro: ', form.errors)
                    erro_tmp = str(form.errors)
                    erro_tmp = erro_tmp.replace('<ul class="errorlist">', '')
                    erro_tmp = erro_tmp.replace('</li>', '')
                    erro_tmp = erro_tmp.replace('<ul>', '')
                    erro_tmp = erro_tmp.replace('</ul>', '')
                    erro_tmp = erro_tmp.split('<li>')

                    print('erro:', erro_tmp)

                    messages.error(request, erro_tmp[1] + ': ' + erro_tmp[2])
        else:
            messages.error(request, 'Corrigir o erro apresentado.')
    else:
        form = CadastrarForm()
        form.fields["estado"].initial = 19
        form.fields["cidade"].initial = 3639

    return render(request, 'usuarios/cadastrar.html', { 'form': form })
