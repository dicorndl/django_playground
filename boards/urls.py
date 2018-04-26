from django.conf.urls import url

from . import rest_views
from . import views

urlpatterns = [
    url('^$', views.BoardListView.as_view(), name='home'),
    url('^(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url('^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url('^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    url('^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),
    url('^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),

    # REST
    url('^rest/boards/$',
        rest_views.BoardList.as_view(), name='rest_boards'),
    url(r'^rest/boards/(?P<pk>\d+)/$',
        rest_views.BoardDetail.as_view(), name='rest_board_detail'),
    url('^rest/boards/(?P<pk>\d+)/topics/$',
        rest_views.TopicList.as_view(), name='rest_topics'),
    url(r'^rest/boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$',
        rest_views.PostList.as_view(), name='rest_topic_posts'),
    url(r'^rest/boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/$',
        rest_views.PostDetail.as_view(), name='rest_post'),
]
