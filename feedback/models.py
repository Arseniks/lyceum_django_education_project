from django.db import models
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
    text = models.TextField(
        'фидбэк',
        help_text='Напишите отзыв о нашем сайте',
    )
    created_on = models.DateTimeField(
        'дата написания',
        auto_now_add=True,
    )
    mail = models.EmailField(
        'почта',
        default='user_mail@example.com',
        help_text='Введите почту',
    )

    class Status(models.TextChoices):
        GOT = 'получено', _('Получено')
        IN_PROGRESS = 'в обработке', _('в обработке')
        ANSWER_GIVEN = 'ответ дан', _('ответ дан')

    status = models.CharField(
        max_length=11,
        choices=Status.choices,
        default=Status.GOT,
    )

    def __str__(self):
        return 'Отзыв №' + str(self.pk)

    class Meta:
        verbose_name = 'фидбэк'
        verbose_name_plural = 'фидбэки'
