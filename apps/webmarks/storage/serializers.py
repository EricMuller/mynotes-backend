import time
from webmarks.storage import models
from rest_framework import serializers


class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Archive
        fields = ('id', 'name', 'url', 'bookmark',
                  'data',  # 'user_cre', 'user_upd',
                  'created_dt', 'updated_dt')
