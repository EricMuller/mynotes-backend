

from rest_framework import serializers


class CrawlSerializer(serializers.Serializer):
    url = serializers.CharField()
    html = serializers.CharField()
    title = serializers.CharField()
    content_type = serializers.CharField()

    class Meta:
        fields = ('url', 'html', 'title', 'content_type')
