from django.conf.urls import url

from . import rest_views

urlpatterns = [
    url('^rest/accounts/$', rest_views.AccountList.as_view(), name='rest_accounts'),
    url('^rest/accounts/(?P<pk>\d+)/$', rest_views.AccountList.as_view(), name='rest_account_detail'),
]
