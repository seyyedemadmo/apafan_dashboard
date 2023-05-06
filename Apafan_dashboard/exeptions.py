from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _



class CustomInvalidToken(AuthenticationFailed):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Token is invalid or expired")
    default_code = "token_not_valid"
