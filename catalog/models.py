from functools import wraps
import re

import django.core.exceptions
import django.core.validators
import django.db.models

from Core.models import AbstractItemModel
from Core.models import UniqueNamesModel


def validate_must_contain(*args):
    @wraps(validate_must_contain)
    def validator(value):
        must_words = set(args)
        text = value.lower()
        text = re.findall(r'\b.*?\b', text)

        wrong_text = True
        for word in must_words:
            if word in text:
                wrong_text = False
                break

        if wrong_text:
            raise django.core.exceptions.ValidationError(
                f'Обязательно нужно использовать {" ".join(must_words)}'
            )
        return value

    return validator


class Tag(AbstractItemModel, UniqueNamesModel):
    slug = django.db.models.SlugField(
        'URL slug',
        help_text='Напишите URL slug вашего товара',
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Category(AbstractItemModel, UniqueNamesModel):
    slug = django.db.models.SlugField(
        'URL slug',
        help_text='Напишите URL slug вашей категории',
        max_length=200,
        unique=True,
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Item(AbstractItemModel):
    text = django.db.models.TextField(
        'Описание',
        help_text='Опишите товар',
        default=None,
        validators=[validate_must_contain('превосходно', 'роскошно')],
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name='Категория',
        help_text='Выберите категорию',
    )
    tags = django.db.models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
