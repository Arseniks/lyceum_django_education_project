from datetime import datetime

from django.shortcuts import render


def item_list(request):
    template = 'catalog/item_list.html'
    context = {'date': datetime.now().strftime("%Y %m %d %H:%M")}
    return render(request, template, context)


def item_detail(request, number):
    template = 'catalog/item_detail.html'
    context = {'date': datetime.now().strftime("%Y %m %d %H:%M")}
    return render(request, template, context)
