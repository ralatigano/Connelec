# Generated by Django 5.0.3 on 2024-05-20 15:25

import asistencias.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencias', '0003_reporte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to=asistencias.models.profile_picture_path),
        ),
    ]