# Generated by Django 5.0.4 on 2024-04-30 04:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0004_area_de_concentracao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20, unique=True, verbose_name='Descrição')),
                ('dtInclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
            ],
            options={
                'verbose_name': 'Nível',
                'verbose_name_plural': 'Níveis',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='NivelCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dtInclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cursos.curso')),
                ('nivel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cursos.nivel', verbose_name='Nível')),
            ],
            options={
                'ordering': ['curso', 'nivel'],
            },
        ),
    ]
