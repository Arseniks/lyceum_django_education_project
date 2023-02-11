from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_catalog_item_list_endpoint(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_detail_endpoint(self):
        response = Client().get('/catalog/1/')
        self.assertEqual(response.status_code, 200)
