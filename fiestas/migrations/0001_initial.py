# Generated by Django 4.0.2 on 2022-10-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discotecas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('foto', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Foto')),
                ('direccion', models.TextField(null=True, verbose_name='Direccion')),
            ],
        ),
    ]
