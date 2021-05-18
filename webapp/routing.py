from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/map/', consumers.MapConsumer.as_asgi())
]