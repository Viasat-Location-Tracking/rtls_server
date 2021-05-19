from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mainline', views.mainline, name='mainline'),
    path('clinic', views.clinic, name='clinic'),
    path('manager', views.manager, name='manager'),
    path('executive', views.executive, name='executive'),
    path('ie', views.ie, name='ie'),
<<<<<<< HEAD
    path('tagAssign', views.tagAssign, name='tagAssign'),
    path('insert_tagAssign', views.insert_tagAssign, name='tagAssign')
=======
    path('data', views.data, name='data') # used for returning metrics and other data via AJAX requests on the browser side
>>>>>>> 55748d2eb1e4eb962cb52f649531a83fefa4956a
]