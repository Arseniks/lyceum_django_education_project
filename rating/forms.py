from django import forms

from rating.models import Mark


class MarkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
            field.field.required = False

    class Meta:
        model = Mark
        fields = (Mark.mark.field.name,)
        labels = {Mark.mark.field.name: 'Ваша оценка:'}
        help_texts = {Mark.mark.field.name: 'Оцените товар'}
