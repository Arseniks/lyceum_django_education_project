# Generated by Django 3.2.17 on 2023-03-19 08:44

from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
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
                    'first_name',
                    models.CharField(
                        blank=True,
                        max_length=225,
                        null=True,
                        verbose_name='имя',
                    ),
                ),
                (
                    'last_name',
                    models.CharField(
                        blank=True,
                        max_length=225,
                        null=True,
                        verbose_name='фамилия',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        verbose_name='адрес электронной почты',
                    ),
                ),
                (
                    'birthday',
                    models.DateField(
                        blank=True, null=True, verbose_name='день рождения'
                    ),
                ),
                (
                    'coffee_count',
                    models.IntegerField(verbose_name='количество варок кофе'),
                ),
                (
                    'date_joined',
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'профили пользователей',
            },
        ),
    ]