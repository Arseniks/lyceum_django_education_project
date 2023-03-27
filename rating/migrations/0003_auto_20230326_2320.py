# Generated by Django 3.2.17 on 2023-03-26 19:20

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20230223_2243_squashed_0011_auto_20230310_1408'),
        ('users', '0006_rename_freezing_account_data_profile_freezing_account_date'),
        ('rating', '0002_mark_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.item', verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.person', verbose_name='кто поставил оценку?'),
        ),
    ]
