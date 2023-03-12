from django.db import models


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
    status = models.TextField(
        'статус',
        default='получено',
        choices=[
            ('получено', 'получено'),
            ('в обработке', 'в обработке'),
            (
                'ответ дан',
                'ответ дан',
            ),
        ],
    )

    def __str__(self):
        return 'Отзыв №' + str(self.pk)

    class Meta:
        verbose_name = 'фидбэк'
        verbose_name_plural = 'фидбэки'
