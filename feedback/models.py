from django.db import models
from django.utils.translation import gettext_lazy as _


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


class FeedbackFiles(models.Model):
    def saving_path(self, filename):
        return 'uploads/{0}/{1}'.format(self.feedback.pk, filename)

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

    def __str__(self):
        return self.files.name

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
        blank=True,
    )

    def __str__(self):
        return 'Текст отзыва №' + str(self.feedback.pk)

    class Meta:
        verbose_name = 'Текст фидбека'
        verbose_name_plural = 'Тексты фидбека'
