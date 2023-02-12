from django.urls import path, re_path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, 'positive_int')

urlpatterns = [
    path('', views.item_list),
    path('<int:number>/', views.item_detail),
    path('converter/<positive_int:positive_number>/', views.converter),
    re_path(r're/[0-9]+/$', views.re),
]
