# Generated by Django 4.0.2 on 2023-05-08 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiestas', '0038_alter_usuarios_dni_alter_usuarios_edad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='dni',
            field=models.CharField(blank=True, default='', max_length=9, verbose_name='dni'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='edad',
            field=models.CharField(blank=True, default='', max_length=3, verbose_name='edad'),
        ),
    ]