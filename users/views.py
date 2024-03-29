from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from users.forms import CustomCreationForm
from users.forms import CustomUserChangeForm
from users.forms import ProfileForm
from users.models import Person
from users.models import Profile


class UserListView(ListView):
    model = Person
    template_name = 'users/user_list.html'
    context_object_name = 'profiles'
    queryset = Profile.objects.activated


class UserDetailView(DetailView):
    model = Person
    template_name = 'users/user_detail.html'
    context_object_name = 'profile'
    get_queryset = Profile.objects.activated


class ActivateUserView(View):
    template_name = 'users/activate.html'

    def get(self, request, name):
        user = get_object_or_404(Person, username=name)
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
        return render(request, self.template_name)


class RecoveryUserView(View):
    template_name = 'users/recovery.html'

    def get(self, request, name):
        user = get_object_or_404(Person, username=name)
        if (
            user.profile.freezing_account_date is not None
            and user.profile.freezing_account_date
            > timezone.now() + timedelta(days=7)
            and not user.is_active
        ):
            user.delete()
            messages.error(
                request, 'Пользователь удален системой безопасности'
            )
        elif user.is_active is False:
            user.is_active = True
            user.profile.login_failed_count = 0
            user.profile.freezing_account_date = None
            user.profile.save()
            user.save()
            messages.success(request, 'Аккаунт восстановлен!')
        else:
            messages.success(request, 'Аккаунт не требует восстановления')

        return render(request, self.template_name)


class UserProfile(View):
    template_name = 'users/profile.html'

    def get(self, request):
        user = request.user
        form = CustomUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        user_profile = get_object_or_404(
            Profile.objects.activated(), pk=user.pk
        )
        context = {'form': (form, profile_form), 'profile': user_profile}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user

        form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=user.profile
        )

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('users:profile')

        context = {'form': (form, profile_form)}
        return render(request, self.template_name, context)


class Register(FormView):
    template_name = 'users/signup.html'
    form_class = CustomCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)

        user.is_active = settings.DEFAULT_USER_ACTIVITY
        user.save()
        user_profile = Profile(user=user, coffee_count=0)
        user_profile.save()

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
        return super().form_valid(form)
