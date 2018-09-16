
from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
import uuid
from webmarks_django_contrib.models import AuditableModelMixin


class Node(AuditableModelMixin):

    KINDS = (
        ('NOTE', 'Note'),
        ('TODO', 'Todo'),
        ('MAIL', 'Mail'),
        ('LINK', 'Link'),
        ('FLDR', 'Folder'),
    )

    kind = models.CharField(max_length=10, choices=KINDS, default='LINK')
    folders = models.ManyToManyField(
        'webmarks_folders.Folder', related_name="nodes", blank=True)
    indexed_dt = models.DateTimeField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    public = models.BooleanField(default=False)


class Folder(MPTTModel, Node):

    name = models.CharField(max_length=256)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name="children")

    def __str__(self):
        return self.libelle
