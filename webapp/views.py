from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from .models import DataPoint, Tag

import datetime
import json

# Mainline Page
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

# Clinic Page
def clinic(request):
    return render(request, 'webapp/clinic.html')

# Manager Page
def manager(request):
    return render(request, 'webapp/manager.html')

# Executive Page
def executive(request):
    return render(request, 'webapp/executive.html')

# IE/CI Page
def ie(request):
    return render(request, 'webapp/ie.html')

# Homepage (redirects to mainline)
def index(request):
    return redirect(reverse('webapp:mainline'))

# Returns JSON-formatted request_types and other data in response to AJAX requests
def data(request):
    # Determine which workstation we're talking about, if any
    workstation = request.GET['workstation'] if 'workstation' in request.GET else None

    # Determine what data we want to get
    request_type = request.GET['request_type'] if 'request_type' in request.GET else None

    # If no request_type provided, abort
    if request_type == None:
        return HttpResponseBadRequest("Missing 'request_type' parameter")

    # Workstation-related queries
    if workstation:
        # Units Present
        if request_type == "units_present":
            oldest_valid_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=settings.CURRENT_POSITION_LOOKBACK)
            units = DataPoint.objects.filter(
                timestamp__gte = oldest_valid_timestamp,    # find all datapoints with timestamp greater than or equal to the current time minus CURRENT_POSITION_LOOKBACK seconds
                zone__contains = [workstation]              # find the subset that are flagged with the workstation of interest (using list() to avoid syntax errors in Postgres)
            )

            units = add_serial_numbers(units, 'tag_id')

            return JsonResponse({'data': units})
    
    # Non-workstation-related queries
    else:
        # Map data
        if request_type == 'map_data':
            oldest_valid_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=settings.CURRENT_POSITION_LOOKBACK)
            data = DataPoint.objects.filter(
                timestamp__gte = oldest_valid_timestamp,
            ).order_by(
                "-timestamp" # put the most recent data on top
            )

            data = add_serial_numbers(data, 'tag_id', 'x_pos', 'y_pos', 'button_pushed')

            return JsonResponse({'data': data})

    # If nothing matched, abort
    return HttpResponseBadRequest("Invalid request")


# Helper function to match serial numbers and tags
def add_serial_numbers(units, *columns_to_keep):
    # Find the related serial number for each tag_id in the retrieved dataset. Must be current.
    serial_nums = []
    for unit in units:
        tag_assignment = Tag.objects.filter(
            valid_after__lte = unit.timestamp,
            valid_before__gte = unit.timestamp,
            tag_id = unit.tag_id
        )
        try:
            serial_nums.append(tag_assignment.first().serial_num)
        except AttributeError:
            # If the tag doesn't have a valid serial number match, insert a string that says so
            serial_nums.append('S/N not found')
            continue
    
    # Merge serial numbers into list of present units
    units = list(units.values(*columns_to_keep))
    for i in range(len(serial_nums)):
        units[i]['serial_num'] = serial_nums[i]

    return units