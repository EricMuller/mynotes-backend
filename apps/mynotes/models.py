from apps.users.models import User
from apps.mynotes.managers import NoteManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
# from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from simple_history.models import HistoricalRecords
from apps.mynotes.managers import TagManager


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


class Model(MPTTModel):

    parent = TreeForeignKey('self', null=True, blank=True)
    code = models.CharField(_("code"), max_length=64,
                            db_index=True)
    libelle = models.CharField(max_length=256)

    def __str__(self):
        return self.libelle

class Search(models.Model):
    name = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag, related_name="tags_search")
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        User, related_name='%(class)s_user_cre', blank=True)
    user_upd = models.ForeignKey(
        User, related_name='%(class)s_user_upd', blank=True)


class Favorite(models.Model):
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=2000, default=None, null=True)
    add_dt = models.DateTimeField()
    icon = models.CharField(max_length=2000, default=None, null=True)


class FileUploader(models.Model):
    TYPES = (
        ('FAVORITE', 'Favorite'),
    )
    file = models.FileField()
    type = models.CharField(max_length=10, choices=TYPES)
    # name is filename without extension
    name = models.CharField(max_length=100)
    version = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey(User, related_name='uploaded_files')
    size = models.IntegerField(default=0)


class Note(models.Model):

    objects = NoteManager()

    TYPES = (
        ('NOTE', 'Note'),
        ('TODO', 'Todo'),
        ('MAIL', 'Mail'),
        ('LINK', 'Link'),

    )
    STATUS = (
        ('D', 'Draft'),
        ('V', 'Valid'),
        ('T', 'Trash'),
    )

    title = models.CharField(max_length=256)
    url = models.CharField(max_length=2000, default=None, null=True)
    description = models.TextField(blank=True)
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        User, related_name='%(class)s_user_cre', default=None)
    user_upd = models.ForeignKey(
        User, related_name='%(class)s_user_upd', default=None, blank=True)
    rate = models.IntegerField(default=0)
    # type = models.ForeignKey(
    #     TypeNote, verbose_name='TypeNote', null=True,
    #     default=None, blank=True, related_name='TypeNote')

    type = models.CharField(max_length=10, choices=TYPES, default='NOTE')

    status = models.CharField(max_length=1, choices=STATUS, default='D')

    public = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)

    schedule_dt = models.DateTimeField(null=True)
    # taggs = models.CharField(max_length=2000, default=None, null=True)

    history = HistoricalRecords()

    def get_status_libelle(self):
        t = [item for item in self.STATUS if item[0] == self.status]
        return '' if t is None else t[0][1]

    def get_type_libelle(self):
        t = [item for item in self.TYPES if item[0] == self.type]
        return '' if t is None else t[0][1]

    def tagsAsStr(self, sep=','):
        # return ''
        return sep.join(s.name for s in self.tags.all())

    @classmethod
    def create(cls, title, description, type):
        note = cls(title=title, type=type, description=description)
        return note

    def __str__(self):
        return str(self.id) + ' ' + self.title + ' ' + self.status


class NoteAttachement(models.Model):
    name = models.CharField(max_length=255)
    note = models.ForeignKey(Note)
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, name, note):
        attachement = cls(name=name, note=note)
        return attachement
