import django.db.models

import catalog.models
import users.models


class Mark(django.db.models.Model):
    user = django.db.models.ForeignKey(
        users.models.Person,
        verbose_name='кто поставил оценку?',
        on_delete=django.db.models.CASCADE,
        unique=False,
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        verbose_name='товар',
        on_delete=django.db.models.CASCADE,
        unique=False,
    )

    mark_choices = django.db.models.IntegerChoices(
        'mark_choices',
        'Ненависть Неприязнь Нейтрально Обожание Любовь',
    )
    mark = django.db.models.IntegerField(
        'оценка',
        help_text='оцените товар',
        choices=mark_choices.choices,
        unique=False,
    )

    def __str__(self):
        return (
            f'Оценка от пользователя id = {self.user.id} '
            f'на товар {self.item.id}'
        )

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
