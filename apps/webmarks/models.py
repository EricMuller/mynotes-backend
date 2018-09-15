
from django.db import models
from django.conf import settings
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
import uuid


class AuditableModelMixin(models.Model):
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_user_cre', default=None)
    user_upd = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_user_upd', default=None, blank=True)

    class Meta:
        abstract = True


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
        'webmarks.Folder', related_name="nodes", blank=True)
    indexed_dt = models.DateTimeField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    public = models.BooleanField(default=False)


class Folder(MPTTModel, Node):

    name = models.CharField(max_length=256)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name="children")

    def __str__(self):
        return self.libelle
