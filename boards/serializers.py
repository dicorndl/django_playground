from rest_framework import serializers

from .models import Board, Topic


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description')


class TopicSerializer(serializers.ModelSerializer):
    starter = serializers.ReadOnlyField(source='starter.id')

    class Meta:
        model = Topic
        fields = ('id', 'subject', 'last_updated', 'board', 'starter', 'views')
