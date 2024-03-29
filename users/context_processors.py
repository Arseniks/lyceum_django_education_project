import datetime

import django
import django.utils.timezone

import users.models


def birthday_people(request):
    active_user_with_births = users.models.Profile.objects.activated().filter(
        birthday__isnull=False
    )
    births = []
    if active_user_with_births:
        births = (
            users.models.Profile.objects.activated()
            .only(
                f'{users.models.Profile.user.field.name}__'
                f'{users.models.User.email.field.name}',
                f'{users.models.Profile.user.field.name}__'
                f'{users.models.User.first_name.field.name}',
                users.models.Profile.birthday.field.name,
            )
            .filter(
                birthday__day__range=[
                    (
                        django.utils.timezone.now()
                        - datetime.timedelta(hours=26)
                    ).day,
                    (
                        django.utils.timezone.now()
                        + datetime.timedelta(hours=26)
                    ).day,
                ],
                birthday__month__range=[
                    (
                        django.utils.timezone.now()
                        - datetime.timedelta(hours=26)
                    ).month,
                    (
                        django.utils.timezone.now()
                        + datetime.timedelta(hours=26)
                    ).month,
                ],
            )
        )
    return {
        'births': births,
    }
