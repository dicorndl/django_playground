from django.contrib.auth.models import User
from rest_framework import serializers

from boards.models import Topic


class UserSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(many=True,
                                                queryset=Topic.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'topics')
