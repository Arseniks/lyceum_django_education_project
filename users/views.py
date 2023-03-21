from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View

import users
from users.forms import CustomCreationForm
from users.forms import CustomUserChangeForm
from users.forms import ProfileForm
from users.models import Profile


def user_list(request):
    template = 'users/user_list.html'
    all_users = users.models.Profile.objects.activated()
    context = {
        'users': all_users,
    }
    return render(request, template, context)


def user_detail(request, pk):
    template = 'users/user_detail.html'
    user = users.models.Profile.objects.activated().filter(pk=pk)[0]
    context = {
        'user': user,
    }
    return render(request, template, context)


def activate_user(request, name):
    template = 'users/activate.html'

    user = get_object_or_404(User, username=name)
    if (
        user.date_joined < timezone.now() - timedelta(hours=12)
        and not user.is_active
    ):
        user.delete()
        messages.error(request, 'Активация аккаунта недействительна')
    elif user.is_active is False:
        user.is_active = True
        user.save()
        messages.success(request, 'Аккаунт активирован!')
    else:
        messages.success(request, 'Аккаунт уже был активирован ранее')

    return render(request, template)


def profile(request):
    template = 'users/profile.html'
    form = CustomUserChangeForm
    profile_form = ProfileForm
    context = {'form': form, 'profile_form': profile_form}
    return render(request, template, context)


class Register(View):
    template_name = 'users/signup.html'

    def get(self, request):
        context = {'form': CustomCreationForm}
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomCreationForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = settings.DEFAULT_USER_ACTIVITY
            user.save()
            profile = Profile(user=user, coffee_count=0)
            profile.save()

            if not settings.DEFAULT_USER_ACTIVITY:
                send_mail(
                    'Письмо верификации аккаунта',
                    'Ваша почта была зарегистрирована на сайте KittyShop!\n'
                    'Для подтверждение регистрации перейдите по ссылке: '
                    'http://127.0.0.1:8000/auth/activate/'
                    f'{form.cleaned_data["username"]}',
                    settings.FEEDBACK_MAIL,
                    [f'{form.cleaned_data["email"]}'],
                    fail_silently=False,
                )
            return redirect('users:login')
        context = {'form': form}
        return render(request, self.template_name, context)
