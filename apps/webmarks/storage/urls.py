from webmarks.storage import viewsets
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

apiRouter = routers.DefaultRouter()
# apiRouter.register(r'upload', viewsets.FileUploaderViewSet)
# apiRouter.register(r'crawler', viewsets.CrawlerViewSet, base_name='crawler')
apiRouter.register(r'archives', viewsets.ArchiveViewSet, base_name='archive')

urlpatterns = [
    # API V1
    url(r'v1/', include(apiRouter.urls, namespace='external_apis')),
]
