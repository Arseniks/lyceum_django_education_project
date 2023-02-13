from django.http import HttpResponse


def home(request):
    return HttpResponse('<body>Главная</body>')


def teapot(request):
    return HttpResponse('<body>IM_A_TEAPOT</body>', status=418)
