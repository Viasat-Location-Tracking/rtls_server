from django.http import HttpResponse
from django.shortcuts import render

from .models import DataPoint

def index(request):
    context = {
        # Hash table of variables to be passed to the template renderer, e.g.:
        'username': 'demouser',
        'mood': 'pretty good',
        'is_button_pushed': True,
    }
    return render(request, 'webapp/index.html', context)