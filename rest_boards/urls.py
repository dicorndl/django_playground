from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^boards/$',
        views.BoardList.as_view(), name='boards'),
    url(r'^boards/(?P<pk>\d+)/$',
        views.BoardDetail.as_view(), name='board_detail'),
    url(r'^boards/(?P<pk>\d+)/topics/$',
        views.TopicList.as_view(), name='topics'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$',
        views.TopicDetail.as_view(), name='topic_detail'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/$',
        views.PostList.as_view(), name='posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/$',
        views.PostDetail.as_view(), name='post_detail'),
]