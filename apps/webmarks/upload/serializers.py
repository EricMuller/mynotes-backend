
import os
from webmarks.upload import models
from rest_framework import serializers


class UploadSerializer(serializers.ModelSerializer):
    # overwrite = serializers.BooleanField()
    class Meta:
        model = models.Upload
        fields = ('id', 'file', 'name', 'version', 'upload_date', 'size')
        read_only_fields = ('name', 'version', 'owner', 'upload_date', 'size')

    def validate(self, validated_data):

        validated_data['owner'] = self.context['request'].user
        validated_data['name'] = os.path.splitext(
            validated_data['file'].name)[0]
        validated_data['size'] = validated_data['file'].size
        # other validation logic
        return validated_data

    def create(self, validated_data):
        return models.Upload.objects.create(**validated_data)
