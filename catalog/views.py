import django.db.models
from django.shortcuts import render, get_object_or_404

import catalog.models


def item_list(request):
    template = 'catalog/item_list.html'
    items = catalog.models.Item.objects.published().order_by('category__name')
    context = {
        'items': items,
    }
    return render(request, template, context)


def item_detail(request, number):
    template = 'catalog/item_detail.html'
    item = get_object_or_404(catalog.models.Item.objects.published(), id=number)
    gallery = catalog.models.ImageGallery.objects.filter(item=item)
    context = {
        'item': item,
        'gallery': gallery
    }
    return render(request, template, context)
