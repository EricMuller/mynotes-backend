from rest_framework import serializers
from webmarks.storage import models


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = ('id', 'user_uuid', 'kind',  # 'user_cre', 'user_upd',
                  'created_dt', 'updated_dt')


class DataStorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DataStorage
        fields = ('id', 'node_uuid',   # 'user_cre', 'user_upd',
                  'created_dt', 'updated_dt')
