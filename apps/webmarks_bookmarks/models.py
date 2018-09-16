
from django.db import models
from django.conf import settings
from webmarks_folders.models import Node
from webmarks_bookmarks.managers import TagManager


class Tag(models.Model):

    objects = TagManager()

    name = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='%(class)s_user_cre', blank=True)
    user_upd = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='%(class)s_user_upd', blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self.name)

    class Meta:
        unique_together = ('name', 'user_cre',)


class Bookmark(Node):
    """ any kind of Bookmark """

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
    archive_id = models.UUIDField(null=True)
    archived_dt = models.DateTimeField(null=True)

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
