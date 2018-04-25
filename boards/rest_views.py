from rest_framework import generics, permissions

from boards.models import Board, Topic, Post
from boards.serializers import BoardSerializer, TopicSerializer, PostSerializer


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

    def perform_create(self, serializer):
        serializer.save(starter=self.request.user)

    def get_queryset(self):
        board_pk = self.kwargs['pk']
        board = Board.objects.get(pk=board_pk)
        return board.topics.order_by('-last_updated')


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
