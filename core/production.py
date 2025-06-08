from .settings import *  # noqa

DEBUG = False
"""
IF YOU WANT SET CSRF_TRUSTED_ORIGINS = ["*"] THEN YOU SHOULD SET:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
"""

# CSRF_COOKIE_SECURE = True
#
#
#
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://zamonsher.icu',
]