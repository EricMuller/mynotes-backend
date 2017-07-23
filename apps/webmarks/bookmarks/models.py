from webmarks.bookmarks.managers import MediaManager
from webmarks.bookmarks.managers import TagManager
from webmarks.drf_utils.models import AuditableModelMixin
from webmarks.users.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from model_utils.managers import InheritanceManager
# from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords


class Tag(models.Model):

    objects = TagManager()

    name = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        User, related_name='%(class)s_user_cre', blank=True)
    user_upd = models.ForeignKey(
        User, related_name='%(class)s_user_upd', blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self.name)

    class Meta:
        unique_together = ('name', 'user_cre',)


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
        'Folder', related_name="nodes", blank=True)
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


class Bookmark(Node):

    objects = MediaManager()

    STATUS = (
        ('D', 'Draft'),
        ('V', 'Valid'),
        ('T', 'Trash'),
    )

    archive_id = models.IntegerField(null=True)
    archived_dt = models.DateTimeField(null=True)
    description = models.TextField(blank=True)
    favorite = models.BooleanField(default=False)
    history = HistoricalRecords()
    public = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)
    schedule_dt = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, choices=STATUS, default='D')
    tags = models.ManyToManyField(Tag, related_name="bookmarks", blank=True)
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=2000, default=None, null=True)

    def get_status_libelle(self):
        t = [item for item in self.STATUS if item[0] == self.status]
        return '' if t is None else t[0][1]

    def get_type_libelle(self):
        t = [item for item in self.TYPES if item[0] == self.type]
        return '' if t is None else t[0][1]

    def tagsAsStr(self, sep=','):
        return sep.join(s.name for s in self.tags.all())

    @classmethod
    def create(cls, title, description, type):
        media = cls(title=title, type=type, description=description)
        return media

    def __str__(self):
        return 'id=' + str(self.id) + ';title=' + \
            self.title + ';status=' + self.status

    class Meta:
        pass


# class MediaAttachement(models.Model):
#     name = models.CharField(max_length=255)
#     bookmark = models.ForeignKey(Bookmark)
#     updated_dt = models.DateTimeField(auto_now=True)
#     created_dt = models.DateTimeField(auto_now_add=True)

#     @classmethod
#     def create(cls, name, media):
#         attachement = cls(name=name, media=media)
#         return attachement
