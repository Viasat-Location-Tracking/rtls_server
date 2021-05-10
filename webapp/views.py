from django.http import HttpResponse
from django.shortcuts import render

from .models import DataPoint

def mainline(request):
    data_point_objects = DataPoint.objects.all()
    context = {
        "workstations": [
            "Workstation 1A",
            "Workstation 1B",
            "Workstation 2",
        ],
        "data_point_objects": data_point_objects,
        "move_transactions": [
            {
                "name": "Tag 1",
                "approve_link": "#",
                "deny_link": "#",
            },
            {
                "name": "Tag 2",
                "approve_link": "#",
                "deny_link": "#",
            },
            {
                "name": "Tag 3",
                "approve_link": "#",
                "deny_link": "#",
            },
        ],
        "metrics": {
            "daily_pace": "20%",
            "units_sent_to_clinic": 5,
            "yield": "80%",
        },
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