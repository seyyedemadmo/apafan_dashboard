from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication

from django.contrib.auth import get_user_model

from datetime import datetime


class CustomAuthentication(SessionAuthentication):
    def authenticate(self, request):
        user = super(CustomAuthentication, self).authenticate(request)
        if not user:
            return None
        if user[0].is_band:
            raise exceptions.AuthenticationFailed('your user are band tell it to support')
        now = datetime.now()
        if not user[0].expire_time or now < user[0].expire_time:
            return user
        else:
            raise exceptions.AuthenticationFailed('your account has expired')
