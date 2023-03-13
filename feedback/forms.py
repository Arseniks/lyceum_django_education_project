from django import forms

from feedback.models import Feedback, FeedbackFiles, FeedbackText


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            Feedback.mail.field.name,
        )


class FeedbackTextForm(forms.ModelForm):
    class Meta:
        model = FeedbackText
        fields = (
            FeedbackText.text.field.name,
        )


class FeedbackFilesForm(forms.ModelForm):
    class Meta:
        model = FeedbackFiles
        widgets = {FeedbackFiles.files.field.name: forms.ClearableFileInput(attrs={'multiple': True})}
        fields = (
            FeedbackFiles.files.field.name,
        )
