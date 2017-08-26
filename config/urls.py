# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer
from rest_framework_swagger.renderers import OpenAPIRenderer

schema_url_patterns = [
    url(r'^api/', include('webmarks.bookmarks.urls',
                          namespace='bookmarks')),
]

schema_url_patterns_storage = [
    url(r'^api/', include('webmarks.storage.urls',
                          namespace='storage')),
]

schema_url_patterns_auth = [
    url(r'^api/', include('webmarks.authentication.urls',
                          namespace='authentication')),
]

schema_view = get_schema_view(
    title='Bookmark API',
    # url='https://webmarks.net/',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    patterns=schema_url_patterns,
    public=True,
)

schema_view_storage = get_schema_view(
    title='Storage API',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    patterns=schema_url_patterns_storage,
    public=True,
)

schema_view_auth = get_schema_view(
    title='Authentification API',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    patterns=schema_url_patterns_auth,
)

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='index.html'), name='index'),
    url(settings.ADMIN_URL, include(admin.site.urls)),
    # webmarks api
    url(r'^api/', include('webmarks.bookmarks.urls',
                          namespace='bookmarks')),
    url(r'^api/', include('webmarks.storage.urls',
                          namespace='storage')),
    url(r'^api/', include('webmarks.authentication.urls')),
    # swagger
    url(r'^api/$',
        TemplateView.as_view(template_name='api/index.html'),
        name='index_api'),
    url(r'^api/bookmark/', schema_view),
    url(r'^api/storage/', schema_view_storage),
    url(r'^api/rest_auth/', schema_view_auth),

    # browsable api need rest_framework for authentification
    url(r'^rest_framework/', include('rest_framework.urls')),
    # http://django-rest-auth.readthedocs.io/en/latest/installation.html

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]


# logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.ERROR)
