import datetime
import random

import django.db.models
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

import catalog.models

import rating.forms
import rating.methods


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
    mark_form = rating.forms.MarkForm(request.POST or None)
    if mark_form.is_valid() and request.user.is_authenticated:
        mark = mark_form.cleaned_data['mark']
        rating.methods.add_mark(request.user.id, number, mark)
        return redirect('catalog:item_detail', number)
    mark_form.fields['mark'].initial = \
        rating.methods.get_initial_form_value(request.user.id, number)
    marks_data = rating.methods.get_marks_statistic(number)
    context = {
        'item': item,
        'gallery': gallery,
        'mark_form': mark_form,
        'rating': marks_data[1],
        'count_marks': marks_data[0]
        }
    return render(request, template, context)


def friday(request):
    template = 'catalog/friday.html'
    items = (
        catalog.models.Item.objects.published()
        .filter(change_date__week_day=6)
        .order_by('-creation_date')[:5]
    )
    context = {
        'items': items,
    }
    return render(request, template, context)


def novelty(request):
    template = 'catalog/novelty.html'
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
    items = None
    if ids:
        items = catalog.models.Item.objects.published().filter(
            id__in=random.sample(list(ids), k=min(len(ids), 5)),
        )
    context = {
        'items': items,
    }
    return render(request, template, context)


def untested(request):
    template = 'catalog/untested.html'
    items = catalog.models.Item.objects.filter(
        django.db.models.Q(
            creation_date__lt=django.db.models.F('change_date')
            + datetime.timedelta(seconds=1)
        )
        & django.db.models.Q(
            change_date__lt=django.db.models.F('creation_date')
            + datetime.timedelta(seconds=1)
        )
    )
    context = {
        'items': items,
    }
    return render(request, template, context)
