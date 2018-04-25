from rest_framework import serializers

from .models import Board, Topic, Post


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description')


class PostSerializer(serializers.ModelSerializer):
    updated_at = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField(source='created_by.id')
    updated_by = serializers.ReadOnlyField(source='updated_by.id')
    topic = serializers.ReadOnlyField(source='topic.id')

    class Meta:
        model = Post
        fields = ('message', 'topic', 'created_at', 'updated_at', 'created_by',
                  'updated_by')


class TopicSerializer(serializers.ModelSerializer):
    starter = serializers.ReadOnlyField(source='starter.id')
    views = serializers.ReadOnlyField()
    post_count = serializers.SerializerMethodField()
    posts = PostSerializer(write_only=True)

    def create(self, validated_data):
        posts = validated_data.pop('posts')
        topic = Topic.objects.create(**validated_data)
        Post.objects.create(
            message=posts.get('message'),
            topic=topic,
            created_by=validated_data.get('starter')
        )
        return topic

    def get_post_count(self, obj):
        return obj.posts.count()

    class Meta:
        model = Topic
        fields = ('id', 'subject', 'last_updated', 'board', 'starter', 'views',
                  'post_count', 'posts')
