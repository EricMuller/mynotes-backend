
from contrib.django.models import AuditableModelMixin
from django.db import models
import uuid
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey


class Node(AuditableModelMixin):

    KINDS = (
        ('NOTE', 'Note'),
        ('TODO', 'Todo'),
        ('MAIL', 'Mail'),
        ('LINK', 'Link'),
        ('FLDR', 'Folder'),
    )

    kind = models.CharField(max_length=10, choices=KINDS, default='NOTE')
    folders = models.ManyToManyField(
        'webmarks_core.Folder', related_name="nodes", blank=True)
    indexed_dt = models.DateTimeField(null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    public = models.BooleanField(default=False)
    # type = models.ForeignKey(
    #     TypeNote, verbose_name='TypeNote', null=True,
    #     default=None, blank=True, related_name='TypeNote')
    #     objects = InheritanceManager()
    #     kind = models.CharField(max_length=10, choices=KINDS, default='NOTE')
    #     container = models.ManyToManyField(
    #         Container, related_name="containers", blank=True)


class Folder(MPTTModel, Node):

    name = models.CharField(max_length=256)
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name="children")

    def __str__(self):
        return self.libelle
