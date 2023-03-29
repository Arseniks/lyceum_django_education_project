from django.urls import path

from stats import views

app_name = 'stats'

urlpatterns = [
    path('user_stat_short/', views.ShortUser.as_view(), name='short_user'),
]
