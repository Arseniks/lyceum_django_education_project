from django.test import Client
from django.test import TestCase
import parameterized


class StaticURLTests(TestCase):
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
