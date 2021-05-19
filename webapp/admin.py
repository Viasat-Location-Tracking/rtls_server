from django.contrib import admin
from .models import DataPoint, Tag, ClinicItem

# Register your models here.
admin.site.register(DataPoint)
admin.site.register(Tag)
admin.site.register(ClinicItem)