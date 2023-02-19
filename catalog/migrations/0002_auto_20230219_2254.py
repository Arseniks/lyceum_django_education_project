# Generated by Django 3.2.17 on 2023-02-19 19:54

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='items',
                to='catalog.category',
            ),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='catalog.Tag'),
        ),
    ]
