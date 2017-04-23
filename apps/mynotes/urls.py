from apps.mynotes import viewsets
# from apps.mynotes.apiviews import obtain_auth_token
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework import response, schemas
# from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

# @api_view()
# @renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
# def schema_view(request):
#     generator = schemas.SchemaGenerator(title='MyNotes API')
#     return response.Response(generator.get_schema(request=request))

apiRouter = routers.DefaultRouter()
apiRouter.register(r'notes', viewsets.NoteViewSet)
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

    # url(r'^api/authenticate', obtain_auth_token),
    # url(r'^api-token-auth/', obtain_auth_token),
    # url(r'^docs/', schema_view),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),
]
