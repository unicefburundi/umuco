from django.conf.urls import patterns, url
from bdiadmin.views import get_commune, get_colline

urlpatterns = patterns('',
        url(r'^get_commune/(?P<pk>\d+)/$', get_commune, name='get_commune'),
        url(r'^get_colline/(?P<pk>\d+)/$', get_colline, name='get_colline'),
)