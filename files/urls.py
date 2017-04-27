from django.conf.urls import url

from files.views import upload, form

urlpatterns = [
    url(r'form/$', form),
    url(r'upload/$', upload),
]
