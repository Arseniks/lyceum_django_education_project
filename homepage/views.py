from http import HTTPStatus

from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView

import catalog.models


class HomeView(ListView):
    template_name = 'homepage/home.html'
    context_object_name = 'items'

    def get_queryset(self):
        return (
            catalog.models.Item.objects.published()
            .filter(is_on_main=True)
            .order_by('name')
        )


class TeapotView(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.profile.coffee_count += 1
            request.user.profile.save()
        return HttpResponse(
            '<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT
        )
