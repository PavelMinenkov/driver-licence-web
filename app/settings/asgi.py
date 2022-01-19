"""
ASGI config for xxx project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from websockets.consumers import QRNotifications


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({

    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket handler
    "websocket": URLRouter([
        re_path("^qr-notification$", QRNotifications.as_asgi()),
    ])
})
