from django.db import models

# Create your models here.

class Tipo_Formacao(models.Model):

    class Meta:
        ordering = ['descricao']
        verbose_name_plural = "Tipos de Formação"
        verbose_name = "Tipo de Formação"

    def __str__(self):
        return '%s' % (self.descricao)

    descricao = models.CharField(unique=True, max_length=60, verbose_name='Descrição')
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Curso(models.Model):

    class Meta:
        ordering = ['tipoFormacao', 'nome']

    def __str__(self):
        return '%s - %s' % (self.tipoFormacao, self.nome)

    tipoFormacao = models.ForeignKey(Tipo_Formacao, on_delete=models.PROTECT)
    nome = models.CharField(unique=True, max_length=60)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')


class Linha_Pesquisa(models.Model):

    class Meta:
        ordering = ['curso__nome', 'descricao']
        verbose_name_plural = "Linhas de Pesquisas"
        verbose_name = "Linha de Pesquisa"


    def __str__(self):
        return '%s - %s' % (self.curso, self.descricao)

    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    descricao = models.CharField(unique=True, max_length=120)
    dtInclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')
