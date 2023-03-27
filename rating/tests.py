from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category
from catalog.models import Item
import rating.methods
from rating.models import Mark
from users.models import Person
from users.models import Profile


class TestMarkLogic(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = Person.objects.create(
            id=1, username='user1', password='123'
        )
        cls.user2 = Person.objects.create(
            id=2, username='user2', password='123'
        )
        cls.profile1 = Profile.objects.create(user_id=1)
        cls.profile2 = Profile.objects.create(user_id=2)
        cls.category = Category.objects.create(
            name='test_category', slug='cat1'
        )
        cls.item1 = Item.objects.create(
            id=1, name='item1', text='роскошно', category=cls.category
        )
        cls.item2 = Item.objects.create(
            id=2, name='item2', text='превосходно', category=cls.category
        )
        super().setUpTestData()

    def tearDown(self):
        Item.objects.all().delete()
        User.objects.all().delete()
        Mark.objects.all().delete()
        super().tearDown()

    def test_create_mark(self):
        marks_count = Mark.objects.count()
        rating.methods.add_mark(self.user1.id, self.item1.id, 3)
        self.assertEqual(Mark.objects.count(), marks_count + 1)

    def test_change_mark(self):
        marks_count = Mark.objects.count()
        rating.methods.add_mark(self.user1.id, self.item1.id, 3)
        rating.methods.add_mark(self.user1.id, self.item1.id, 4)
        self.assertEqual(Mark.objects.count(), marks_count + 1)

    def test_delete_mark(self):
        marks_count = Mark.objects.count()
        rating.methods.add_mark(self.user1.id, self.item1.id, 3)
        rating.methods.add_mark(self.user1.id, self.item1.id, '')
        self.assertEqual(Mark.objects.count(), marks_count)

    def test_form_is_on_page(self):
        client = Client()
        client.force_login(self.user1)
        response = client.get(reverse('catalog:item_detail', args=[1]))
        self.assertContains(response, 'Ваша оценка:')

    def test_form_is_not_on_page(self):
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertNotContains(response, 'Ваша оценка:')

    def test_default_form_value(self):
        client = Client()
        client.force_login(self.user1)
        response = client.get(reverse('catalog:item_detail', args=[1]))
        form = response.context['mark_form']
        self.assertEqual(form['mark'].value(), None)
        rating.methods.add_mark(self.user1.id, self.item1.id, 4)
        response = client.get(reverse('catalog:item_detail', args=[1]))
        form = response.context['mark_form']
        self.assertEqual(form['mark'].value(), 4)

    def test_correct_middle_value(self):
        rating.methods.add_mark(self.user2.id, self.item1.id, 5)
        rating.methods.add_mark(self.user1.id, self.item1.id, 4)
        response = Client().get(reverse('catalog:item_detail', args=[1]))
        self.assertContains(response, 'Рейтинг: 4,5. (2 оценок)')
