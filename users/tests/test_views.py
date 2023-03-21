import datetime

from django.contrib.auth.models import User
from django.core import exceptions
from django.test import Client
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import mock
import pytz


class ViewsTests(TestCase):
    user_register_data = {
        'username': 'TestUsername',
        'email': 'test@test.test',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    }

    def test_user_signup_context(self):
        response = Client().get(
            reverse(
                'users:signup',
            )
        )
        self.assertIn('form', response.context)

    def test_user_signup_success_redirect(self):
        response = Client().post(
            reverse('users:signup'),
            self.user_register_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('users:login'))

    def test_user_signup_success(self):
        user_count = User.objects.count()

        Client().post(
            reverse('users:signup'),
            self.user_register_data,
            follow=True,
        )

        self.assertEqual(User.objects.count(), user_count + 1)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    def test_signup_is_active_false(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data['username'])

        self.assertFalse(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='True')
    def test_signup_is_active_true(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data['username'])

        self.assertTrue(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    def test_user_activate_user_success(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data['username'])

        Client().get(
            reverse('users:activate_user', args=(user.username,)),
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data['username'])

        self.assertTrue(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    @mock.patch('django.utils.timezone.now')
    def test_user_activate_user_error(self, mock_now):
        Client().post(
            reverse('users:signup'),
            self.user_register_data,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data['username'])

        utc = pytz.UTC
        mock_now.return_value = utc.localize(
            timezone.datetime.now() + datetime.timedelta(hours=12)
        )

        Client().get(
            reverse('users:activate_user', args=(user.username,)),
            follow=True,
        )

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            User.objects.get(username=self.user_register_data['username'])
