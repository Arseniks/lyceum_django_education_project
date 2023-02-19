# Generated by Django 3.2.17 on 2023-02-19 20:16

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20230219_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(help_text='Напишите URL slug вашей категории', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')], verbose_name='URL slug'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(help_text='Напишите URL slug вашего товара', max_length=200, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')], verbose_name='URL slug'),
        ),
    ]
