from datetime import datetime

from django.shortcuts import render


def description(request):
    template = 'about/description.html'
    context = {'date': datetime.now().strftime("%Y %m %d %H:%M")}
    return render(request, template, context)
