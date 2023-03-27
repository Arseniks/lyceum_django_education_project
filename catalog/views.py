import datetime
import random

import django.db.models
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView

import catalog.models
import rating.forms
import rating.methods


class ItemDetailView(DetailView):
    model = catalog.models.Item
    template_name = 'catalog/item_detail.html'
    context_object_name = 'item'
    get_queryset = catalog.models.Item.objects.published

    def get(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        mark_form = rating.forms.MarkForm()
        mark_form.fields[
            'mark'
        ].initial = rating.methods.get_initial_form_value(request.user.id, pk)
        context = self.get_context_data()
        context['mark_form'] = mark_form
        marks_data = rating.methods.get_marks_statistic(pk)
        context['rating'] = marks_data[1]
        context['count_marks'] = marks_data[0]
        return self.render_to_response(context)

    def post(self, request, pk, *args, **kwargs):
        mark_form = rating.forms.MarkForm(request.POST or None)
        if mark_form.is_valid() and request.user.is_authenticated:
            mark = mark_form.cleaned_data['mark']
            rating.methods.add_mark(request.user.id, pk, mark)
        return redirect('catalog:item_detail', pk)


class ItemListView(ListView):
    model = catalog.models.Item
    template_name = 'catalog/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return catalog.models.Item.objects.published().order_by(
            'category__name'
        )


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
