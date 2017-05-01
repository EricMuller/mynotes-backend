from django.contrib import admin

# Register your models here.

from apps.mywebmarks.models import Model
from apps.mywebmarks.models import Media
from apps.mywebmarks.models import Tag
from apps.mywebmarks.models import Search
from apps.mywebmarks.models import FileUploader
from simple_history.admin import SimpleHistoryAdmin


admin.site.register(Search)
admin.site.register(Model)
admin.site.register(FileUploader)


class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


admin.site.register(Tag, TagAdmin)
admin.site.register(Media, SimpleHistoryAdmin)
