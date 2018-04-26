from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedIdentityField

from boards.models import Board, Topic, Post


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    post_count = serializers.SerializerMethodField()
    topic_count = serializers.SerializerMethodField()

    def get_post_count(self, obj):
        return obj.get_posts_count()

    def get_topic_count(self, obj):
        return obj.topics.count()

    class Meta:
        model = Board
        fields = ('name', 'description', 'post_count', 'topic_count', 'url')
        extra_kwargs = {
            'url': {'view_name': 'rest_board:board_detail'}
        }


class PostSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'pk': 'topic__board__id',
        'topic_pk': 'topic__id'
    }
    updated_at = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField(source='created_by.id')
    updated_by = serializers.ReadOnlyField(source='updated_by.id')
    topic = NestedHyperlinkedIdentityField(view_name='rest_board:topic_detail',
                                           parent_lookup_kwargs={
                                               'pk': 'topic__board__id',
                                               'topic_pk': 'topic__id'
                                           })

    class Meta:
        model = Post
        fields = ('message', 'created_at', 'updated_at', 'created_by',
                  'updated_by', 'topic', 'url')
        extra_kwargs = {
            'url': {'view_name': 'rest_board:post_detail',
                    'lookup_url_kwarg': 'post_pk'}
        }


class TopicSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'pk': 'board__id'
    }

    starter = serializers.ReadOnlyField(source='starter.id')
    board = NestedHyperlinkedIdentityField(view_name='rest_board:board_detail',
                                           parent_lookup_kwargs={'pk': 'board__id'})
    views = serializers.ReadOnlyField()
    post_count = serializers.SerializerMethodField()
    posts = PostSerializer(write_only=True)

    def create(self, validated_data):
        print(validated_data)
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
        fields = ('subject', 'starter', 'post_count', 'views', 'posts',
                  'last_updated', 'board', 'url')
        extra_kwargs = {
            'url': {'view_name': 'rest_board:topic_detail',
                    'lookup_url_kwarg': 'topic_pk'}
        }
