from django.db import models
from webmarks.bookmarks.models import Bookmark
from django.template.defaultfilters import slugify


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
        Bookmark, related_name='archives', default=None, blank=True)

    @classmethod
    def create(cls, bookmark, content_type, data):
        slug = slugify(bookmark.url)
        archive = cls(name=slug, url=bookmark.url, bookmark=bookmark,
                      content_type=content_type, data=data)
        return archive
