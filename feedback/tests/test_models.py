from django.test import TestCase

from feedback.models import Feedback


class ModelTests(TestCase):
    def test_feedback_model(self):
        feedback_count = Feedback.objects.count()

        user_feedback = Feedback(
            text='test',
            mail='test.test@test.test',
        )
        user_feedback.full_clean()
        user_feedback.save()

        self.assertEqual(Feedback.objects.count(), feedback_count + 1)
