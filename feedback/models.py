from django.db import models


class Feedback(models.Model):
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


class FeedbackFiles(models.Model):
    def saving_path(self):
        return f'uploads/{self.pk}/'

    files = models.FileField(
        'файлы',
        upload_to=saving_path,
        null=True,
        default=None,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name='Файлы',
        help_text='Прикрепите файлы',
        default=None,
    )

    class Meta:
        verbose_name = 'Файл фидбека'
        verbose_name_plural = 'Файлы фидбека'


class FeedbackText(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name='Текст',
        help_text='Напишите ваш отзыв',
        primary_key=True,
    )
    text = models.TextField(
        'фидбэк',
        help_text='Напишите отзыв о нашем сайте',
        null=True,
    )

    class Meta:
        verbose_name = 'Текст фидбека'
        verbose_name_plural = 'Тексты фидбека'
