from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from injira.views import ContactList, ContactDetail, save_embed, piechart
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turabeneza.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^piechart/$', piechart),
    url(r'^api/v1/contacts/$', ContactList.as_view(), name='contacts_list'),
    url(r'^api/v1/contacts/(?P<pk>[0-9]+)/$', ContactDetail.as_view(), name='contact_detail'),
    url(r'^injira/', include('injira.urls', namespace='injira_yo')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', save_embed),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
urlpatterns += staticfiles_urlpatterns()