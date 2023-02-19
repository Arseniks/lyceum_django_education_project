import django.core.exceptions
import django.core.validators
import django.db.models

from Core.models import AbstractModel


def excellent_or_luxurious_in_field_validator(value):
    value = value.lower()
    if 'превосходно' not in value and 'роскошно' not in value:
        raise django.core.exceptions.ValidationError(
            'В тексте должно быть слово превосходно или роскошно'
        )


class Tag(AbstractModel):
    slug = django.db.models.CharField(
        'URL slug',
        help_text='Напишите URL slug вашего товара',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.validate_slug
        ],
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Item(AbstractModel):
    text = django.db.models.TextField(
        'Описание',
        help_text='Опишите товар',
        default=None,
        validators=[
            excellent_or_luxurious_in_field_validator
        ],
    )
    category = django.db.models.ForeignKey(
        'category',
        default=None,
        on_delete=django.db.models.CASCADE,
        related_name='items'
    )
    tags = django.db.models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class Category(AbstractModel):
    slug = django.db.models.CharField(
        'URL slug',
        help_text='Напишите URL slug вашей категории',
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.validate_slug
        ],
    )
    weight = django.db.models.IntegerField(
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767)
        ],
    )

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        return self.name
