from django.contrib.auth.models import User
from django.db import models

import users.models


class PersonManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(User.profile.related.related_name)
        )


class ProfileManager(models.Manager):
    def activated(self):
        return (
            self.get_queryset()
            .select_related(users.models.Profile.user.field.name)
            .filter(user__is_active=True)
            .only(
                f'{users.models.Profile.user.field.name}'
                f'__{User.first_name.field.name}',
                f'{users.models.Profile.user.field.name}'
                f'__{User.last_name.field.name}',
                users.models.Profile.birthday.field.name,
            )
        )
