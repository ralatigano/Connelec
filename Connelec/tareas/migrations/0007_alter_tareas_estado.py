# Generated by Django 5.0.3 on 2024-04-25 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0006_tareas_proyecto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tareas',
            name='estado',
            field=models.CharField(choices=[('Sin asignar', 'Sin asignar'), ('Asignado/Sin iniciar', 'Asignado/Sin iniciar'), ('En proceso', 'En proceso'), ('Hecho', 'Hecho'), ('En pausa', 'En pausa'), ('Cancelado', 'Cancelado')], default='Sin asignar', max_length=30),
        ),
    ]