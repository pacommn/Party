# Generated by Django 4.0.2 on 2023-02-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiestas', '0022_alter_entradas_carritoid'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradas',
            name='total',
            field=models.IntegerField(null=True, verbose_name='total'),
        ),
    ]
