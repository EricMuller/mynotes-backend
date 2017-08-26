from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from webmarks.bookmarks import viewsets

apiRouter = routers.DefaultRouter()
apiRouter.register(r'upload', viewsets.UploadViewSet)

urlpatterns = [
    # API V1
    url(r'v1/', include(apiRouter.urls, namespace='external_apis')),
]
