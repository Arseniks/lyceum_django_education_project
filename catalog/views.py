import datetime
import random

import django.db.models
from django.views.generic import DetailView
from django.views.generic import ListView

import catalog.models


class ItemListView(ListView):
    model = catalog.models.Item
    template_name = 'catalog/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return catalog.models.Item.objects.published().order_by(
            'category__name'
        )


class ItemDetailView(DetailView):
    model = catalog.models.Item
    template_name = 'catalog/item_detail.html'
    context_object_name = 'item'
    get_queryset = catalog.models.Item.objects.published


class FridayView(ListView):
    model = catalog.models.Item
    template_name = 'catalog/friday.html'
    context_object_name = 'items'

    def get_queryset(self):
        return (
            catalog.models.Item.objects.published()
            .filter(change_date__week_day=6)
            .order_by('-creation_date')[:5]
        )


class NoveltyView(ListView):
    model = catalog.models.Item
    template_name = 'catalog/novelty.html'
    context_object_name = 'items'

    def get_queryset(self):
        ids = (
            catalog.models.Item.objects.published()
            .filter(
                creation_date__range=[
                    django.utils.timezone.now() - datetime.timedelta(weeks=1),
                    django.utils.timezone.now(),
                ],
            )
            .values_list(catalog.models.Item.id.field.name, flat=True)
        )
        if ids:
            return catalog.models.Item.objects.published().filter(
                id__in=random.sample(list(ids), k=min(len(ids), 5)),
            )


class UntestedView(ListView):
    model = catalog.models.Item
    template_name = 'catalog/untested.html'
    context_object_name = 'items'

    def get_queryset(self):
        return catalog.models.Item.objects.filter(
            django.db.models.Q(
                creation_date__lt=django.db.models.F('change_date')
                + datetime.timedelta(seconds=1)
            )
            & django.db.models.Q(
                change_date__lt=django.db.models.F('creation_date')
                + datetime.timedelta(seconds=1)
            )
        )
