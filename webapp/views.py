from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .models import DataPoint
from .models import Tag

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
            "daily_pace_percent": "85",
            "units_sent_to_clinic": 5,
            "yield": "80%",
        },
        "units_present": [
            {
                "serial": "00052",
                "tag_id": 1
            },
            {
                "serial": "00056",
                "tag_id": 14
            },
            {
                "serial": "00054",
                "tag_id": 33
            }
        ]
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

def tagAssign(request):
    tag_objects = Tag.objects.all()
    context_tag = {
        "tag_point_objects": tag_objects,
        "tags_hardcode" :[
            {
                "serial": "00052",
                "tag_id": 1
            },
            {
                "serial": "00056",
                "tag_id": 14
            },
            {
                "serial": "00054",
                "tag_id": 33
            }
        ]
    }
    return render(request, 'webapp/tagAssign.html', context_tag)

def insert_tagAssign(request):
    content = request.POST['tagID_TB', 'SN_TB', 'time_TB']
    newTag = Tag(content)
    newTag.save()
    return redirect('/tagAssign.html')
    #return render(request, 'webapp/manager.html')

def index(request):
    return redirect('/mainline')