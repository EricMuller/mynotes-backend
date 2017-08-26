from webmarks.storage import viewsets
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

apiRouter = routers.DefaultRouter()
apiRouter.register(r'storages', viewsets.DataStorageViewSet,
                   base_name='storages')
apiRouter.register(r'stores', viewsets.StoreViewSet,
                   base_name='stores')

urlpatterns = [
    # API V1
    url(r'v1/', include(apiRouter.urls, namespace='external_apis')),
]
