from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_about_description_endpoint(self):
        response = Client().get('/about/')
        self.assertEqual(response.status_code, 200)
