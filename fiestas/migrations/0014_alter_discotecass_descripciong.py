# Generated by Django 4.0.2 on 2023-02-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiestas', '0013_alter_discotecass_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discotecass',
            name='descripciong',
            field=models.TextField(max_length=3000, null=True, verbose_name='descripcion grande'),
        ),
    ]