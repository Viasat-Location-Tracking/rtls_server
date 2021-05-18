from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mainline', views.mainline, name='mainline'),
    path('clinic', views.clinic, name='clinic'),
    path('manager', views.manager, name='manager'),
    path('executive', views.executive, name='executive'),
    path('ie', views.ie, name='ie'),
    path('data', views.data, name='data') # used for returning metrics and other data via AJAX requests on the browser side
]