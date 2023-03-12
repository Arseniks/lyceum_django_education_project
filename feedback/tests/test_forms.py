from django.test import Client
from django.test import TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_text_label(self):
        text_label = self.form.fields['text'].label
        self.assertEqual(text_label, 'Фидбэк')

    def test_mail_label(self):
        mail_label = self.form.fields['mail'].label
        self.assertEqual(mail_label, 'Почта')

    def test_text_help_text(self):
        mail_label = self.form.fields['mail'].help_text
        self.assertEqual(mail_label, 'Напишите отзыв о нашем сайте')

    def test_mail_help_text(self):
        mail_help_text = self.form.fields['mail'].help_text
        self.assertEqual(mail_help_text, 'Введите почту')

    def test_create_task(self):
        feedback_count = Feedback.objects.count()

        form_data = {
            'text': 'Тестовый отзыв',
            'mail': 'test.test@test.test',
        }

        response = Client().post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse('feedback:successfully_sent'))
        self.assertEqual(Feedback.objects.count(), feedback_count + 1)
        self.assertTrue(
            Feedback.objects.filter(
                text='Тестовый отзыв',
                mail='test.test@test.test',
            ).exists()
        )
