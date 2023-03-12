import re

import django.core.exceptions
import django.core.validators
import django.db.models

from catalog.managers import ItemManager
from catalog.managers import TagManager
from core.models import AbstractItemModel
from core.models import ImageBaseModel
from core.models import UniqueNamesModel


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.must_words = set(words)

    def __call__(self, value):
        normalizable_words = value.lower()
        normalizable_words = re.findall(r'\b.*?\b', normalizable_words)

        wrong_text = True
        for word in self.must_words:
            if word in normalizable_words:
                wrong_text = False
                break

        if wrong_text:
            raise django.core.exceptions.ValidationError(
                f'Обязательно нужно использовать {" ".join(self.must_words)}'
            )
        return value


class Tag(AbstractItemModel, UniqueNamesModel):
    objects = TagManager()

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
    objects = ItemManager()

    creation_date = django.db.models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        editable=False,
    )
    change_date = django.db.models.DateTimeField(
        'Дата изменения',
        auto_now=True,
        editable=False,
    )
    is_on_main = django.db.models.BooleanField(
        'На главной',
        default=False,
    )
    text = django.db.models.TextField(
        'Описание',
        help_text='Опишите товар',
        default=None,
        validators=[ValidateMustContain('превосходно', 'роскошно')],
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
        default_related_name = 'items'


class MainImage(ImageBaseModel):
    item = django.db.models.OneToOneField(
        Item,
        verbose_name='товар',
        on_delete=django.db.models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'главное изображение'
        verbose_name_plural = 'главные изображения'

    def __str__(self):
        return self.item_name()


class ImageGallery(ImageBaseModel):
    item = django.db.models.ForeignKey(
        Item,
        verbose_name='товар',
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фотогалерея товара'

    def __str__(self):
        return self.item_name()
