from django.db import models
import uuid
# from django.template.defaultfilters import slugify


class Store(models.Model):

    WBM_STORE = 'WBMSTORE'
    KINDS = (
        ('WBMSTORE', 'Webmarks Store'),
        ('GOOGLEDRV', 'Google Drive')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kind = models.CharField(
        max_length=15, choices=KINDS, default=WBM_STORE)
    user_uuid = models.UUIDField()
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, kind, user_uuid):
        return cls(kind=kind, user_uuid=user_uuid)


class DataStorage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(max_length=255)
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    node_uuid = models.UUIDField()
    store = models.ForeignKey(Store, related_name='%(class)s_store')

    @classmethod
    def create(cls, node_uuid, content_type, store):
        # slug = slugify(bookmark.url)
        return cls(node_uuid=node_uuid, content_type=content_type, store=store)
