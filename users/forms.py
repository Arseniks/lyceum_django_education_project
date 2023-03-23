from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Person
from users.models import Profile


def normalize_email(email):
    email = email or ''
    try:
        username, domain = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        username_no_tags = username.split('+')[0].lower()
        if domain.lower() in ['yandex.ru', 'ya.ru']:
            username_no_tags = username_no_tags.replace('.', '-')
            domain = 'yandex.ru'
        if domain.lower() == 'gmail.com':
            username_no_tags = username_no_tags.replace('.', '')
        email = '@'.join([username_no_tags, domain.lower()])
    return email


class CustomCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        is_email_unique = (
            Person.objects.filter(email=normalize_email(cleaned_data['email']))
            .exclude(pk=self.instance.id)
            .exists()
        )
        if is_email_unique:
            self.add_error(
                Person.email.field.name,
                'Пользователь с такой почтой уже существует',
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = normalize_email(self.cleaned_data['email'])
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    password = None

    def clean(self):
        cleaned_data = super().clean()
        is_email_unique = (
            Person.objects.filter(email=normalize_email(cleaned_data['email']))
            .exclude(pk=self.instance.id)
            .exists()
        )
        if is_email_unique:
            self.add_error(
                Person.email.field.name,
                'Пользователь с такой почтой уже существует',
            )

    class Meta(UserCreationForm.Meta):
        fields = (
            User.email.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (Profile.birthday.field.name, Profile.image.field.name)
