from django.http import HttpResponse
from django.test import Client
from django.test import override_settings
from django.test import TestCase
import parameterized

from middleware.reverse_middleware import ReverseEachTenWordMiddleware


class MiddlewareTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ('О проекте', 'О еткеорп'),
            ('Я чайник', 'Я кинйач'),
            ('Данила - лучший лектор', 'алинаД - йишчул роткел'),
            ('Ильнур, спасибо за ревью!', 'руньлИ, обисапс аз юьвер!'),
            ('Нfаfбfоfр бfуfкfв', 'Нfаfбfоfр бfуfкfв'),
            ('Hello, world!', 'Hello, world!'),
        ]
    )
    def test_reverse_russian_words_middleware(self, response, result):
        with override_settings(ACTIVATE_REVERSE_MIDDLEWARE=True):
            testing_middleware = ReverseEachTenWordMiddleware(HttpResponse)
            self.assertEqual(
                result, testing_middleware.reverse_russian_words(response)
            )

    @parameterized.parameterized.expand(
        [('Ж', True), ('/', False), ('G', False), ('Х', True)]
    )
    def test_is_russian_letter_middleware(self, letter, result):
        with override_settings(ACTIVATE_REVERSE_MIDDLEWARE=True):
            testing_middleware = ReverseEachTenWordMiddleware(HttpResponse)
            self.assertEqual(
                result, testing_middleware.is_russian_letter(letter)
            )

    def test_reverse_middleware(self):
        with override_settings(ACTIVATE_REVERSE_MIDDLEWARE=True):
            client = Client()
            response = ''
            for _ in range(10 + 1):
                response = client.get('/coffee')
            self.assertEqual(response.content.decode(), '<body>Я кинйач</body>')

    def test_middleware_disable(self):
        with override_settings(ACTIVATE_REVERSE_MIDDLEWARE=False):
            client = Client()
            for _ in range(10 + 1):
                response = client.get('/')
                self.assertEqual(
                    response.content.decode(), '<body>Главная</body>'
                )
