from django.db import models
from .functions_cpf_cnpj import validate_CPF
from django.contrib.auth.models import User
from cursos.models import Curso, Linha_Pesquisa

# Create your models here.

SEXO = (
    ('F', 'Feminino'),
    ('M', 'Masculino'),
    ('O', 'Outro'),
    ('N', 'Prefiro não dizer'),
)

class Pais(models.Model):

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Países"
        verbose_name = "País"

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=60)
    sigla = models.CharField(unique=True, max_length=2)

class Estado(models.Model):

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    nome = models.CharField(unique=True, max_length=60)
    uf = models.CharField(unique=True, max_length=2)


class Cidade(models.Model):

    class Meta:
        ordering = ['nome']
        unique_together = ('estado', 'nome')

    def __str__(self):
        return '%s - %s' % (self.estado, self.nome)

    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)


class Empresa(models.Model):

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=120)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, blank=True, null=True)
    cidade_exterior = models.CharField(max_length=120, blank=True, null=True)
    estado_exterior = models.CharField(max_length=120, blank=True, null=True)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Rede_Social(models.Model):

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Redes Sociais"

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=120)


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
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, blank=True, null=True)
    cidade_exterior = models.CharField(max_length=120, blank=True, null=True)
    estado_exterior = models.CharField(max_length=120, blank=True, null=True)
    cep = models.CharField(max_length=8, blank=True, null=True)
    autorizoExporContato = models.BooleanField(verbose_name="Autorizo expor meus dados de contato para integrantes desta plataforma")
    autorizoExporCurriculo = models.BooleanField(verbose_name="Autorizo expor meus dados sobre formação acadêmica e profissional para integrantes desta plataforma")
    ativo = models.BooleanField(default=True)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Usuario_Curso(models.Model):

    class Meta:
        ordering = ['curso', 'user']

    def __str__(self):
        return '%s - %s' % (self.curso, self.user)

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    linhaPesquisa = models.ForeignKey(Linha_Pesquisa, on_delete=models.PROTECT)
    dtinicio = models.DateField('Data início')
    dtConclusao = models.DateField('Data Conclusão')
    tituloDisertacao = models.CharField(max_length=200, verbose_name='Título da Dissertação')
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Cargo(models.Model):

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

    nome = models.CharField(unique=True, max_length=120)


class Usuario_Empresa(models.Model):

    class Meta:
        verbose_name_plural = "Usuários/Empresas"
        verbose_name = "Usuário/Empresa"
        ordering = ['user']

    def __str__(self):
        return '%s - %s' % (self.user, self.empresa)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    cargo_outro = models.CharField(max_length=120, blank=True, null=True)
    dtInicio = models.DateField('Data Contratação')
    dtFim = models.DateField('Data Desligamento', blank=True, null=True)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')



class Usuario_RedeSocial(models.Model):

    class Meta:
        verbose_name_plural = "Usuários/Redes Sociais"
        verbose_name = "Usuário/Rede Social"
        ordering = ['user', 'rede_social']

    def __str__(self):
        return '%s - %s' % (self.user, self.rede_social)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rede_social = models.ForeignKey(Rede_Social, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=120, verbose_name="Endereço")
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')

class Tipo_Informe(models.Model):

    class Meta:
        ordering = ['descricao']
        verbose_name_plural = "Tipos de Informes"
        verbose_name = "Tipo de Informe"


    def __str__(self):
        return '%s' % (self.descricao)

    descricao = models.CharField(unique=True, max_length=120)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Informe(models.Model):

    class Meta:
        ordering = ['id']


    def __str__(self):
        return '%s - %s - %s' % (self.user, self.tipoInforme, self.texto)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipoInforme = models.ForeignKey(Tipo_Informe, on_delete=models.PROTECT)
    texto = models.CharField(max_length=3000)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')
