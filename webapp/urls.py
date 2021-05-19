from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mainline', views.mainline, name='mainline'),
    path('clinic', views.clinic, name='clinic'),
    path('manager', views.manager, name='manager'),
    path('executive', views.executive, name='executive'),
    path('ie', views.ie, name='ie'),
    path('tagAssign', views.tagAssign, name='tagAssign'),
    path('insert_tagAssign', views.insert_tagAssign, name='tagAssign')
]