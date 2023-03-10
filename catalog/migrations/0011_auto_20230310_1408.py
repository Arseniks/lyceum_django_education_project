# Generated by Django 3.2.17 on 2023-03-10 14:08

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0010_auto_20230310_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='change_date',
            field=models.DateTimeField(
                auto_now=True, verbose_name='Дата изменения'
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='creation_date',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='Дата создания'
            ),
        ),
    ]