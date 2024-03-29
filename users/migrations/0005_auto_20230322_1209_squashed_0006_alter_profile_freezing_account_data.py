# Generated by Django 3.2.17 on 2023-03-24 11:16

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    replaces = [
        ('users', '0005_auto_20230322_1209'),
        ('users', '0006_alter_profile_freezing_account_data'),
    ]

    dependencies = [
        ('users', '0004_auto_20230319_0903'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='profile',
            name='login_failed_count',
            field=models.IntegerField(
                default=0, verbose_name='количество неудачных входов в аккаунт'
            ),
        ),
        migrations.AlterField(
            model_name='profile',
            name='coffee_count',
            field=models.IntegerField(
                default=0, verbose_name='количество варок кофе'
            ),
        ),
        migrations.AddField(
            model_name='profile',
            name='freezing_account_data',
            field=models.DateTimeField(
                blank=True,
                default=None,
                null=True,
                verbose_name='день заморозки аккаунта',
            ),
        ),
    ]
