from django.conf import settings


def generate_setting_dict():
    return {
        "allow_host": settings.ALLOWED_HOSTS,
        "debug": settings.DEBUG,
        "swagger": settings.SWAGGER_ENABLE,
        "expire_session": (settings.SESSION_COOKIE_AGE / 3600),
        "expire_when_tab_close": settings.SESSION_EXPIRE_AT_BROWSER_CLOSE,
        "default_paginate_size": settings.REST_FRAMEWORK['PAGE_SIZE']
    }
