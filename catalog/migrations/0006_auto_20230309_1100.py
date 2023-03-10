# Generated by Django 3.2.17 on 2023-03-09 11:00

import datetime

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0005_item_is_on_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='change_time',
            field=models.DateField(
                default=datetime.datetime(2023, 3, 9, 11, 0, 46, 664171),
                verbose_name='Дата изменения',
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='creation_time',
            field=models.DateField(
                default=datetime.datetime(2023, 3, 9, 11, 0, 46, 664157),
                verbose_name='Дата создания',
            ),
        ),
    ]