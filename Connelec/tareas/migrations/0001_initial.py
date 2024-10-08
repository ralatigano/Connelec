# Generated by Django 5.0.3 on 2024-05-29 21:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyectos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrada_historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, default=None, null=True)),
                ('resumen', models.TextField(max_length=1000)),
                ('adjunto', models.FileField(blank=True, null=True, upload_to='archivos/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyectos')),
                ('usuario', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tareas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descrip', models.TextField(max_length=500)),
                ('estado', models.CharField(choices=[('Sin asignar', 'Sin asignar'), ('Asignado/Sin iniciar', 'Asignado/Sin iniciar'), ('En proceso', 'En proceso'), ('Hecho', 'Hecho'), ('En pausa', 'En pausa'), ('Cancelado', 'Cancelado')], default='Sin asignar', max_length=30)),
                ('fecha_entrega', models.DateField(blank=True, default=None, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('encargado', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyectos')),
            ],
        ),
        migrations.CreateModel(
            name='Archivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('archivo', models.FileField(blank=True, default=None, null=True, upload_to='archivos/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualización', models.DateTimeField(auto_now=True)),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tareas.tareas')),
            ],
        ),
    ]
