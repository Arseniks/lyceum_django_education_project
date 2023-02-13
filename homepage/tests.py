from django.test import TestCase, Client


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
            response.content.decode('utf-8'), '<body>IM_A_TEAPOT</body>')