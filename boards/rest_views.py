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


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        board_pk = self.kwargs['pk']
        topic_pk = self.kwargs['topic_pk']
        topic = Topic.objects.get(board__pk=board_pk,
                                  pk=topic_pk)
        return topic.posts.order_by('created_at')
