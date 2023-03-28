import datetime

import users.models


def birthday_people(request):
    today = datetime.datetime.utcnow().strftime('%d.%m.%Y')
    user_date = request.COOKIES.get('django_date', today).split('.')

    births = (
        users.models.Profile.objects.activated()
        .only(
            f'{users.models.Profile.user.field.name}__'
            f'{users.models.User.email.field.name}',
            f'{users.models.Profile.user.field.name}__'
            f'{users.models.User.first_name.field.name}',
        )
        .filter(
            birthday__day=user_date[0],
            birthday__month=user_date[1],
        )
    )

    return {
        'births': births,
    }
