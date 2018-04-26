from django.utils import timezone
from rest_framework import generics, permissions

from boards.models import Board, Topic, Post
from rest_boards.serializers import BoardSerializer, TopicSerializer, PostSerializer


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class TopicList(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        board_pk = self.kwargs['pk']
        board = Board.objects.get(pk=board_pk)
        return board.topics.order_by('-last_updated')

    def perform_create(self, serializer):
        board_pk = self.kwargs['pk']
        board = Board.objects.get(pk=board_pk)
        serializer.save(starter=self.request.user,
                        board=board)


class TopicDetail(generics.RetrieveAPIView):
    serializer_class = TopicSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'topic_pk'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        board_pk = self.kwargs['pk']
        board = Board.objects.get(pk=board_pk)
        return board.topics.all()


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        board_pk = self.kwargs['pk']
        topic_pk = self.kwargs['topic_pk']
        topic = Topic.objects.get(board__pk=board_pk,
                                  pk=topic_pk)
        return topic.posts.order_by('created_at')

    def perform_create(self, serializer):
        board_pk = self.kwargs['pk']
        topic_pk = self.kwargs['topic_pk']
        topic = Topic.objects.get(board__pk=board_pk,
                                  pk=topic_pk)
        serializer.save(created_by=self.request.user,
                        topic=topic)


class PostDetail(generics.RetrieveUpdateAPIView):
    serializer_class = PostSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_pk'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        board_pk = self.kwargs['pk']
        topic_pk = self.kwargs['topic_pk']
        topic = Topic.objects.get(board__pk=board_pk,
                                  pk=topic_pk)
        return topic.posts.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user,
                        updated_at=timezone.now())
