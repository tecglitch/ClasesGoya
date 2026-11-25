from django.urls import re_path

from .consumers import TaskNotificationConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/projects/(?P<project_id>\d+)/$",
        TaskNotificationConsumer.as_asgi(),
    ),
]
