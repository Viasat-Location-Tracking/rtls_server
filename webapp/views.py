from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.forms.models import model_to_dict

from .models import DataPoint, Tag, ClinicItem

import datetime

# Mainline Page
def mainline(request):
    context = {
        "workstations": [
            "Workstation 1A",
            "Workstation 1B",
            "Workstation 2",
            "Rework",
        ],
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
            "units_sent_to_clinic": '',
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

# Homepage
def index(request):
    return redirect(reverse('webapp:mainline'))

# Clinic Page
def clinic(request):
    context = {
        "clinic_items": [],
    }
    clinic_items = ClinicItem.objects.all()
    for item in clinic_items:
       context["clinic_items"].append(item)
        
    return render(request, 'webapp/clinic.html', context)

# Manager Page
def manager(request):
    return render(request, 'webapp/manager.html')

# Executive Page
def executive(request):
    context = {
        "metrics": {
            "avg_time_prob_solution": "8.2 hrs",
            "prob_freq": "2%",
            "on_time_delivery": "85%",
            "perc_on_takt" : "71%"
        }
    }
    return render(request, 'webapp/executive.html', context)

# IE/CI Page
def ie(request):
    context = {
        "metrics": {
            "daily_pace_percent": "85",
            "units_sent_to_clinic": 5,
            "yield": "80%",
            "on_time_delivery": "85%",
            "perc_on_takt" : "71%"
        }
    }
    return render(request, 'webapp/ie.html', context)

# Tag Assignment Page
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

# Tag Assignment Updater
def insert_tagAssign(request):
    newTag = Tag(tag_id = request.POST['tagID_TB'], tag_name = request.POST['tagName_TB'], serial_num = request.POST['SN_TB'], valid_after = request.POST['time_TB'])
    #content = request.POST['tagID_TB', 'SN_TB', 'time_TB']
    #newTag = Tag(content)
    newTag.save()
    return redirect('/tagAssign')
    #return render(request, 'webapp/manager.html')

# Clinic Table Updater
def update_clinic_table(request):
    operation = request.POST['operation'] if request.POST['operation'] else None

    if operation == None:
        return HttpResponseBadRequest("Missing 'operation' parameter")

    if operation == "add":
        try:
            serial_num = request.POST['serial_num']
            from_zone = request.POST['workstation']
            problem = request.POST['problem']
        except AttributeError:
            return HttpResponseBadRequest("Missing parameter")

        # Get tag id corresponding with submitted serial number (works similarly to add_serial_numbers() below)
        try:
            tag_id = Tag.objects.filter(
                valid_after__lte = datetime.datetime.now(),
                #valid_before__gte = datetime.datetime.now(), # Commented out for demo because the query returns nothing when valid_before is null.
                serial_num = serial_num,
            ).first().tag_id
        except AttributeError:
            return HttpResponseServerError("No tag assigned to serial number %s" % serial_num)

        # Create new table row
        clinic_item = ClinicItem(
            tag_id = tag_id,
            serial_num = serial_num,
            added_to_clinic = datetime.datetime.now(),
            from_zone = [from_zone], # from_zone in models.py is an ArrayField, so we have to pass an array
            problem = problem,
        )
        clinic_item.save()
    
    return JsonResponse({
        'data': {
            'message': 'Serial number %s successfully added to clinic.' % clinic_item.serial_num,
        }
    })

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

        # Units sent to clinic from workstation in past x hours
        if request_type == "units_sent_to_clinic":
            hours_ago = request.GET['hours_ago']
            oldest_valid_timestamp = datetime.datetime.now() - datetime.timedelta(hours=int(hours_ago))
            units = ClinicItem.objects.filter(
                from_zone__contains = [workstation],
                added_to_clinic__gte = oldest_valid_timestamp
            )

            return JsonResponse({'data': len(units.values())})
    
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
            #valid_after__lte = unit.timestamp,
            #valid_before__gte = unit.timestamp,
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
