import datetime

from . import models


def birthday_people(request):
    today = datetime.datetime.utcnow().strftime('%d.%m.%Y')
    user_date = request.COOKIES.get('django_date', today).split('.')

    births = models.Profile.objects.activated().only(
        f'{models.Profile.user.field.name}__'
        f'{models.User.email.field.name}',

        f'{models.Profile.user.field.name}__'
        f'{models.User.first_name.field.name}'
    ).filter(
        birthday__day=user_date[0],
        birthday__month=user_date[1],
    )

    return {
        'births': births
    }
