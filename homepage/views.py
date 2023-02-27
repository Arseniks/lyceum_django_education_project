from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    template = 'homepage/home.html'
    context = {}
    return render(request, template, context)


def teapot(request):
    template = 'homepage/coffee.html'
    context = {}
    return render(request, template, context)
