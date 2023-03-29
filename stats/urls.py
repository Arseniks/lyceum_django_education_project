from django.urls import path

from stats import views

app_name = 'stats'

urlpatterns = [
    path(
        'user_rated_items_list/<int:pk>/',
        views.UserRatedItemsList.as_view(),
        name='user_rated_items_list',
    ),
    path('item_stat/<int:pk>/', views.ItemStats.as_view(), name='item_stat'),
    path(
        'user_stat_short/<int:pk>/',
        views.ShortUserStatsView.as_view(),
        name='user_stat_short',
    ),
]
