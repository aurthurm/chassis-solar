from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse

from ..info.models import HomeInfo, About


class HomeInfoView(View):
    def get(self, *args, **kwargs):
        representation = {}
        home_info = HomeInfo.objects.first()
        representation['heading'] = home_info.heading
        representation['message'] = home_info.message
        representation['cat_heading'] = home_info.categories_heading
        representation['outro'] = home_info.outro
        return JsonResponse(representation)


class AboutUsView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about = About.objects.all().first()
        context['about'] = about
        return context