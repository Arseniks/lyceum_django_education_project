# Generated by Django 3.2.17 on 2023-03-24 12:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            'users',
            '0005_auto_20230322_1209_squashed_0006_alter_profile_freezing_account_data',
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='freezing_account_data',
            new_name='freezing_account_date',
        ),
    ]
