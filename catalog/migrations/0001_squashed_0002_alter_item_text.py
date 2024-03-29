# Generated by Django 3.2.17 on 2023-02-23 21:05

import django.core.validators
from django.db import migrations
from django.db import models
import django.db.models.deletion

import catalog.models


class Migration(migrations.Migration):
    replaces = [
        ('catalog', '0001_initial'),
        ('catalog', '0002_alter_item_text'),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите назовите',
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
                    'unique_name',
                    models.CharField(
                        default=None,
                        editable=False,
                        max_length=150,
                        unique=True,
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Напишите URL slug вашей категории',
                        max_length=200,
                        unique=True,
                        verbose_name='URL slug',
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
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите назовите',
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
                    'unique_name',
                    models.CharField(
                        default=None,
                        editable=False,
                        max_length=150,
                        unique=True,
                    ),
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Напишите URL slug вашего товара',
                        max_length=200,
                        unique=True,
                        verbose_name='URL slug',
                    ),
                ),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        help_text='Введите назовите',
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
                    'text',
                    models.TextField(
                        default=None,
                        help_text='Опишите товар',
                        validators=[catalog.models.ValidateMustContain],
                        verbose_name='Описание',
                    ),
                ),
                (
                    'category',
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='catalog.category',
                    ),
                ),
                ('tags', models.ManyToManyField(blank=True, to='catalog.Tag')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
    ]
