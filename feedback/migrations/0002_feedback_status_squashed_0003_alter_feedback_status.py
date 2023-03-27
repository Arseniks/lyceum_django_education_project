# Generated by Django 3.2.17 on 2023-03-24 11:59

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    replaces = [
        ('feedback', '0002_feedback_status'),
        ('feedback', '0003_alter_feedback_status'),
    ]

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='status',
            field=models.CharField(
                choices=[
                    ('получено', 'Получено'),
                    ('в обработке', 'в обработке'),
                    ('ответ дан', 'ответ дан'),
                ],
                default='получено',
                max_length=11,
            ),
        ),
    ]