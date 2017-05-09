from apps.mywebmarks import viewsets
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

apiRouter = routers.DefaultRouter()
apiRouter.register(r'folders', viewsets.FolderViewSet)
apiRouter.register(r'bookmarks', viewsets.BookmarkViewSet)
apiRouter.register(r'search', viewsets.SearchViewSet)
apiRouter.register(r'tags-cloud', viewsets.TagCloudViewSet,
                   base_name='tags-cloud')
apiRouter.register(r'tags', viewsets.TagViewSet)
apiRouter.register(r'upload', viewsets.FileUploaderViewSet)
apiRouter.register(r'crawler', viewsets.CrawlerViewSet, base_name='crawler')
apiRouter.register(r'archive', viewsets.ArchiveViewSet, base_name='archive')

urlpatterns = [
    # API
    url(r'^api/v1/', include(apiRouter.urls, namespace='external_apis')),

]
