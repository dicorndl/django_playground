from django.conf.urls import url

from files.views import simple_upload

urlpatterns = [
    url(r'upload/$', simple_upload, name='upload'),
]
