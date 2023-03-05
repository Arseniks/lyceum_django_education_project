from django.test import Client
from django.test import TestCase
from django.urls import reverse


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
    def test_home_page_shown_correct_context(self):
        response = Client().get(reverse('homepage:home'))
        self.assertIn('items', response.context)
