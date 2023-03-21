from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
import users
from users.models import Profile


def home(request):
    template = 'homepage/home.html'
    items = (
        catalog.models.Item.objects.published()
        .filter(is_on_main=True)
        .order_by('name')
    )
    context = {
        'items': items,
    }
    return render(request, template, context)


def teapot(request):
    user_profiles = users.models.Profile.objects.activated()
    if user_profiles:
        user_profile = user_profiles.filter(user__pk=request.user.pk)
        user_profiles[0].coffee_count += 1
        user_profiles[0].save()
    return HttpResponse('<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT)
