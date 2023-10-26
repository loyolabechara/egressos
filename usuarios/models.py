from django.db import models
from .functions_cpf_cnpj import validate_CPF
from django.contrib.auth.models import User

# Create your models here.

SEXO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
    ('O', 'Outro'),
    ('N', 'Prefiro não dizer'),
)

class Estado(models.Model):

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=60)
    uf = models.CharField(unique=True, max_length=2)


class Cidade(models.Model):

    class Meta:
        ordering = ['nome']
        unique_together = ('estado', 'nome')

    def __str__(self):
        return '%s' % (self.nome)

    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)


class Empresa(models.Model):

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=60)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Usuario(models.Model):

    class Meta:
        verbose_name_plural = "Usuários"
        verbose_name = "Usuário"
        ordering = ['user']

    def __str__(self):
        return '%s' % (self.user)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(unique=True, max_length=11, validators=[validate_CPF])
    sexo = models.CharField(max_length=1, choices=SEXO)
    dtNascimento = models.DateField('Data Nascimento')
    celular = models.CharField(max_length=11)
    rua = models.CharField(max_length=120)
    numero = models.CharField(max_length=50, verbose_name='Número')
    complemento = models.CharField(max_length=120, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    cep = models.CharField(max_length=8)
    empresas = models.ManyToManyField(Empresa)
    ativo = models.BooleanField(default=True)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')
