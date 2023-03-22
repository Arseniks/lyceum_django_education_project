from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from users.managers import PersonManager
from users.managers import ProfileManager


class Person(User):
    objects = PersonManager()

    class Meta:
        proxy = True

    def clean(self):
        is_normalized_email_already_exist = Profile.objects.filter(
            normalized_email=Person.get_normalized_email(self.email)
        ).exists()
        if is_normalized_email_already_exist:
            raise ValidationError(
                'Пользователь с такой почтой уже существует'
            )
        super().clean()

    def save(self, *args, **kwargs):
        super().save()
        normalized_email = Person.get_normalized_email(self.email)
        profile = Profile(user=self, normalized_email=normalized_email)
        profile.save()

    @classmethod
    def get_normalized_email(cls, email):
        username, domain = email.strip().rsplit('@', 1)
        username_no_tags = username.split('+')[0].lower()
        if domain.lower() in ['yandex.ru', 'ya.ru']:
            username_no_tags = username_no_tags.replace('.', '-')
            domain = 'yandex.ru'
        if domain.lower() == 'gmail.com':
            username_no_tags = username_no_tags.replace('.', '')
        email = '@'.join([username_no_tags, domain.lower()])

        return email


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    normalized_email = models.EmailField(
        'Нормализованная почта',
        unique=True,
        default=None,
    )
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
        default=0,
    )
    login_failed_count = models.IntegerField(
        'количество неудачных входов в аккаунт',
        default=0,
    )
    freezing_account_data = models.DateTimeField(
        'день заморозки аккаунта',
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'
