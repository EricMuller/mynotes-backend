from rest_framework import serializers

from webmarks_social.models import User


class UserSerializer(serializers.ModelSerializer):
    # fields must be a models.DateTimeField

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
