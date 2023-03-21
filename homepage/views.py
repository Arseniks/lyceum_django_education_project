from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
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
    user_profiles = Profile.objects.activated()
    if user_profiles:
        user_profile = user_profiles.filter(user__pk=request.user.pk)
        user_profile.coffee_count += 1
        user_profile.save()
    return HttpResponse('<body>Я чайник</body>', status=HTTPStatus.IM_A_TEAPOT)
