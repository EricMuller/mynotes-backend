# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from webmarks_social.apiviews import ApiCurrentUserView
from webmarks_social.viewsets import UserViewSet

apiRouter = routers.DefaultRouter()
apiRouter.register(r'users', UserViewSet)

urlpatterns = [
    # API V1
    url(r'v1/', include(apiRouter.urls, namespace='external_apis')),
    url(r'v1/users/me', ApiCurrentUserView.as_view())
]

