# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
# from django.views.generic import RedirectView
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_swagger.views import get_swagger_view

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_swagger.views import get_swagger_view

from rest_framework.renderers import CoreJSONRenderer


schema_url_patterns = [
    url(r'^api/', include('webmarks.bookmarks.urls',
                          namespace='bookmarks')),
]

schema_url_patterns_auth = [
    url(r'^api/', include('webmarks.rest_auth.urls',
                                   namespace='rest_auth')),
]

schema_view = get_schema_view(
    title='Webmarks API',
    # url='https://webmarks.net/',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    patterns=schema_url_patterns,
)

schema_view_auth = get_schema_view(
    title='Rest Authentification API',
    # url='https://webmarks.net/',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer],
    patterns=schema_url_patterns_auth,
)

# schema_view_swagger = get_swagger_view(title='Django API')
# schema_view = get_schema_view(title='Webmarks API REST', renderer_classes=[

# OpenAPIRenderer, SwaggerUIRenderer])
# schema_view = get_swagger_view(title='My great API', url='')

urlpatterns = [
    # url(r'^about/$',
    # TemplateView.as_view(template_name='pages/about.html'), name='about'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^api/$',
        TemplateView.as_view(template_name='api/index.html'), name='index_api'),
    url(r'^api/', include('webmarks.bookmarks.urls',
                          namespace='bookmarks')),
    url(r'^api/', include('webmarks.storage.urls',
                          namespace='storage')),
    url(r'^api/', include('webmarks.rest_auth.urls')),

    url(r'^api/webmarks/', schema_view),
    url(r'^api/rest_auth/', schema_view_auth),
    # User management
    url(r'^users/', include('webmarks.users.urls', namespace='users')),
    url(r'^$',
        TemplateView.as_view(template_name='index.html'), name='index'),
    # Ajout authentification pour browsable api need
    # include('rest_framework.urls')
    url(r'^rest_framework/', include('rest_framework.urls')),
    # http://django-rest-auth.readthedocs.io/en/latest/installation.html


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
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
