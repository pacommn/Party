# Generated by Django 4.0.2 on 2023-03-03 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiestas', '0026_entradas_correo_entrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradas',
            name='correo_entrega',
            field=models.CharField(max_length=100, null=True, verbose_name='correo de entrega'),
        ),
    ]
