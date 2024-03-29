# Generated by Django 3.2.17 on 2023-03-26 18:45

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='mark',
            field=models.IntegerField(
                choices=[
                    (1, 'Ненависть'),
                    (2, 'Неприязнь'),
                    (3, 'Нейтрально'),
                    (4, 'Обожание'),
                    (5, 'Любовь'),
                ],
                default=0,
                help_text='оцените товар',
                verbose_name='оценка',
            ),
            preserve_default=False,
        ),
    ]
