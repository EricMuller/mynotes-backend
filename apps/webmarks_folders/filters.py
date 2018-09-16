from webmarks_folders import models
from rest_framework import filters


class FolderFilter(filters.FilterSet):

    class Meta:
        model = models.Folder
        fields = ['id', 'tree_id', 'level', 'parent_id']
