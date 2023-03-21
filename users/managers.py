from django.contrib.auth.models import User
from django.db import models


class ProfileManager(models.Manager):
    def activated(self):
        from users.models import Profile

        return (
            self.get_queryset()
            .select_related(Profile.user.field.name)
            .filter(user__is_active=True)
            .only(
                f'{Profile.user.field.name}__{User.first_name.field.name}',
                f'{Profile.user.field.name}__{User.last_name.field.name}',
                Profile.birthday.field.name,
            )
        )
