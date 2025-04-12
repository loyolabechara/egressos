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

            if user is not None:
                login(request, user)
                if form.cleaned_data["next"] == '':
                    return redirect(reverse('usuarios:inicio'))
                else:
                    return redirect('%s?next=%s' % (reverse('login'), full_path))

        messages.error(request, 'E-Mail e/ou senha inválidos.')
        return render(request, 'usuarios/login.html', { 'form' : form })

    #    full_path = request.get_full_path()

    full_path = request.META.get('HTTP_REFERER')

    form = LoginForm()

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
        print(request.POST['rua'])
        print(request.POST['estado'])
        print(request.POST['cidade'])
        form = CadastrarForm(request.POST)
        print("form------->", form)
        if form.is_valid():
            try:
                cidade = Cidade.objects.get(id=request.POST.get('cidade'))
            except Exception as e:
                print('Erro:', e)
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

                messages.success(request, 'Usuário cadastrado.')

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
        form.fields["pais"].initial = 1
#        form.fields["estado"].initial = 19
#        form.fields["cidade"].initial = 3639

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


def rede_social_atualiza(request):
#    usuario = Usuario.objects.get(user=request.user)
    redes_sociais = Usuario_RedeSocial.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UsuarioRedeSocialForm(request.POST)
        if form.is_valid():
            form_aux = form.save(commit=False)
            form_aux.user = request.user
            form_aux.save()
        else:
            print('erro')

    form = UsuarioRedeSocialForm()

    return render(request, 'usuarios/rede_social_atualiza.html', { 'form': form, 'user': request.user, 'redes_socials': redes_sociais })

# ============================

def profissional(request):
    usuario = Usuario.objects.get(user=request.user)
    empresas = Usuario_Empresa.objects.filter(user=request.user)
    
    return render(request, 'usuarios/empresas.html', { 'user': request.user, 'usuario' : usuario, 'empresas': empresas })


def profissional_inclui(request):

    if request.method == 'POST':
        form_empresa = EmpresaForm(request.POST)
        form_usuario_empresa = Usuario_EmpresaForm(request.POST)

        if form_empresa.is_valid() and form_usuario_empresa.is_valid():
            form_empresa_aux = form_empresa.save()
            form_usuario_empresa_aux = form_usuario_empresa.save(commit=False)
            form_usuario_empresa_aux.empresa = form_empresa_aux
            form_usuario_empresa_aux.user = request.user
            form_usuario_empresa_aux.save()

            return redirect(reverse('usuarios:profissional'))


    form_empresa = EmpresaForm()
    form_usuario_empresa = Usuario_EmpresaForm()
    
    return render(request, 'usuarios/profissional_inclui.html', { 'form_empresa': form_empresa, 'form_usuario_empresa': form_usuario_empresa })


def academico(request):
    usuario = Usuario.objects.get(user=request.user)
    empresas = Usuario_Empresa.objects.filter(user=request.user)
    graduacoes = Usuario_Graduacao.objects.filter(user=request.user)
    pos = Usuario_Pos.objects.filter(user=request.user)
    
    return render(request, 'usuarios/academico.html', { 'user': request.user, 'usuario' : usuario, 'graduacoes': graduacoes, 'pos': pos, 'empresas': empresas })


def academico_inclui(request):
    cursos = Curso.objects.all()

    return render(request, 'usuarios/academico_inclui.html', { 'cursos': cursos })


def academico_inclui_graduacao(request, id):

    curso = Curso.objects.get(id=id)

    if request.method == 'POST':
        form = GraduacaoForm(request.POST)

        if form.is_valid():
            form_aux = form.save(commit=False)
            form_aux.user = request.user
            form_aux.curso = curso
            form_aux.save()

            return redirect(reverse('usuarios:academico'))

    form = GraduacaoForm()
    
    return render(request, 'usuarios/academico_inclui_graduacao.html', { 'form': form, 'curso': curso })


def academico_inclui_pos(request, id):

    curso = Curso.objects.get(id=id)

    if request.method == 'POST':
        form = PosForm(request.POST)

        if form.is_valid():
            form_aux = form.save(commit=False)
            form_aux.user = request.user
            form_aux.curso = curso
            form_aux.save()

            return redirect(reverse('usuarios:academico'))

    form = PosForm()
    
    return render(request, 'usuarios/academico_inclui_pos.html', { 'form': form, 'curso': curso })


def informes(request):
    informes = Informe.objects.all().order_by('-id')
    
    return render(request, 'usuarios/informes.html', { 'informes': informes })


def informes_inclui(request):

    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            form_aux = form.save(commit=False)
            form_aux.user = request.user
            form_aux.save()
        else:
            print('erro')

    form = InformeForm()

    return render(request, 'usuarios/informes_inclui.html', { 'form': form, 'user': request.user })


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

def load_cidades(request, estado_id):
    from django.http import JsonResponse
    """
    if not request.GET.get('id'):
        return render(request, 'usuarios/ret_cidades.html', {})

    estado_id = request.GET.get('id')
    cidades = Cidade.objects.filter(estado = estado_id).order_by('nome')

    return render(request, 'usuarios/ret_cidades.html', {'cidades' : cidades})
    """
    cidades = Cidade.objects.filter(estado_id=estado_id).values('id', 'nome')
    return JsonResponse({'cidades': list(cidades)})



@login_required
def mostra_usuario(request, id):
    user = User.objects.get(id=id)
    usuario = Usuario.objects.get(user=user)
    redes_sociais = Usuario_RedeSocial.objects.filter(user=request.user)
    graduacoes = Usuario_Graduacao.objects.filter(user=request.user)
    pos = Usuario_Pos.objects.filter(user=request.user)
    empresas = Usuario_Empresa.objects.filter(user=request.user)

    return render(request, 'usuarios/mostra_usuario.html', { 'usuario' : usuario, 'redes_sociais': redes_sociais, 'graduacoes': graduacoes, 'pos': pos, 'empresas': empresas })
