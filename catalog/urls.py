from . import converters, views
from django.urls import path, re_path, register_converter


register_converter(converters.PositiveDigitConverter, 'positive_int')

urlpatterns = [
    path('', views.item_list),
    path('<int:number>/', views.item_detail),
    path('converter/<positive_int:number>/', views.item_detail),
    re_path(r'^re/(?P<number>[1-9][0-9]*)/$', views.item_detail),
]
