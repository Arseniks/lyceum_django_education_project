import django.db.models


class AbstractItemModel(django.db.models.Model):
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


class UniqueNamesModel(django.db.models.Model):
    is_cleaned = False
    unique_name = django.db.models.CharField(
        max_length=150, unique=True, editable=False, default=None
    )

    class Meta:
        abstract = True
