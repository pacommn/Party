# Generated by Django 4.0.2 on 2023-05-08 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiestas', '0035_alter_usuarios_edad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='dni',
            field=models.CharField(max_length=9, null=True, verbose_name='dni'),
        ),
    ]
