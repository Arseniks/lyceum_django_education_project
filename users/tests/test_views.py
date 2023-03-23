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
    user_register_data_1 = {
        'username': 'TestUsername1',
        'email': 'test@test.test',
        'password1': 'testpassword1231',
        'password2': 'testpassword1231',
    }
    user_register_data_2 = {
        'username': 'TestUsername2',
        'email': 'test@test.test',
        'password1': 'testpassword1232',
        'password2': 'testpassword1232',
    }
    user_login_data = {
        'username': 'TestUsername',
        'password': 'testpassword123',
    }
    user_login_by_mail_data = {
        'email': 'test@test.test',
        'password': 'testpassword123',
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
            self.user_register_data_1,
            follow=True,
        )

        self.assertRedirects(response, reverse('users:login'))

    def test_user_signup_success(self):
        user_count = User.objects.count()

        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        self.assertEqual(User.objects.count(), user_count + 1)

    def test_users_signup_with_same_mails_negative(self):
        user_count = User.objects.count()
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )
        response = Client().post(
            reverse('users:signup'),
            self.user_register_data_2,
            follow=True,
        )
        self.assertFormError(
            response,
            'form',
            'email',
            'Пользователь с такой почтой уже существует',
        )
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_user_login_success(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )
        response = Client().post(
            reverse('users:login'),
            self.user_login_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_login_by_mail_success(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )
        response = Client().post(
            reverse('users:login'),
            self.user_login_by_mail_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    def test_signup_is_active_false(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data_1['username'])

        self.assertFalse(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='True')
    def test_signup_is_active_true(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data_1['username'])

        self.assertTrue(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    def test_user_activate_user_success(self):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data_1['username'])

        Client().get(
            reverse('users:activate_user', args=(user.username,)),
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data_1['username'])

        self.assertTrue(user.is_active)

    @override_settings(DEFAULT_USER_ACTIVITY='False')
    @mock.patch('django.utils.timezone.now')
    def test_user_activate_user_error(self, mock_now):
        Client().post(
            reverse('users:signup'),
            self.user_register_data_1,
            follow=True,
        )

        user = User.objects.get(username=self.user_register_data_1['username'])

        utc = pytz.UTC
        mock_now.return_value = utc.localize(
            timezone.datetime.now() + datetime.timedelta(hours=12)
        )

        Client().get(
            reverse('users:activate_user', args=(user.username,)),
            follow=True,
        )

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            User.objects.get(username=self.user_register_data_1['username'])
