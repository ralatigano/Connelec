# Generated by Django 5.0.3 on 2024-05-27 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencias', '0005_user_dark_mode_user_grupo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='grupo',
        ),
        migrations.AddField(
            model_name='user',
            name='telefono',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
