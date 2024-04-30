# Generated by Django 5.0.4 on 2024-04-30 05:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0005_nivel_nivelcurso'),
        ('usuarios', '0008_informe_dtexpiracao'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario_Graduacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dtInicio', models.DateField(verbose_name='Data Início')),
                ('dtFim', models.DateField(verbose_name='Data Conclusão')),
                ('dtInclusao', models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuário/Graduacao',
                'verbose_name_plural': 'Usuários/Graduacao',
                'ordering': ['user', 'dtInicio'],
            },
        ),
    ]