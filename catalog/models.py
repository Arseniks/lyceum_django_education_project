from functools import wraps
import re
import string

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

    def normalization(self):
        result_name = ''
        for letter in self.name.lower():
            if letter not in set(string.punctuation + ' '):
                result_name += letter

        english_letters_same_with_russian = {
            'a': 'а',
            'b': 'в',
            'e': 'е',
            'k': 'к',
            'm': 'м',
            'h': 'н',
            'o': 'о',
            'p': 'р',
            'c': 'с',
            'y': 'у',
            'x': 'х',
        }
        result_name = list(result_name)
        for num, letter in enumerate(result_name):
            if letter in english_letters_same_with_russian.keys():
                result_name[num] = english_letters_same_with_russian[letter]
        result_name = ''.join(result_name)

        unique_names = [i.unique_name for i in Tag.objects.all()]
        for unique_name in unique_names:
            if unique_name == result_name:
                raise django.core.exceptions.ValidationError(
                    f"Такое имя уже существует"
                )

        return result_name

    def clean(self):
        self.is_cleaned = True
        if not self.unique_name:
            self.unique_name = self.normalization()
        return super().clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)

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

    def normalization(self):
        result_name = ''
        for letter in self.name.lower():
            if letter not in set(string.punctuation + ' '):
                result_name += letter

        english_letters_same_with_russian = {
            'a': 'а',
            'b': 'в',
            'e': 'е',
            'k': 'к',
            'm': 'м',
            'h': 'н',
            'o': 'о',
            'p': 'р',
            'c': 'с',
            'y': 'у',
            'x': 'х',
        }
        result_name = list(result_name)
        for num, letter in enumerate(result_name):
            if letter in english_letters_same_with_russian.keys():
                result_name[num] = english_letters_same_with_russian[letter]
        result_name = ''.join(result_name)

        unique_names = [i.unique_name for i in Category.objects.all()]
        for unique_name in unique_names:
            if unique_name == result_name:
                raise django.core.exceptions.ValidationError(
                    f"Такое имя уже существует"
                )

        return result_name

    def clean(self):
        self.is_cleaned = True
        if not self.unique_name:
            self.unique_name = self.normalization()
        return super().clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)

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
    category = django.db.models.OneToOneField(
        Category,
        default=None,
        on_delete=django.db.models.CASCADE,
    )
    tags = django.db.models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
