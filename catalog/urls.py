from django.urls import path
from django.urls import re_path
from django.urls import register_converter

from . import converters
from . import views

app_name = 'catalog'

register_converter(converters.PositiveDigitConverter, 'positive_int')

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('friday', views.FridayView.as_view(), name='friday'),
    path('novelty', views.NoveltyView.as_view(), name='novelty'),
    path('untested', views.UntestedView.as_view(), name='untested'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path(
        'converter/<positive_int:pk>/',
        views.ItemDetailView.as_view(),
        name='item_detail',
    ),
    re_path(
        r'^re/(?P<pk>[1-9][0-9]*)/$',
        views.ItemDetailView.as_view(),
        name='item_detail',
    ),
]
