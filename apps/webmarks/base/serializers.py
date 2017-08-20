
import time
from webmarks.base import models
from rest_framework import serializers


class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Node
        fields = '__all__'
        # fields = ('id', 'name', 'kind', 'user_cre_id',
        # 'user_upd_id', 'parent_id', 'tree_id', 'lft', 'rght', 'level')


class FolderSerializer(serializers.ModelSerializer):

    def validate(self, validated_data):

        if 'id' not in validated_data:
            validated_data['user_cre'] = self.context['request'].user

        validated_data['user_upd'] = self.context['request'].user

        return validated_data

    kind = serializers.CharField()
    name = serializers.CharField()
    user_cre_id = serializers.IntegerField(read_only=True)
    user_upd_id = serializers.IntegerField(read_only=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    tree_id = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    lft = serializers.IntegerField(read_only=True)
    rght = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Folder
        fields = ('id', 'name', 'kind', 'user_cre_id',
                  'user_upd_id', 'parent_id', 'tree_id',
                  'lft', 'rght', 'level')
        # fields = '__all__'
