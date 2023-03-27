from django.urls import path
from django.urls import re_path
from django.urls import register_converter

from . import converters
from . import views

app_name = 'catalog'

register_converter(converters.PositiveDigitConverter, 'positive_int')

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('friday', views.friday, name='friday'),
    path('novelty', views.novelty, name='novelty'),
    path('untested', views.untested, name='untested'),
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
