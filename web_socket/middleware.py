from channels.auth import BaseMiddleware
from channels.db import database_sync_to_async

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user(scope):
    headers = dict(scope['headers'])
    if b'auth-uuid' in headers:
        try:
            uuid = headers[b'auth-uuid'].decode('utf-8')
            if uuid:
                user = get_user_model().objects.get(uuid=str(uuid))
                return user
        except Exception as e:
            return AnonymousUser()
    else:
        return AnonymousUser()


class UUIDAuthMiddleware(BaseMiddleware):
    """
    Token authorization middleware for Django Channels 2
    """

    async def __call__(self, scope, receive, send):
        scope['user'] = await get_user(scope)
        return await super(UUIDAuthMiddleware, self).__call__(scope, receive, send)
