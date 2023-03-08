from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def home(request):
    template = 'homepage/home.html'
    items = Item.objects.published().filter(is_on_main=True).order_by('name')
    context = {
        'items': items,
    }
    return render(request, template, context)


def teapot(request):
    return HttpResponse('<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT)
