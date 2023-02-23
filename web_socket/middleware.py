from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


class UUIDAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, a, b):
        headers = dict(scope['headers'])
        if b'AUTH-UUID' in headers:
            try:
                uuid = headers[b'AUTH-UUID']
                if uuid:
                    user = get_user_model().objects.get(uuid=str(uuid))
                    scope['user'] = user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        return self.inner(scope)


UUIDAuthMiddlewareStack = lambda inner: UUIDAuthMiddleware(AuthMiddlewareStack(inner))
