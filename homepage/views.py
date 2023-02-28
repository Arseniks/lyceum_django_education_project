from datetime import datetime
from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = 'homepage/home.html'
    context = {'date': datetime.now().strftime('%Y %m %d %H:%M')}
    return render(request, template, context)


def teapot(request):
    return HttpResponse('<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT)
