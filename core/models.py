import string

import django.db.models
from django.utils.safestring import mark_safe
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete
from sorl.thumbnail import get_thumbnail
from transliterate import translit


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
    unique_name = django.db.models.CharField(
        max_length=150, unique=True, editable=False, default=None
    )

    def normalization(self):
        result_name = ''
        for letter in self.name.lower():
            if letter not in set(string.punctuation + ' '):
                result_name += letter
        result_name = translit(result_name, 'ru')

        matches = self.__class__.objects.filter(unique_name=result_name)
        if list(matches):
            raise django.core.exceptions.ValidationError(
                'Такое имя уже существует'
            )

        return result_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.unique_name = self.normalization()
        return super().clean()

    class Meta:
        abstract = True


class ImageBaseModel(django.db.models.Model):
    image = django.db.models.ImageField(
        'изображение товара',
        upload_to='catalog/',
        default=None,
    )

    @property
    def get_image(self):
        return get_thumbnail(self.image, '300x300', crop='center', quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.get_image.url}" ')
        return 'Нет изображения'

    image_tmb.short_description = 'превью'
    image_tmb.allow_tags = True

    def item_name(self):
        return self.item.name

    item_name.short_description = 'товар'

    def sorl_delete(**kwargs):
        delete(kwargs['file'])

    cleanup_pre_delete.connect(sorl_delete)

    class Meta:
        abstract = True
