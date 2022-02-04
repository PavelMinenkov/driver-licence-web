"""
ASGI config for xxx project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.urls import re_path
from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from asgi_middleware_static_file import ASGIMiddlewareStaticFile

from main.consumers import QRNotifications


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')

django_asgi_app = get_asgi_application()
django_asgi_app = ASGIMiddlewareStaticFile(
  django_asgi_app, static_url=settings.STATIC_URL,
  static_root_paths=[settings.STATIC_ROOT]
)

application = ProtocolTypeRouter({

    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket handler
    "websocket": URLRouter([
        re_path("^qr/(?P<connection_key>\w+)$", QRNotifications.as_asgi()),
    ])
})
