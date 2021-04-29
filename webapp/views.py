from django.http import HttpResponse
from django.shortcuts import render

from .models import DataPoint

def mainline(request):
    context = {
        # Hash table of variables to be passed to the template renderer, e.g.:
        'username': 'demouser',
        'mood': 'pretty good',
        'is_button_pushed': True,
    }
    return render(request, 'webapp/mainline.html', context)

def clinic(request):
    return render(request, 'webapp/clinic.html')

def manager(request):
    return render(request, 'webapp/manager.html')

def executive(request):
    return render(request, 'webapp/executive.html')

def ie(request):
    return render(request, 'webapp/ie.html')