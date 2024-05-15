# Generated by Django 5.0.3 on 2024-03-21 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField()),
                ('hora', models.TimeField()),
                ('tipo', models.IntegerField(choices=[(0, 'Entrada'), (1, 'Salida')])),
            ],
        ),
    ]
