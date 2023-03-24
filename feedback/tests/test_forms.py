from django.test import Client
from django.test import TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.forms import FeedbackTextForm


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()
        cls.text_form = FeedbackTextForm()

    def test_feedback_text_label(self):
        text_label = self.text_form.fields['text'].label
        self.assertEqual(text_label, 'Фидбек')

    def test_feedback_mail_label(self):
        mail_label = self.form.fields['mail'].label
        self.assertEqual(mail_label, 'Почта')

    def test_feedback_text_help_text(self):
        mail_label = self.text_form.fields['text'].help_text
        self.assertEqual(mail_label, 'Напишите отзыв о нашем сайте')

    def test_feedback_mail_help_text(self):
        mail_help_text = self.form.fields['mail'].help_text
        self.assertEqual(mail_help_text, 'Введите почту')

    def test_feedback_create_task(self):
        form_data = {
            'mail': 'test.test@test.test',
        }

        response = Client().post(
            reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )

        self.assertIn('feedback_form', response.context)
        self.assertIn('feedback_text_form', response.context)
        self.assertIn('feedback_file_form', response.context)
