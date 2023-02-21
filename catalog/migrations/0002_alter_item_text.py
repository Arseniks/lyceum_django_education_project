# Generated by Django 3.2.17 on 2023-02-21 20:52

from django.db import migrations
from django.db import models

import catalog.models


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(
                default=None,
                help_text='Опишите товар',
                validators=[catalog.models.validate_must_contain],
                verbose_name='Описание',
            ),
        ),
    ]
