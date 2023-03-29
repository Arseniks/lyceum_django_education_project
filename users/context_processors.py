import datetime

from django.utils import timezone

import django

import users.models


def birthday_people(request):
    births = (
        users.models.Profile.objects.activated()
        .only(
            f'{users.models.Profile.user.field.name}__'
            f'{users.models.User.email.field.name}',
            f'{users.models.Profile.user.field.name}__'
            f'{users.models.User.first_name.field.name}',
        )
        .filter(
            birthday__day__range=[
                (django.utils.timezone.now() - datetime.timedelta(hours=26)).day,
                (django.utils.timezone.now() + datetime.timedelta(hours=26)).day,
            ],
            birthday__month__range=[
                (django.utils.timezone.now() - datetime.timedelta(hours=26)).month,
                (django.utils.timezone.now() + datetime.timedelta(hours=26)).month,
            ],

        )
    )
    return {
        'births': births,
    }
