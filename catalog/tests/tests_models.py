import django.core.exceptions

from catalog.models import Category, Item, Tag
from django.core.exceptions import ValidationError
from django.test import TestCase


class ModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            id=1,
            name='Тестовая категория',
            slug='test-category-slug',
        )
        cls.tag = Tag.objects.create(
            id=1,
            name='Тестовая тэг',
            slug='test-tag-slug',
        )

    def test_without_excellent_or_luxurious(self):
        item_count = Item.objects.count()
        test_texts = [
            'Привет, мир, без роскоши и прекрас!',
            'нероскошный',
            'превосходительство',
        ]
        for text in test_texts:
            Item.objects.all().delete()
            with self.assertRaises(ValidationError):
                self.item = Item(
                    id=1,
                    name='Тестовый товар',
                    category=self.category,
                    text=text,
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)

            self.assertEqual(Item.objects.count(), item_count)

    def test_with_excellent_or_luxurious(self):
        item_count = Item.objects.count()
        test_texts = [
            'Он смотрится превосходно',
            'Выглядит роскошно',
            'Очень роскошно и так превосходно',
            'Просто превосходно!',
            'Так роскошно, не верится своим глазам',
        ]
        for text in test_texts:
            Item.objects.all().delete()
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = Item(
                    id=1,
                    name='Тестовый товар',
                    category=self.category,
                    text=text,
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)
            self.assertEqual(Item.objects.count(), item_count + 1)
