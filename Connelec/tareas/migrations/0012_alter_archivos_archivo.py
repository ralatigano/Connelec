# Generated by Django 5.0.3 on 2024-05-10 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0011_alter_tareas_fecha_entrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivos',
            name='archivo',
            field=models.FileField(blank=True, default=None, null=True, upload_to='archivos/'),
        ),
    ]
