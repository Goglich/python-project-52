from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse

class HomePageView(TemplateView):

    def get(self, request):
        return render(request, 'index.html')
    

def index(request):
    a = None
    a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")