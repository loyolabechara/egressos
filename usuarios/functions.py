from django.contrib import messages
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

import re

error_messages = {
    'invalid': _("Número de CPF inválido."),
    'digits_only': _("Este campo requer somente números."),
    'max_digits': _("Este campo requer 11 dígitos."),
}


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


def validate_CPF(value):
    """
    Value can be either a string in the format XXX.XXX.XXX-XX or an
    11-digit number.
    """

    if value in EMPTY_VALUES:
        return u''
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(error_messages['digits_only'])
    if len(value) != 11:
        raise ValidationError(error_messages['max_digits'])
    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise ValidationError(error_messages['invalid'])

    return orig_value


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
