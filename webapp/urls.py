from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainline, name='index'),
    path('mainline', views.mainline, name='mainline'),
    path('clinic', views.clinic, name='clinic'),
    path('manager', views.manager, name='manager'),
    path('executive', views.executive, name='executive'),
    path('ie', views.ie, name='ie'),
]