from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from usuarios.templatetags.template_filters import *

from .models import *
from .functions import trataErro
from .forms import *

# Create your views here.

def termos_uso(request):

    return render(request, 'usuarios/termos_uso.html')


def politica_privacidade(request):

    return render(request, 'usuarios/politica_privacidade.html')


def entrar(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["senha"])

            print('user:', user, form.cleaned_data["next"])

            if user is not None:
                login(request, user)
                print('next:', form.cleaned_data["next"])
                if form.cleaned_data["next"] == '':
                    print('next vazio')
                    return redirect(reverse('usuarios:inicio'))
                else:
                    print('next não vazio')
                    return redirect('%s?next=%s' % (reverse('login'), full_path))

        messages.error(request, 'E-Mail e/ou senha inválidos.')
        return render(request, 'usuarios/login.html', { 'form' : form })

    #    full_path = request.get_full_path()

    full_path = request.META.get('HTTP_REFERER')
    print('Caminho:', full_path)

    form = LoginForm()

    print(form)
    return render(request, 'usuarios/login.html', { 'form' : form })



@login_required
def sair(request):
    logout(request)
    return redirect(reverse('usuarios:inicio'))


# @login_required
def inicio(request):

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
        form.fields["pais"].initial = 31
        form.fields["estado"].initial = 19
        form.fields["cidade"].initial = 3639

    return render(request, 'usuarios/cadastrar.html', { 'form': form })


@login_required
def cadastro(request):
    usuario = Usuario.objects.get(user=request.user)
    redes_sociais = Usuario_RedeSocial.objects.filter(user=request.user)

    return render(request, 'usuarios/cadastro.html', { 'usuario' : usuario, 'redes_sociais': redes_sociais })


@login_required
def cadastro_altera(request):

    usuario = Usuario.objects.get(user=request.user)

    if request.method == 'POST':
        print('entrou no post', request.POST)
        form = CadastroAlteraForm(request.POST, instance=usuario)
        if form.is_valid():
            """
            try:
                cidade = Cidade.objects.get(id=request.POST.get('cidade'))
            except Exception as e:
                trataErro(request, e, form)
            """
            try:
                user = User.objects.get(id=request.user.id)

                # Update fields and then save again
                user.first_name = form.cleaned_data["nome"]
                user.save()

                form.save()

                messages.success(request, 'Cadastro alterado.')

                return render(request, 'usuarios/cadastro.html', { 'usuario' : usuario })

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
        form = CadastroAlteraForm(instance=usuario, initial={
            'nome': request.user.first_name,
            'estado': usuario.cidade.estado,
            'cpf': formata_cpf(usuario.cpf),
            'celular': formata_tel(usuario.celular),
            'cep': formata_cep(usuario.cep),
        })


    return render(request, 'usuarios/cadastro_altera.html', { 'form': form })

# ============================

def academico(request):
    usuario = Usuario.objects.get(user=request.user)
    empresas = Usuario_Empresa.objects.filter(user=request.user)
    
    return render(request, 'usuarios/academico.html', { 'user': request.user, 'usuario' : usuario, 'empresas': empresas })


def profissional(request):
    usuario = Usuario.objects.get(user=request.user)
    empresas = Usuario_Empresa.objects.filter(user=request.user)
    
    return render(request, 'usuarios/empresas.html', { 'user': request.user, 'usuario' : usuario, 'empresas': empresas })


def informes(request):
    usuario = Usuario.objects.get(user=request.user)
    empresas = Usuario_Empresa.objects.filter(user=request.user)
    
    return render(request, 'usuarios/informes.html', { 'user': request.user, 'usuario' : usuario, 'empresas': empresas })


def rede_social_atualiza(request):
    usuario = Usuario.objects.get(user=request.user)
    redes_sociais = Usuario_RedeSocial.objects.filter(user=request.user)
    
    form = RedeSocialForm()

    return render(request, 'usuarios/rede_social_atualiza.html', { 'form': form, 'user': request.user, 'usuario' : usuario, 'redes_socials': redes_sociais })


"""
def carrega_pais(request):
    arquivo = open('/home/loyola/Downloads/paises.txt')
    for linha in arquivo:
        print(linha)
        linha_aux = linha.split(' - ')
        pais = Pais(
            nome  = linha_aux[0],
            sigla = linha_aux[1],
        )

        pais.save()
"""

def load_cidades(request):

    if not request.GET.get('id'):
        return render(request, 'usuarios/ret_cidades.html', {})

    estado_id = request.GET.get('id')
    cidades = Cidade.objects.filter(estado = estado_id).order_by('nome')

    return render(request, 'usuarios/ret_cidades.html', {'cidades' : cidades})
