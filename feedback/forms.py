from django import forms
from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            Feedback.text.field.name,
            Feedback.mail.field.name,
        )
