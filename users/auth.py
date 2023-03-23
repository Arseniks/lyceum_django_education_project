from datetime import datetime

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.mail import send_mail


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                user.profile.login_failed_count += 1
                if (
                    user.profile.login_failed_count
                    == settings.NUMBER_OF_FAILED_LOGIN
                ):
                    user.is_active = False
                    user.profile.freezing_account_data = datetime.now()
                    send_mail(
                        'Письмо восстановления аккаунта',
                        'В ваш аккаунт было совершено множество неудачных'
                        ' попыток входа на сайте KittyShop!\n'
                        'Мы заморозили ваш аккаунт для'
                        ' предотвращения мошеннических действий.\n'
                        'Вы можете сменить пароль во избежание '
                        'взлома, а также  '
                        'восстановить пароль, если вы забыли '
                        'его, на нашем сайте.\n'
                        'Для разморозки аккаунта и продолжения '
                        'использования сайта KittyShop перейдите по ссылке: '
                        'http://127.0.0.1:8000/auth/recovery/'
                        f'{user.username}',
                        settings.FEEDBACK_MAIL,
                        [f'{user.email}'],
                        fail_silently=False,
                    )
                    user.save()
                user.profile.save()
                return None
        except User.DoesNotExist:
            return None
