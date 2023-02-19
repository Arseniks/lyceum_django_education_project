# Generated by Django 3.2.17 on 2023-02-19 18:41

import re

import django.core.validators
from django.db import migrations
from django.db import models

import catalog.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'is_published',
                    models.BooleanField(
                        default=True,
                        help_text='Объект опубликован',
                        verbose_name='Опубликован',
                    ),
                ),
                (
                    'id',
                    models.IntegerField(
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Назовите объект',
                        max_length=150,
                        verbose_name='Название',
                    ),
                ),
                (
                    'slug',
                    models.CharField(
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[-a-zA-Z0-9_]+\\Z'),
                                'Enter a valid “slug” consisting of letters,'
                                ' numbers, underscores or hyphens.',
                                'invalid',
                            )
                        ],
                    ),
                ),
                (
                    'weight',
                    models.IntegerField(
                        default=100,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                    ),
                ),
            ],
            options={
                'verbose_name': 'Каталог',
                'verbose_name_plural': 'Каталоги',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                (
                    'id',
                    models.IntegerField(
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True,
                        help_text='Объект опубликован',
                        verbose_name='Опубликован',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Назовите объект',
                        max_length=150,
                        verbose_name='Название',
                    ),
                ),
                (
                    'text',
                    models.TextField(
                        default=None,
                        help_text='Опишите объект',
                        validators=[
                            catalog.models.excellent_or_luxurious_in_field_validator
                        ],
                        verbose_name='Описание',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.IntegerField(
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Назовите объект',
                        max_length=150,
                        verbose_name='Название',
                    ),
                ),
                (
                    'is_published',
                    models.BooleanField(
                        default=True,
                        help_text='Объект опубликован',
                        verbose_name='Опубликован',
                    ),
                ),
                (
                    'slug',
                    models.CharField(
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile('^[-a-zA-Z0-9_]+\\Z'),
                                'Enter a valid “slug” consisting of letters,'
                                ' numbers, underscores or hyphens.',
                                'invalid',
                            )
                        ],
                    ),
                ),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
    ]
