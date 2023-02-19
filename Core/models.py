import django.db.models
import django.core.validators


class AbstractModel(django.db.models.Model):
    id = django.db.models.IntegerField(
        primary_key=True,
        validators=[
            django.core.validators.MinValueValidator(1)
        ],
    )
    name = django.db.models.CharField(
        'Название',
        help_text='Введите назовите',
        max_length=150,
    )
    is_published = django.db.models.BooleanField(
        'Опубликован',
        help_text='Объект опубликован',
        default=True,
    )

    class Meta:
        abstract = True

