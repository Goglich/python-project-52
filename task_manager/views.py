from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):

    def get(self, request):
        return render(request, 'index.html')