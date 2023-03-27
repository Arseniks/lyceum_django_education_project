# Generated by Django 3.2.17 on 2023-03-22 20:29

from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ('users', '0001_initial'),
        ('users', '0002_auto_20230319_0859'),
        ('users', '0003_profile_image'),
        ('users', '0004_auto_20230319_0903'),
    ]

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
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        default=None,
                        upload_to='users/',
                        verbose_name='аватарка пользователя',
                    ),
                ),
            ],
            options={
                'verbose_name': 'профиль пользователя',
                'verbose_name_plural': 'профили пользователей',
            },
        ),
    ]