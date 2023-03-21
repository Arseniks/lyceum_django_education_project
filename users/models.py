from django.contrib.auth.models import User
from django.db import models

from users.managers import PersonManager
from users.managers import ProfileManager


class Person(User):
    objects = PersonManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(
        'день рождения',
        null=True,
        blank=True,
    )
    image = models.ImageField(
        'аватарка пользователя',
        upload_to='users/',
        default=None,
    )
    coffee_count = models.IntegerField(
        'количество варок кофе',
    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'
