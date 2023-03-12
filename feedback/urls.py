from django.urls import path

from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback, name='feedback'),
    path(
        'successfully_sent', views.successfully_sent, name='successfully_sent'
    ),
]
