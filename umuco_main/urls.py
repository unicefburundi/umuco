from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from umuco.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from umuco import backend

urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     url(r'^accounts/', include('authtools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add_group/$', backend.handel_rapidpro_request, name='add_group'),
    url(r'^report/', include('umuco.urls', namespace='report', app_name='umuco')),
    url(r'^groups/$', all_groups, name="groups"),
    url(r'^analytics/$', analytics, name="analytics"),
    url(r'^home/$', home, name="home"),
    url(r'^$', landing, name="landing_page"),
    url(r'^create/group/$', NaweNuzeCreate.as_view(), name='add_nawenuze'),
    url(r'^create/number/$', PhoneModelCreate.as_view(), name='add_number'),
    url(r'^reports/(?P<pk>\d+)$', NaweNuzeDetail.as_view(), name='reports_by_groups2'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
urlpatterns += staticfiles_urlpatterns()
