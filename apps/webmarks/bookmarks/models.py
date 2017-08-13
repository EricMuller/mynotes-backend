
from webmarks.bookmarks.managers import MediaManager
from webmarks.bookmarks.managers import TagManager
from contrib.django.models import AuditableModelMixin
from users.models import User
from webmarks.core.models import Node
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from model_utils.managers import InheritanceManager
# from mptt.managers import TreeManager

from simple_history.models import HistoricalRecords
from django.template.defaultfilters import slugify
import uuid


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



class Task(Node):
    schedule_dt = models.DateTimeField(null=True)
    pass


class Bookmark(Node):
    """ any kind of Bookmark """

    objects = MediaManager()

    STATUS = (
        ('D', 'Draft'),
        ('V', 'Valid'),
        ('T', 'Trash'),
    )

    title = models.CharField(max_length=256)
    url = models.CharField(max_length=2000, default=None, null=True)
    description = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, related_name="bookmarks", blank=True)

    rate = models.IntegerField(default=0)
    favorite = models.BooleanField(default=False)

    status = models.CharField(max_length=1, choices=STATUS, default='D')
    archive_id = models.IntegerField(null=True)
    archived_dt = models.DateTimeField(null=True)
    history = HistoricalRecords()

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


class Archive(models.Model):
    name = models.SlugField(max_length=255)
    url = models.SlugField(max_length=255)
    content_type = models.CharField(max_length=255)
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    data = models.TextField(
        db_column='data',
        blank=True)

    bookmark = models.ForeignKey(
        Bookmark, related_name='%(class)s_archives', default=None, blank=True)

    @classmethod
    def create(cls, bookmark, content_type, data):
        slug = slugify(bookmark.url)
        archive = cls(name=slug, url=bookmark.url, bookmark=bookmark,
                      content_type=content_type, data=data)
        return archive

# class MediaAttachement(models.Model):
#     name = models.CharField(max_length=255)
#     bookmark = models.ForeignKey(Bookmark)
#     updated_dt = models.DateTimeField(auto_now=True)
#     created_dt = models.DateTimeField(auto_now_add=True)

#     @classmethod
#     def create(cls, name, media):
#         attachement = cls(name=name, media=media)
#         return attachement
