from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from umuco.views import home, all_groups
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from umuco import backend


urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     url(r'^accounts/', include('authtools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$', backend.handel_rapidpro_request, name='add'),
    url(r'^report/', include('umuco.urls', namespace='report', app_name='umuco')),
    url(r'^groups/$', all_groups, name="groups"),
    url(r'^home/$', home, name="home"),
    url(r'^$', home, name="landing"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
urlpatterns += staticfiles_urlpatterns()
