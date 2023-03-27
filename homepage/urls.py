from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('coffee/', views.TeapotView.as_view(), name='coffee'),
]
