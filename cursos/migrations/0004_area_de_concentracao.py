# Generated by Django 5.0.4 on 2024-04-30 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_alter_curso_options_alter_linha_pesquisa_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area_De_Concentracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=120, unique=True)),
                ('dtInclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('linhaDePesquisa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cursos.linha_pesquisa')),
            ],
            options={
                'verbose_name': 'Área de Concentração',
                'verbose_name_plural': 'Áreas de Concentração',
                'ordering': ['linhaDePesquisa__descricao', 'descricao'],
            },
        ),
    ]
