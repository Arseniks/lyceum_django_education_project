import datetime

import django.shortcuts
import django.test
import parameterized

from users import models

import mock


class ContextTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = models.User.objects.create_user(
            username='test_user',
            password='tang0_mang0',
            email='nota@yahoo.com',
        )
        cls.profile = models.Profile.objects.create(user_id=cls.user.id)

    @parameterized.parameterized.expand(
        [
            (
                '29.04.2023',
                '29.04.2023',
                1,
            ),
            (
                '29.04.2023',
                '30.04.2023',
                0,
            ),
            (
                '29.04.2002',
                '29.04.2023',
                1,
            ),
            (
                '29.03.2002',
                '29.04.2023',
                0,
            ),
            (
                '30.03.2002',
                '29.04.2023',
                0,
            ),
        ]
    )
    @mock.patch('django.utils.timezone.now')
    def test_birthday_user(self, user_birth, server_date, result, mock_date):
        mock_date.return_value = datetime.datetime.strptime(server_date, '%d.%m.%Y')
        date = user_birth
        self.profile.birthday = datetime.datetime.strptime(date, '%d.%m.%Y')
        self.profile.save()

        response = self.client.get(
            django.shortcuts.reverse('homepage:home'), follow=True
        )
        self.assertEqual(result, response.context['births'].count())
