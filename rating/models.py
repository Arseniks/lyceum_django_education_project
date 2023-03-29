import django.db.models

import catalog.models
import users.models


class Mark(django.db.models.Model):
    user = django.db.models.ForeignKey(
        users.models.Person,
        verbose_name='пользователь',
        help_text='кто поставил оценку?',
        on_delete=django.db.models.CASCADE,
        unique=False,
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        verbose_name='товар',
        help_text='товар, на который поставлена оценка',
        on_delete=django.db.models.CASCADE,
        unique=False,
    )

    class MarkChoices(django.db.models.IntegerChoices):
        HATE = (1, 'ненависть')
        DISLIKE = (2, 'неприязнь')
        NEUTRAL = (3, 'нейтрально')
        ADORATION = (4, 'обожание')
        LOVE = (5, 'любовь')

    mark = django.db.models.IntegerField(
        'оценка',
        help_text='оцените товар',
        choices=MarkChoices.choices,
        unique=False,
    )

    date_created = django.db.models.DateTimeField(
        'время создания',
        help_text='когда была поставлена оценка?',
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f'Оценка от пользователя {self.user.username} '
            f'на товар {self.item.name}'
        )

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
