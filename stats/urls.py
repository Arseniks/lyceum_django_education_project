from django.urls import path

from stats import views

app_name = 'stats'

urlpatterns = [
    path('user_stat_short/', views.ShortUser.as_view(), name='short_user'),
    path('item_stat/<int:pk>/', views.ItemStats.as_view(), name='item_stat'),
]
