from django.test import Client
from django.test import TestCase
from django.urls import reverse
import parameterized

from catalog.models import Category
from catalog.models import Item
from catalog.models import Tag


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовая категория',
            slug='test-category-slug',
        )
        Item.objects.create(
            name='Тестовый товар',
            text='превосходно',
            category=cls.category,
        )

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        super().tearDown()

    def test_catalog_item_list_endpoint(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_number_endpoint(self):
        response = Client().get('/catalog/1/')
        self.assertEqual(response.status_code, 200)

    @parameterized.parameterized.expand([(-1,), ('adf',), (1.8,)])
    def test_catalog_number_endpoint_negative(self, number):
        response = Client().get(f'/catalog/{number}/')
        self.assertEqual(response.status_code, 404)

    def test_catalog_converter_endpoint(self):
        response = Client().get('/catalog/converter/1/')
        self.assertEqual(response.status_code, 200)

    @parameterized.parameterized.expand(
        [(-1,), ('adf',), (1.8,), ('00',), ('025',)]
    )
    def test_catalog_converter_endpoint_negative(self, number):
        response = Client().get(f'/catalog/converter/{number}/')
        self.assertEqual(response.status_code, 404)

    def test_catalog_re_endpoint(self):
        response = Client().get('/catalog/re/1/')
        self.assertEqual(response.status_code, 200)

    @parameterized.parameterized.expand(
        [(-1,), ('adf',), (1.8,), ('00',), ('025',)]
    )
    def test_catalog_re_endpoint_negative(self, number):
        response = Client().get(f'/catalog/re/{number}/')
        self.assertEqual(response.status_code, 404)


class ContextTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag_published = Tag.objects.create(
            is_published=True,
            name='Опубликованный тестовый тег',
            slug='published-test-tag-slug',
        )
        cls.tag_unpublished = Tag.objects.create(
            is_published=False,
            name='Неопубликованный тестовый тег',
            slug='unpublished-test-tag-slug',
        )
        cls.category_published = Category.objects.create(
            is_published=True,
            name='Опубликованная тестовая категория',
            slug='published-test-category-slug',
        )
        cls.category_unpublished = Category.objects.create(
            is_published=False,
            name='Неопубликованная тестовая категория',
            slug='unpublished-test-category-slug',
        )
        cls.category_first = Category.objects.create(
            is_published=True,
            name='АААААА',
            slug='first-test-category-slug',
        )
        cls.category_second = Category.objects.create(
            is_published=True,
            name='ББББББ',
            slug='second-test-category-slug',
        )
        cls.item_published_with_category_published = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Опубликованный тестовый товар с опубликованной категорией',
            text='превосходно',
            category=cls.category_published,
        )
        cls.item_published_with_category_unpublished = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Опубликованный тестовый товар c неопубликованной категорией',
            text='превосходно',
            category=cls.category_unpublished,
        )
        cls.item_unpublished = Item.objects.create(
            is_published=False,
            is_on_main=False,
            name='Неопубликованный тестовый товар',
            text='превосходно',
            category=cls.category_published,
        )
        cls.item_first = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Тестовая категория, первая в списке',
            text='превосходно',
            category=cls.category_first,
        )

        cls.item_second = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Тестовая категория, вторая в списке',
            text='превосходно',
            category=cls.category_second,
        )

        cls.item_first.clean()
        cls.item_first.save()
        cls.item_second.clean()
        cls.item_second.save()
        cls.item_published_with_category_published.clean()
        cls.item_published_with_category_published.save()
        cls.item_published_with_category_published.tags.add(cls.tag_published)
        cls.item_published_with_category_published.tags.add(
            cls.tag_unpublished
        )
        cls.item_published_with_category_unpublished.clean()
        cls.item_published_with_category_unpublished.save()
        cls.item_unpublished.clean()
        cls.item_unpublished.save()

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        super().tearDown()

    def test_catalog_shown_context_item_list(self):
        response = Client().get(reverse('catalog:item_list'))

        self.assertIn('items', response.context)
        print(response.context['items'])
        self.assertEqual(3, len(response.context['items']))

    def test_catalog_shown_context_sorting_item_list(self):
        response = Client().get(reverse('catalog:item_list'))
        self.assertEqual(
            'Тестовая категория, первая в списке',
            response.context['items'][0].name,
        )
        self.assertEqual(
            'Тестовая категория, вторая в списке',
            response.context['items'][1].name,
        )

    def test_catalog_shown_correct_items_in_context_item_list(self):
        response = Client().get(reverse('catalog:item_list'))
        self.assertIn(
            self.item_published_with_category_published,
            response.context['items'],
        )
        self.assertNotIn(
            self.item_published_with_category_unpublished,
            response.context['items'],
        )
        self.assertNotIn(self.item_unpublished, response.context['items'])

    def test_catalog_shown_correct_categories_in_context_item_list(self):
        response = Client().get(reverse('catalog:item_list'))
        self.assertIn(self.category_published, response.context['category'])
        self.assertNotIn(
            self.category_unpublished, response.context['category']
        )

    def test_catalog_shown_correct_tags_in_context_item_list(self):
        response = Client().get(reverse('catalog:item_list'))
        self.assertIn(
            self.tag_published, response.context['items'][2].tags.all()
        )
        self.assertNotIn(
            self.tag_unpublished, response.context['items'][2].tags.all()
        )

    def test_catalog_have_context_item_detail(self):
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertIn('item', response.context)

    def test_catalog_shown_have_context_item_detail_negative(self):
        response = Client().get(reverse('catalog:item_detail', args=[100]))
        self.assertEqual(404, response.status_code)

    def test_catalog_shown_correct_items_in_context_item_detail(self):
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertEqual(
            self.item_published_with_category_published,
            response.context['item'],
        )
        self.assertNotEqual(
            self.item_published_with_category_unpublished,
            response.context['item'],
        )
        self.assertNotEqual(self.item_unpublished, response.context['item'])

    def test_catalog_shown_correct_categories_in_context_item_detail(self):
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertEqual(
            self.category_published, response.context['item'].category
        )
        self.assertNotEqual(
            self.category_unpublished, response.context['item'].category
        )

    def test_catalog_shown_correct_tags_in_context_item_detail(self):
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertIn(self.tag_published, response.context['item'].tags.all())
        self.assertNotIn(
            self.tag_unpublished, response.context['item'].tags.all()
        )
