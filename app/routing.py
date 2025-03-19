# your_app/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/login/', consumers.LoginConsumer.as_asgi()),
]
