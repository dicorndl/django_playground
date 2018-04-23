"""django_playground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
import oauth2_provider.views as oauth2_views

from accounts import views as accounts_views
from boards import views as boards_views


# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r"^authorize/$", oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r"^token/$", oauth2_views.TokenView.as_view(), name="token"),
    url(r"^revoke_token/$", oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r"^applications/$", oauth2_views.ApplicationList.as_view(), name="list"),
        url(r"^applications/register/$", oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r"^applications/(?P<pk>[\w-]+)/$", oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r"^applications/(?P<pk>[\w-]+)/delete/$", oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r"^applications/(?P<pk>[\w-]+)/update/$", oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # Oauth2 Token management views
    oauth2_endpoint_views += [
        url(r"^authorized_tokens/$", oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r"^authorized_tokens/(?P<pk>[\w-]+)/delete/$", oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # accounts
    url(r'signup/$', accounts_views.sign_up, name='signup'),
    url(r'login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),

    # password reset
    url(r'reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

    # settings
    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
    url(r'^settings/password/$',
        auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),

    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^boards/', include('boards.urls', namespace='boards')),
    url(r'^files/', include('files.urls', namespace='files')),
    url(r'^photos/', include('photos.urls', namespace='photos')),
    url(r'^snippets/', include('snippets.urls', namespace='snippets')),

    url(r'^o/', include(oauth2_endpoint_views, namespace='oauth2_provider')),
    url(r'^api/hello', boards_views.ApiEndpoint.as_view()),
]

# for development
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
