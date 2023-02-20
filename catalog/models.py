from functools import wraps

import django.core.exceptions
import django.core.validators
import django.db.models

from Core.models import AbstractItemModel


def validate_must_contain(*args):
    @wraps(validate_must_contain)
    def validator(value):
        must_words = set(args)
        text = value.lower()

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


class Tag(AbstractItemModel):
    slug = django.db.models.CharField(
        'URL slug',
        help_text='Напишите URL slug вашего товара',
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Item(AbstractItemModel):
    text = django.db.models.TextField(
        'Описание',
        help_text='Опишите товар',
        default=None,
        validators=[validate_must_contain('превосходно', 'роскошно')],
    )
    category = django.db.models.ForeignKey(
        'category',
        default=None,
        on_delete=django.db.models.CASCADE,
        related_name='items',
    )
    tags = django.db.models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(AbstractItemModel):
    slug = django.db.models.CharField(
        'URL slug',
        help_text='Напишите URL slug вашей категории',
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        return self.name
