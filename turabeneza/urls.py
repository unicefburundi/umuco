from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from injira.views import ContactList, ContactDetail, save_embed

router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'contacts', ContactList)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'turabeneza.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/v1/contacts/$', ContactList.as_view(), name='contacts_list'),
    url(r'^api/v1/contacts/(?P<pk>[0-9]+)/$', ContactDetail.as_view(), name='contact_detail'),
    url(r'^injira/', include('injira.urls', namespace='injira_yo')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', save_embed),
)
