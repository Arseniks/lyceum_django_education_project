import datetime

import django.shortcuts
import django.test
import parameterized

from users import models


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
                '28.04.2023',
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
    def test_birthday_user(self, cookie_date, user_birth, result):
        date = user_birth
        self.profile.birthday = datetime.datetime.strptime(date, '%d.%m.%Y')
        self.profile.save()

        self.client.cookies.load({'django_date': cookie_date})
        response = self.client.get(
            django.shortcuts.reverse('homepage:home'), follow=True
        )
        self.assertEqual(result, response.context['births'].count())
