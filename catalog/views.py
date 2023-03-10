import datetime
import random

import django.db.models
from django.shortcuts import get_object_or_404
from django.shortcuts import render

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
    item = get_object_or_404(
        catalog.models.Item.objects.published(), id=number
    )
    gallery = catalog.models.ImageGallery.objects.filter(item=item)
    context = {'item': item, 'gallery': gallery}
    return render(request, template, context)


def friday(request):
    template = 'catalog/friday.html'
    ids = catalog.models.Item.objects.published().values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    items = None
    if ids:
        items = catalog.models.Item.objects.filter(
            change_date__week_day=6,
            id__in=list(ids)[-6:-1],
        )
    print(items)
    context = {
        'items': items,
    }
    return render(request, template, context)


def novelty(request):
    template = 'catalog/novelty.html'
    ids = catalog.models.Item.objects.values_list(
        catalog.models.Item.id.field.name, flat=True
    )
    items = None
    if ids:
        items = (
            catalog.models.Item.objects.published().filter(
                id__in=random.sample(list(ids), k=min(len(ids), 5)),
                creation_date__range=[
                    django.utils.timezone.now() - datetime.timedelta(weeks=1),
                    django.utils.timezone.now(),
                ],
            )
        ).order_by('?')
    context = {
        'items': items,
    }
    return render(request, template, context)


def untested(request):
    template = 'catalog/untested.html'
    items = catalog.models.Item.objects.filter(
        creation_date=django.db.models.F(
            catalog.models.Item.change_date.field.name
        )
    )
    context = {
        'items': items,
    }
    return render(request, template, context)
