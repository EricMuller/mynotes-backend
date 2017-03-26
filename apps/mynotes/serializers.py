
import os
import time
from apps.mynotes import models
from rest_framework import serializers


class TimestampField(serializers.ReadOnlyField):

    def to_representation(self, value):
        return int(time.mktime(value.timetuple()) * 1000)


class ArchiveSerializer(serializers.ModelSerializer):

    # url = models.SlugField(max_length=255)
    # note = models.ForeignKey(Note)

    class Meta:
        model = models.Archive
        fields = ('name', 'url', 'note',
                  # 'user_cre', 'user_upd',
                  'created_dt', 'updated_dt')


class CrawlSerializer(serializers.Serializer):
    url = serializers.CharField()
    html = serializers.CharField()
    title = serializers.CharField()

    class Meta:
        fields = ('url', 'html', 'title')


class TagSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    # id = serializers.ReadOnlyField()

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'public')

    def validate(self, validated_data):

        if 'id' not in validated_data:
            validated_data['user_cre'] = self.context['request'].user

        validated_data['user_upd'] = self.context['request'].user

        return validated_data


class NoteListSerializer(serializers.ModelSerializer):

    tags = TagSerializer(read_only=False, many=True)
    archive_id = serializers.IntegerField(source='archive.note.id')

    def get_archive_id(self, obj):

        return None if obj.archive is None else obj.archive.note_id

    class Meta:
        model = models.Note
        fields = ('id', 'url', 'title', 'type', 'rate', 'user_cre', 'user_upd',
                  'created_dt', 'updated_dt', 'tags', 'status', 'schedule_dt',
                  'archived_dt', 'archive_id')


class NoteSerializer(serializers.ModelSerializer):

    tags = TagSerializer(read_only=False, many=True)
    # Source must be a models.DateTimeField
    schedule_dt = TimestampField()
    created_dt = TimestampField()
    updated_dt = TimestampField()
    archive_id = serializers.IntegerField(source='archive.note.id')

    class Meta:
        model = models.Note
        fields = ('id', 'url', 'title', 'type', 'rate', 'description',
                  'user_cre', 'user_upd', 'created_dt', 'updated_dt',
                  'tags', 'status', 'schedule_dt', 'archived_dt', 'archive_id')
        read_only_fields = ('created_dt', 'updated_dt',
                            'archived_dt', 'archive')
        # https://github.com/tomchristie/django-rest-framework/issues/2760
        # extra_kwargs = {'url': {'view_name': 'internal_apis:user-detail'}}

    def validate(self, validated_data):

        if 'id' not in validated_data:
            validated_data['user_cre'] = self.context['request'].user

        validated_data['user_upd'] = self.context['request'].user

        return validated_data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        instance = super(NoteSerializer, self).create(validated_data)
        # obj.save(foo=validated_data['foo'])
        for tag_data in tags_data:
            tag = models.Tag.objects.get(id=tag_data['id'])
            if tag is not None:
                instance.tags.add(tag)
        # instance.save()
        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance = super(NoteSerializer, self).update(instance, validated_data)
        instance.tags.clear()
        for tag_data in tags_data:
            tag = models.Tag.objects.get(id=tag_data['id'])
            if tag is not None:
                instance.tags.add(tag)
        return instance


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Search
        fields = ('name', 'user_cre', 'created_dt', 'tags')


class TagCloudSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    count = serializers.IntegerField()

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'count')


class FileUploaderSerializer(serializers.ModelSerializer):
    # overwrite = serializers.BooleanField()
    class Meta:
        model = models.FileUploader
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
        return models.FileUploader.objects.create(**validated_data)
