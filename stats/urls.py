from django.urls import path

from stats import views

app_name = 'stats'

urlpatterns = [
    path(
        'user_stat_short/<int:pk>',
        views.ShortUserStatsView.as_view(),
        name='user_stat_short',
    ),
]
