from django.db import models
from django.db.models import Prefetch


class ItemManager(models.Manager):
    def published(self):
        from catalog.models import Item
        from catalog.models import MainImage
        from catalog.models import Tag

        return (
            self.get_queryset()
            .select_related(
                Item.category.field.name, Item.mainimage.related.name
            )
            .filter(is_published=True, category__is_published=True)
            .prefetch_related(
                Prefetch(
                    Item.tags.field.name, queryset=Tag.objects.published()
                )
            )
            .only(
                Item.name.field.name,
                Item.text.field.name,
                f'{Item.category.field.name}__{Item.name.field.name}',
                f'{Item.mainimage.related.name}__{MainImage.image.field.name}',
            )
        )


class TagManager(models.Manager):
    def published(self):
        from catalog.models import Tag

        return (
            self.get_queryset()
            .filter(is_published=True)
            .only(Tag.name.field.name)
        )
