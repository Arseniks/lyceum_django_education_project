from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

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
        cls.profile1 = Profile.objects.create(user_id=1)
        cls.category = Category.objects.create(
            name='test_category', slug='cat1'
        )
        cls.item1 = Item.objects.create(
            id=1, name='item1', text='роскошно', category=cls.category
        )
        cls.item2 = Item.objects.create(
            id=2, name='item2', text='превосходно', category=cls.category
        )
        cls.item3 = Item.objects.create(
            id=3, name='item3', text='превосходно', category=cls.category
        )
        cls.item4 = Item.objects.create(
            id=4, name='item4', text='превосходно', category=cls.category
        )
        super().setUpTestData()

    def tearDown(self):
        Item.objects.all().delete()
        User.objects.all().delete()
        Mark.objects.all().delete()
        super().tearDown()

    def test_correct_middle_value(self):
        rating.methods.add_mark(self.user1.id, self.item1.id, 5)
        rating.methods.add_mark(self.user1.id, self.item3.id, 1)
        with freeze_time('2999-01-14'):
            rating.methods.add_mark(self.user1.id, self.item2.id, 5)
            rating.methods.add_mark(self.user1.id, self.item4.id, 1)
        response = Client().get(reverse('stats:user_stat_short', args=[1]))
        self.assertContains(response, '"<a href="/catalog/re/2/">item2</a>"')
        self.assertContains(response, 'любовь')
        self.assertContains(response, '"<a href="/catalog/re/4/">item4</a>"')
        self.assertContains(response, 'ненависть')
        self.assertContains(
            response,
            'За все время пользования нашим сайтом ' 'вы поставили 4 оценок.',
        )
        self.assertContains(response, 'Среднее значение ваших оценок: 3,0.')
