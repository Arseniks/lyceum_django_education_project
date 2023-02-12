from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_catalog_item_list_endpoint(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_detail_endpoint(self):
        response_1 = Client().get('/catalog/1/')
        response_2 = Client().get('/catalog/-1/')
        response_3 = Client().get('/catalog/adf/')
        response_4 = Client().get('/catalog/1.8/')
        self.assertEqual(response_1.status_code, 200)
        self.assertNotEqual(response_2.status_code, 200)
        self.assertNotEqual(response_3.status_code, 200)
        self.assertNotEqual(response_4.status_code, 200)

    def test_catalog_re_endpoint(self):
        response_1 = Client().get('/catalog/re/1/')
        response_2 = Client().get('/catalog/re/-1/')
        response_3 = Client().get('/catalog/re/adf/')
        response_4 = Client().get('/catalog/re/1.8/')
        self.assertEqual(response_1.status_code, 200)
        self.assertNotEqual(response_2.status_code, 200)
        self.assertNotEqual(response_3.status_code, 200)
        self.assertNotEqual(response_4.status_code, 200)

    def test_catalog_converter_endpoint(self):
        response_1 = Client().get('/catalog/converter/1/')
        response_2 = Client().get('/catalog/converter/-1/')
        response_3 = Client().get('/catalog/converter/adf/')
        response_4 = Client().get('/catalog/converter/1.8/')
        self.assertEqual(response_1.status_code, 200)
        self.assertNotEqual(response_2.status_code, 200)
        self.assertNotEqual(response_3.status_code, 200)
        self.assertNotEqual(response_4.status_code, 200)
