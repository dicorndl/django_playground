from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^boards/$',
        views.BoardList.as_view(), name='rest_boards'),
    url(r'^boards/(?P<pk>\d+)/$',
        views.BoardDetail.as_view(), name='rest_board_detail'),
    url(r'^boards/(?P<pk>\d+)/topics/$',
        views.TopicList.as_view(), name='rest_topics'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$',
        views.TopicDetail.as_view(), name='rest_topic_detail'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/$',
        views.PostList.as_view(), name='rest_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/$',
        views.PostDetail.as_view(), name='rest_post_detail'),
]