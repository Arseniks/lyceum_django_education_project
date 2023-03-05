from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


def home(request):
    template = 'homepage/home.html'
    items = catalog.models.Item.objects.published()
    context = {
        'items': items,
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse('<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT)
