REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'Apafan_dashboard.rendrer.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'Apafan_dashboard.authoraization.CustomAuthentication',
    ),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    "LOGIN_URL": "/api/auth/login/",
    "LOGOUT_URL": "/api/auth/logout/",
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}
