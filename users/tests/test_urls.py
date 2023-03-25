from django.test import Client
from django.test import TestCase
from django.urls import reverse
import parameterized.parameterized


class StaticUrlsTests(TestCase):
    @parameterized.parameterized.expand(
        [
            ('login', 200),
            ('password_reset', 200),
            ('password_reset_complete', 200),
            ('password_reset_done', 200),
            ('signup', 200),
            ('logout', 302),
            ('password_change_done', 302),
        ]
    )
    def test_registration_endpoints(self, url, status):
        response = Client().get(reverse(f'users:{url}'))
        self.assertEqual(response.status_code, status)
