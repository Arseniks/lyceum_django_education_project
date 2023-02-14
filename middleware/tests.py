from django.http import HttpResponse
from django.test import Client, TestCase

from middleware.reverse_middleware import ReverseEachTenWordMiddleware

import parameterized


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
    def test_reverse_middleware(self, response, result):
        testing_middleware = ReverseEachTenWordMiddleware(HttpResponse)
        self.assertEqual(
            result, testing_middleware.reverse_russian_words(response)
        )

    def test_middleware_disable(self):
        testing_middleware = ReverseEachTenWordMiddleware(HttpResponse)
        testing_middleware.activate_middleware = False

        client = Client()

        for _ in range(10):
            response = client.get('/')
            print(response.content.decode())
            self.assertEqual(response.content.decode(), '<body>Главная</body>')
