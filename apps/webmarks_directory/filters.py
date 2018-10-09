from .models import Folder
from rest_framework import filters


class FolderFilter(filters.FilterSet):

    class Meta:
        model = Folder
        fields = ['id', 'tree_id', 'level', 'parent_id']
