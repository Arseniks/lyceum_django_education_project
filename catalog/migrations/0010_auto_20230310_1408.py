# Generated by Django 3.2.17 on 2023-03-10 14:08

import datetime

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0009_auto_20230310_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='change_date',
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 10, 14, 8, 7, 189718),
                verbose_name='Дата изменения',
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='creation_date',
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 10, 14, 8, 7, 189708),
                verbose_name='Дата создания',
            ),
        ),
    ]
