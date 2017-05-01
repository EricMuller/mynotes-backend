# -*- coding: utf-8 -*-
"""
Django settings for mynotes project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

# (mywebmarks/config/settings/common.py - 3 = mywebmarks/)
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('apps')

env = environ.Env()

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
    'channels',
)

THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    'allauth',
    # registration
    # http://django-allauth.readthedocs.io/en/latest/providers.html
    'allauth.account',
    'rest_auth.registration',
    # https://console.developers.google.com/apis?project=snappy-bucksaw-146613
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.dropbox_oauth2',
    'jsonify',
    'mptt',
    'simple_history',
    'rest_framework_swagger',
    # 'easy_select2',
    # rest social authent
    # 'oauth2_provider',
    # 'social.apps.django_app.default',
    # 'rest_framework_social_oauth2',

)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    'apps.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'apps.authentication.apps.AuthenticationConfig',
    'apps.mywebmarks.apps.MyWebmarksConfig',
    # 'apps.mywebmarks-frontend.apps.MynotesViewConfig',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'apps.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', default=True)
# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
# default='django.core.mail.backends.console.EmailBackend')
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.smtp.EmailBackend')
# mailhog  http://iankent.uk/blog/introducing-go-mailhog/
#

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Eric Muller""", 'admin@webmarks.online'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# postgres://mynotes:mynotes@localhost:5432/mynotes
# postgres:///mynotes
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://mynotes:mynotes@192.168.1.100:5432/mywebmarks'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Istanbul'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 2

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See:
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See:
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See:
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See:
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
                # 'allauth.account.context_processors.account',
                # 'allauth.socialaccount.context_processors.socialaccount',
                # rest social autent
                # 'social.apps.django_app.context_processors.backends',
                # 'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

# See:
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# STATIC_URL = 'http://192.168.0.100/static/mywebmarks/'

# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_ROOT = str(ROOT_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

#
SITE_ID = 1

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URLNAME = "/"

ACCOUNT_ALLOW_REGISTRATION = env.bool(
    'DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'apps.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.users.adapters.SocialAccountAdapter'

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
# LOGIN_REDIRECT_URL = 'users:redirect'
# LOGIN_URL = 'account_login'
LOGIN_URL = '/login'


LOGIN_REDIRECT_URL = "/login"
# test
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/login'
# SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_EMAIL_REQUIRED = False
# SOCIALACCOUNT_QUERY_EMAIL = False

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = \
    {'google':
     {'SCOPE': ['profile', 'email'],
      'AUTH_PARAMS': {'access_type': 'online'}}}
# /test
# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# CELERY
INSTALLED_APPS += ('apps.taskapp.celery.CeleryConfig',)
# if you are not using the django database broker (e.g. rabbitmq, redis,
# memcached), you can remove the next line.
INSTALLED_APPS += ('kombu.transport.django',)
BROKER_URL = env('CELERY_BROKER_URL', default='django://')
if BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = BROKER_URL
# END CELERY
# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("compressor", )
STATICFILES_FINDERS += ("compressor.finders.CompressorFinder", )

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

SELECT2_JS = 'vendors/select2/vendor/select2/js/select2.min.js'

SELECT2_CSS = 'vendors/select2/vendor/select2/css/select2.min.css'

SELECT2_USE_BUNDLED_JQUERY = False

STORE_ROOT = '/ged/store/'

# REST_FRAMEWORK = {

#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'oauth2_provider.ext.rest_framework.OAuth2Authentication',
#         'rest_framework_social_oauth2.authentication.SocialAuthentication',
#     ),
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'apps.handlers.custom_exception_handler'
}


SWAGGER_SETTINGS = {
    # for swagger / browsable api  should include('rest_framework.urls')
    'LOGIN_URL': 'rest_framework:login',
}

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.


if DEBUG:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'apps': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True
            },
            'django.template': {
                'level': 'ERROR',
                'handlers': ['console', 'mail_admins'],
                'propagate': True
            },
            'django.security.DisallowedHost': {
                'level': 'ERROR',
                'handlers': ['console', 'mail_admins'],
                'propagate': True
            }
        }
    }
