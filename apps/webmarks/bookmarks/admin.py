from django.contrib import admin

# Register your models here.

from webmarks.bookmarks.models import Bookmark
from webmarks.bookmarks.models import Tag


class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


admin.site.register(Tag, TagAdmin)
admin.site.register(Bookmark)
