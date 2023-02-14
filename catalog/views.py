from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список элементов</body>')


def item_detail(request, number=1):
    return HttpResponse(f'<body> Подробно элемент {number}</body>')
