
import time
from webmarks.bookmarks import models
from rest_framework import serializers


class TimestampField(serializers.ReadOnlyField):
    """"fields must be a models.DateTimeField"""

    def to_representation(self, value):
        return int(time.mktime(value.timetuple()) * 1000)


# class ModelSerializer(serializers.Serializer):
#     id = serializers.IntegerField()

#     class Meta:
#         fields = ('id')


class CrawlSerializer(serializers.Serializer):
    url = serializers.CharField()
    html = serializers.CharField()
    title = serializers.CharField()
    content_type = serializers.CharField()

    class Meta:
        fields = ('url', 'html', 'title', 'content_type')


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
    parent_id = serializers.IntegerField(required=False)
    tree_id = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    lft = serializers.IntegerField(read_only=True)
    rght = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Folder
        fields = ('id', 'name', 'kind', 'user_cre_id',
                  'user_upd_id', 'parent_id', 'tree_id', 'lft', 'rght', 'level')
        # fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'public')

    def validate(self, validated_data):

        if 'id' not in validated_data:
            validated_data['user_cre'] = self.context['request'].user

        validated_data['user_upd'] = self.context['request'].user

        try:
            models.Tag.objects.get(name=validated_data[
                                   'name'], user_cre=validated_data['user_cre'])
        except models.Tag.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError('Tag already exists')

        return validated_data


class TagCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    count = serializers.IntegerField()

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'count')


class BookmarkTagSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'public')


class BookmarkSerializer(serializers.ModelSerializer):

    # fields must be a models.DateTimeField
    schedule_dt = TimestampField()
    created_dt = TimestampField()
    updated_dt = TimestampField()
    # relations many
    tags = BookmarkTagSerializer(read_only=False, many=True)

    class Meta:
        model = models.Bookmark
        fields = ('id', 'url', 'title', 'kind', 'rate', 'description',
                  'user_cre', 'user_upd', 'created_dt', 'updated_dt',
                  'tags', 'status', 'schedule_dt', 'archived_dt', 'archive_id', 'favorite')
        read_only_fields = ('created_dt', 'updated_dt',
                            'archived_dt', 'archive_id')
        # https://github.com/tomchristie/django-rest-framework/issues/2760
        # extra_kwargs = {'url': {'view_name': 'internal_apis:user-detail'}}

    def validate(self, validated_data):

        if 'id' not in validated_data:
            validated_data['user_cre'] = self.context['request'].user

        validated_data['user_upd'] = self.context['request'].user

        return validated_data

    def create(self, validated_data):

        tags_data = validated_data.pop('tags')
        instance = super(BookmarkSerializer, self).create(validated_data)
        # obj.save(foo=validated_data['foo'])
        for tag_data in tags_data:
            tag = models.Tag.objects.get(id=tag_data['id'])
            if tag is not None:
                instance.tags.add(tag)
        # instance.save()
        return instance

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance = super(BookmarkSerializer, self).update(
            instance, validated_data)
        instance.tags.clear()
        for tag_data in tags_data:
            tag = models.Tag.objects.get(id=tag_data['id'])
            if tag is not None:
                instance.tags.add(tag)
        return instance


class PublishedModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id')

# class SearchSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Search
#         fields = ('name', 'user_cre', 'created_dt', 'tags')
