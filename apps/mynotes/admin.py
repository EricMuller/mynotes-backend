from django.contrib import admin

# Register your models here.

from apps.mynotes.models import Model
from apps.mynotes.models import Note
from apps.mynotes.models import Tag
from apps.mynotes.models import Search
from apps.mynotes.models import FileUploader
from simple_history.admin import SimpleHistoryAdmin


admin.site.register(Search)
admin.site.register(Model)
admin.site.register(FileUploader)


class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


admin.site.register(Tag, TagAdmin)
admin.site.register(Note, SimpleHistoryAdmin)
