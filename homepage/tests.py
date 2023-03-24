from django.test import Client
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category
from catalog.models import Item
from catalog.models import Tag


class StaticURLTests(TestCase):
    def test_homepage_home_endpoint(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_teapot_endpoint(self):
        response = Client().get('/coffee')
        self.assertEqual(response.status_code, 418)

    def test_homepage_teapot_endpoint_answer(self):
        response = Client().get('/coffee')
        self.assertEqual(
            response.content.decode('utf-8'), '<body>Я чайник</body>'
        )


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
            text='Неопубликованный тестовый товар',
            category=cls.category_published,
        )
        cls.item_first = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='АААААА',
            text='превосходно',
            category=cls.category_published,
        )

        cls.item_second = Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='ББББББ',
            text='превосходно',
            category=cls.category_published,
        )

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

    def test_homepage_shown_context_home(self):
        response = Client().get(reverse('homepage:home'))
        self.assertIn('items', response.context)

    def test_homepage_shown_correct_items_in_context_home(self):
        response = Client().get(reverse('homepage:home'))
        self.assertIn(
            self.item_published_with_category_published,
            response.context['items'],
        )
        self.assertNotIn(
            self.item_published_with_category_unpublished,
            response.context['items'],
        )
        self.assertNotIn(self.item_unpublished, response.context['items'])

    def test_homepage_shown_correct_categories_in_context_home(self):
        response = Client().get(reverse('homepage:home'))
        self.assertNotIn('category', response.context)

    def test_homepage_shown_correct_tags_in_context_home(self):
        response = Client().get(reverse('homepage:home'))
        self.assertIn(
            self.tag_published, response.context['items'][2].tags.all()
        )
        self.assertNotIn(
            self.tag_unpublished, response.context['items'][2].tags.all()
        )

    def test_homepage_shown_context_sorting_home(self):
        response = Client().get(reverse('homepage:home'))
        self.assertEqual('АААААА', response.context['items'][0].name)
        self.assertEqual('ББББББ', response.context['items'][1].name)
