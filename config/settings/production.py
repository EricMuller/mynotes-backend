# -*- coding: utf-8 -*-
import socket
import os
from .base import *  # noqa

# DEBUG
# Conf non terminee
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[
    'localhost', '127.0.0.1', 'webmarks.net'])
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

EMAIL_HOST = env("EMAIL_HOST", default='localhost')


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
    env('REDIS_ENDPOINT_ADDRESS', default='127.0.0.1'),
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

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# postgres://mynotes:mynotes@localhost:5432/mynotes
# postgres:///mynotes
# default='postgres://mynotes:mynotes@192.168.1.100:5432/webmarks')
USERNAME = env('USER')
DB_HOST_NAME = env('WEBMARK_DB_HOST_NAME', default=HOST_NAME)
DB_NAME = env('WEBMARK_DB_NAME', default=USERNAME)
DATABASES = {
    'default': env.db('WEBMARK_DATABASE_URL', default='postgres://@' +
                      DB_HOST_NAME + '/' + DB_NAME),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
print("env variable DB_HOST_NAME/DB_NAME=" +
      DATABASES['default']['HOST'] + '/' + DB_NAME)




# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )


# CELERY
# In development, all tasks will be executed locally by blocking until the
# task returns
CELERY_ALWAYS_EAGER = False
# END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
