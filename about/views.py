from django.shortcuts import render
from django.views.generic import TemplateView


class DescriptionView(TemplateView):
    template_name = 'about/description.html'
