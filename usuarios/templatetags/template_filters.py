from django import template
register = template.Library()

@register.filter(name='formata_tel')
def formata_tel(numero):
    if numero == '':
        return ''

    if len(numero) == 10:
        first = numero[0:2]
        second = numero[2:6]
        third = numero[6:10]
        return '(' + first + ')' + ' ' + second + '-' + third
    else:
        first = numero[0:2]
        second = numero[2:7]
        third = numero[7:11]
        return '(' + first + ')' + ' ' + second + '-' + third

@register.filter(name='formata_cep')
def formata_cep(numero):
    if numero == '':
        return ''

    first = numero[0:2]
    second = numero[2:5]
    third = numero[5:9]
    return first + '.' + second + '-' + third

@register.filter(name='formata_cpf')
def formata_cpf(numero):
    if numero == '':
        return ''

    first = numero[0:3]
    second = numero[3:6]
    third = numero[6:9]
    fourth = numero[9:11]
    return first + '.' + second + '.' + third + '-' + fourth


@register.filter(name='formata_sexo')
def formata_sexo(sexo):
    if sexo == 'F':
        return 'Feminino'
    elif sexo == 'M':
        return 'Masculino'
    else:
        return 'Não Informado'



@register.filter(name='turno')
def turno(turno):
    if turno == 'A':
        return 'Almoço'
    else:
        return 'Jantar'
