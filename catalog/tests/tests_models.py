from django.core.exceptions import ValidationError
from django.test import TestCase
import parameterized.parameterized

from catalog.models import Category
from catalog.models import Item
from catalog.models import Tag


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            id=123, name='Установочная тестовая категория', slug='setup-test-category-slug'
        )
        cls.tag = Tag.objects.create(id=123, name='Установочный тестовый тег', slug='setup-test-tag-slug')
        super().setUpTestData()

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        super().tearDown()

    @parameterized.parameterized.expand(
        [
            ('Привет, мир, без роскоши и прекрас!',),
            ('нероскошный',),
            ('превосходительство',),
            ('роскошное',),
        ]
    )
    def test_without_excellent_or_luxurious(self, test_text):
        item_count = Item.objects.count()
        with self.assertRaises(ValidationError):
            item = Item(
                id=1,
                name='Тестовый товар',
                category=self.category,
                text=test_text,
            )
            item.full_clean()
            item.save()
            item.tags.add(self.tag)

        self.assertEqual(Item.objects.count(), item_count)

    @parameterized.parameterized.expand(
        [
            ('Он смотрится превосходно',),
            ('Выглядит роскошно!',),
            ('Очень роскошно и так превосходно',),
            ('Просто превосходно, нет слов',),
            ('Так роскошно, не верится своим глазам',),
        ]
    )
    def test_with_excellent_or_luxurious(self, test_text):
        item_count = Item.objects.count()
        item = Item(
            id=1,
            name='Тестовый товар',
            category=self.category,
            text=test_text,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)
        self.assertEqual(Item.objects.count(), item_count + 1)

    @parameterized.parameterized.expand(
        [(-1,), (-1234,), (32768,), (1000000,)]
    )
    def test_without_allowable_weight(self, test_weight):
        category_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            category = Category(
                id=1,
                name='Тестовая категория',
                slug='test-slug',
                weight=test_weight,
            )
            category.full_clean()
            category.save()

        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.parameterized.expand([(0,), (32767,), (100,), (1234,)])
    def test_with_allowable_weight(self, test_weight):
        category_count = Category.objects.count()
        category = Category(
            id=1,
            name='Тестовая категория',
            slug='test-slug',
            weight=test_weight,
        )
        category.full_clean()
        category.save()
        self.assertEqual(Category.objects.count(), category_count + 1)

    @parameterized.parameterized.expand(
        [
            ('Нормализованный ТеКсТ', 'нормализованныйтекст'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('п!!!р.Ив:е?т', 'привет'),
            ('EnglisH', 'еnglisн'),
        ]
    )
    def test_normalization_category(self, first_name, second_name):
        category_1 = Category(
            id=1,
            name=first_name,
            slug='test-slug',
        )
        category_1.full_clean()
        category_1.save()
        category_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            category_2 = Category(
                id=1,
                name=second_name,
                slug='test-slug',
            )
            category_2.full_clean()
            category_2.save()

        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.parameterized.expand(
        [
            ('Нормализованный ТеКсТ', 'нормализованныйтекст'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('п!!!р.Ив:е?т', 'привет'),
            ('EnglisH', 'еnglisн'),
        ]
    )
    def test_normalization_tag(self, first_name, second_name):
        tag_1 = Tag(
            id=1,
            name=first_name,
            slug='test-slug',
        )
        tag_1.full_clean()
        tag_1.save()
        tag_count = Tag.objects.count()
        with self.assertRaises(ValidationError):
            tag_2 = Tag(
                id=1,
                name=second_name,
                slug='test-slug',
            )
            tag_2.full_clean()
            tag_2.save()

        self.assertEqual(Tag.objects.count(), tag_count)
