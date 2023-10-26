from django.contrib import messages


def trataErro(request, e, form):
    erro = str(e).split(', ')

    print('erro:', erro)

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
