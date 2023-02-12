from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список элементов</body>')


def item_detail(request, number):
    return HttpResponse(f'<body> Подробно элемент {number}</body>')


def re(request):
    return HttpResponse('<body>Этот endpoint обработан с помощью регулярного выржения</body>')


def converter(request, positive_number):
    return HttpResponse(f'<body>Этот endpoint обработан с помощью пользовательского конвертора {positive_number}</body>')