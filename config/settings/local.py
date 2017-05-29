# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use mailhog for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket
import os

from .common import *  # noqa

HOST_NAME = env('HOST_NAME', default='127.0.0.1')

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[
                         HOST_NAME, 'localhost', '127.0.0.1'])

if not DEBUG:
    print ("env variable DJANGO_DEBUG is False !!!")
    # start django with --insecure for static file

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='r(f_)4bp@%ritjy#gq19f0_z+c8+#zr=0b@)w8)_-f=+)*k0j0')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = env("EMAIL_HOST", default=HOST_NAME)

EMAIL_HOST_USER = 'e.mul'
EMAIL_HOST_PASSWORD = 'sdfghj35'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL
# EMAIL_TIMEOUT
# EMAIL_SSL_KEYFILE
# EMAIL_SSL_CERTFILE

# CACHING
# ------------------------------------------------------------------------------
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': ''
#     }
# }
# CACHING
# ------------------------------------------------------------------------------
REDIS_LOCATION = "redis://{}:{}/0".format(
    env('REDIS_ENDPOINT_ADDRESS', default=HOST_NAME),
    env('REDIS_PORT', default=6379)
)

# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}

# django-channels
# ------------------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "config.routing.channel_routing",
    },
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "ROUTING": "config.routing.channel_routing",
#         # "CONFIG": {
#         #     "hosts": [("redis-channel-1", 6379), ("redis-channel-2", 6379)],
#         # },
#     },
# }

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# CELERY
# In development, all tasks will be executed locally by blocking until the
# task returns
CELERY_ALWAYS_EAGER = True
# END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
