# Generated by Django 4.0.2 on 2023-03-03 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fiestas', '0027_alter_entradas_correo_entrega'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entradas',
            old_name='correo_entrega',
            new_name='correo_de_entrega',
        ),
    ]