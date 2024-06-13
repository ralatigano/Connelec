# Generated by Django 5.0.3 on 2024-05-09 21:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_proyectos_n_expediente'),
        ('tareas', '0009_alter_entrada_historial_adjunto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='tareas',
            name='encargado',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tareas',
            name='proyecto',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyectos'),
        ),
    ]