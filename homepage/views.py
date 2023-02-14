from django.http import HttpResponse

from http import HTTPStatus


def home(request):
    return HttpResponse(f'<body>Главная</body>')


def teapot(request):
    return HttpResponse('<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT)
