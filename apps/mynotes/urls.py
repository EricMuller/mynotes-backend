from apps.mynotes import authentification
from apps.mynotes import viewsets
# from apps.mynotes.apiviews import obtain_auth_token
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


apiRouter = routers.DefaultRouter()
apiRouter.register(r'notes', viewsets.NoteViewSet)
apiRouter.register(r'search', viewsets.SearchViewSet)
apiRouter.register(r'tags-cloud', viewsets.TagCloudViewSet,
                   base_name='tags-cloud')
apiRouter.register(r'tags', viewsets.TagViewSet)
apiRouter.register(r'upload', viewsets.FileUploaderViewSet)
apiRouter.register(r'crawler', viewsets.CrawlerViewSet, base_name='crawler')

urlpatterns = [
    # API
    url(r'^api/v1/', include(apiRouter.urls, namespace='external_apis')),

    url(r'^api/v1/signup/facebook$',
        csrf_exempt(authentification.FacebookLoginOrSignup.as_view()),
        name='facebook-login-signup'),
    # url(r'^api/authenticate', obtain_auth_token),
    url(r'^api-token-auth/', obtain_auth_token),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
]
