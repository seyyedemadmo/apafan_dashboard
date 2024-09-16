"""
ASGI config for Apafan_dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


from django.core.asgi import get_asgi_application

import web_socket.events.routing
from web_socket.middleware import UUIDAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Apafan_dashboard.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        UUIDAuthMiddleware(URLRouter(web_socket.events.routing.websocket_urlpatterns))
    ),
})
