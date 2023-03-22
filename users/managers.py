from django.contrib.auth.models import User
from django.db import models
import users.models


class ProfileManager(models.Manager):
    def activated(self):
        return (
            self.get_queryset()
            .select_related(users.models.Profile.user.field.name)
            .filter(user__is_active=True)
            .only(
                f'{users.models.Profile.user.field.name}__{User.first_name.field.name}',
                f'{users.models.Profile.user.field.name}__{User.last_name.field.name}',
                users.models.Profile.birthday.field.name,
            )
        )
