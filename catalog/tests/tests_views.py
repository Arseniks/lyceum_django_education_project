from django.test import Client
from django.test import TestCase
from django.urls import reverse
import parameterized

from catalog.models import Category
from catalog.models import Item


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            name='Тестовая категория',
            slug='test-category-slug',
        )
        for i in range(101):
            Item.objects.create(
                name=f'Test item {i}',
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
        cls.category = Category.objects.create(
            name='Тестовая категория',
            slug='test-category-slug',
        )
        Item.objects.create(
            name='Test item 1',
            text='превосходно',
            category=cls.category,
        )

    def tearDown(self):
        Item.objects.all().delete()
        Category.objects.all().delete()
        super().tearDown()

    def test_catalog_shown_correct_context_item_list(self):
        response = Client().get(reverse('catalog:item_list'))
        self.assertIn('items', response.context)

    def test_catalog_shown_correct_context_item_detail(self):
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertIn('item', response.context)
