from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q

from users.models import Person
from users.models import Profile


class CustomCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        is_email_unique = Person.objects.filter(
            ~Q(pk=self.instance.id), email=cleaned_data['email']
        ).exists()
        if is_email_unique:
            self.add_error(
                Person.email.field.name,
                'Пользователь с такой почтой уже существует',
            )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    password = None

    def clean(self):
        cleaned_data = super().clean()
        is_email_unique = Person.objects.filter(
            ~Q(pk=self.instance.id), email=cleaned_data['email']
        ).exists()
        if is_email_unique:
            self.add_error(
                Person.email.field.name,
                'Пользователь с такой почтой уже существует',
            )

    class Meta:
        model = User
        fields = (
            User.email.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (Profile.birthday.field.name, Profile.image.field.name)
