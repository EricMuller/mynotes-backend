
from django.db import models
import uuid
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from webmarks.users.models import User


class AuditableModelMixin(models.Model):
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        User, related_name='%(class)s_user_cre', default=None)
    user_upd = models.ForeignKey(
        User, related_name='%(class)s_user_upd', default=None, blank=True)

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

    kind = models.CharField(max_length=10, choices=KINDS, default='NOTE')
    folders = models.ManyToManyField(
        'base.Folder', related_name="nodes", blank=True)
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
