import django.contrib.auth.views
import django.urls

import users.views

app_name = 'users'

urlpatterns = [
    django.urls.path(
        'login/',
        django.contrib.auth.views.LoginView.as_view(
            template_name='users/login.html'
        ),
        name='login',
    ),
    django.urls.path(
        'logout/',
        django.contrib.auth.views.LogoutView.as_view(
            template_name='users/logout.html',
        ),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done/',
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset/',
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    django.urls.path(
        'reset/<uidb64>/<token>/',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'reset/done/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    django.urls.path(
        'user_list/', users.views.UserListView.as_view(), name='user_list'
    ),
    django.urls.re_path(
        r'user_detail/(?P<pk>[1-9]\d*)/$',
        users.views.UserDetailView.as_view(),
        name='user_detail',
    ),
    django.urls.path(
        'signup/',
        users.views.Register.as_view(
            template_name='users/signup.html',
        ),
        name='signup',
    ),
    django.urls.re_path(
        r'activate/(?P<name>[\da-zA-Z+_@.-]*)/$',
        users.views.ActivateUserView.as_view(),
        name='activate_user',
    ),
    django.urls.re_path(
        r'recovery/(?P<name>[\da-zA-Z+_@.-]*)/$',
        users.views.RecoveryUserView.as_view(),
        name='recovery_user',
    ),
    django.urls.path(
        'profile/',
        users.views.UserProfile.as_view(
            template_name='users/profile.html',
        ),
        name='profile',
    ),
]
