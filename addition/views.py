from django.http import HttpResponse


def teapot(request):
    return HttpResponse('<body>Я чайник</body>', status=418)
