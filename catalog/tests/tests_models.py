from django.core.exceptions import ValidationError
from django.test import TestCase
import parameterized.parameterized

from catalog.models import Category
from catalog.models import Item
from catalog.models import Tag


class ModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовая категория', slug='test-category-slug'
        )
        cls.tag = Tag.objects.create(name='Тестовый тег', slug='test-tag-slug')

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
        Item.objects.all().delete()
        item_count = Item.objects.count()
        with self.assertRaises(ValidationError):
            self.category = Item(
                id=1,
                name='Тестовый товар',
                category=self.category,
                text=test_text,
            )
            self.category.full_clean()
            self.category.save()
            self.category.tags.add(self.tag)

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
        Item.objects.all().delete()
        item_count = Item.objects.count()
        self.category = Item(
            id=1,
            name='Тестовый товар',
            category=self.category,
            text=test_text,
        )
        self.category.full_clean()
        self.category.save()
        self.category.tags.add(self.tag)
        self.assertEqual(Item.objects.count(), item_count + 1)

    @parameterized.parameterized.expand(
        [(-1,), (-1234,), (32768,), (1000000,)]
    )
    def test_without_allowable_weight(self, test_weight):
        Category.objects.all().delete()
        category_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            self.category = Category(
                id=1,
                name='Тестовая категория',
                slug='test-slug',
                weight=test_weight,
            )
            self.category.full_clean()
            self.category.save()

        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.parameterized.expand([(0,), (32767,), (100,), (1234,)])
    def test_with_allowable_weight(self, test_weight):
        Category.objects.all().delete()
        category_count = Category.objects.count()
        self.category = Category(
            id=1,
            name='Тестовая категория',
            slug='test-slug',
            weight=test_weight,
        )
        self.category.full_clean()
        self.category.save()
        self.assertEqual(Category.objects.count(), category_count + 1)

    @parameterized.parameterized.expand(
        [
            ('Нормализованный ТеКсТ', 'нормализованныйтекст'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('п\р.И"в^е?т', 'привет'),
            ('EnglisH', 'еnglisн'),
        ]
    )
    def test_normalization_category(self, first_name, second_name):
        Category.objects.all().delete()
        self.category = Category(
            id=1,
            name=first_name,
            slug='test-slug',
        )
        self.category.full_clean()
        self.category.save()
        category_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            self.category = Category(
                id=1,
                name=second_name,
                slug='test-slug',
            )
            self.category.full_clean()
            self.category.save()

        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.parameterized.expand(
        [
            ('Нормализованный ТеКсТ', 'нормализованныйтекст'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('Нормализация - это здорово!', 'нормализацияэтоздорово'),
            ('п\р.И"в^е?т', 'привет'),
            ('EnglisH', 'еnglisн'),
        ]
    )
    def test_normalization_tag(self, first_name, second_name):
        Tag.objects.all().delete()
        self.tag = Tag(
            id=1,
            name=first_name,
            slug='test-slug',
        )
        self.tag.full_clean()
        self.tag.save()
        tag_count = Tag.objects.count()
        with self.assertRaises(ValidationError):
            self.tag = Tag(
                id=1,
                name=second_name,
                slug='test-slug',
            )
            self.tag.full_clean()
            self.tag.save()

        self.assertEqual(Tag.objects.count(), tag_count)
